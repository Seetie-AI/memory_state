"""MLX hidden-state extraction for the MVP memory retrieval experiment.

This wrapper implements the option (A) definition from MVP_Plan.md sections
3.2 and 6.2: run one forward pass over the prompt and take a prompt-final
hidden state. By default, target_layer_index=None preserves the original path
exactly: call base_model(input_ids) and use the final-layer post-norm hidden
state. That default exists so older Phase 2 results stay reproducible.

For the layer-selection follow-up, target_layer_index can select a raw block
output. This is not a pooling experiment: MVP_Plan.md backburner items such as
mean pooling and sentinel-token pooling are adjacent ideas, but this branch
changes only which layer supplies the prompt-final vector. We intentionally do
not feed the generated token back into the model, because that would measure a
different "after the model sees its own token" state.

The wrapper does not fork mlx-lm and does not monkey-patch package internals.
Instead it calls the loaded model's internal base language model directly. It
auto-detects both multimodal-style layouts (for example
model.language_model.model) and text-only layouts (for example model.model).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import mlx.core as mx
import numpy as np
from mlx_lm import load
from mlx_lm.models.base import create_attention_mask, create_ssm_mask


@dataclass(frozen=True)
class HiddenStateResult:
    """Prompt-final hidden-state result used by the sanity-check script."""

    next_token_text: str
    vector: np.ndarray
    top_token_ids: list[int]
    top_token_texts: list[str]
    layer_index_raw: int | None
    layer_index_resolved: int | None
    num_layers: int | None
    hidden_state_norm: str


class MLXHiddenStateExtractor:
    """Extract option-A hidden-state vectors from an mlx-lm model."""

    def __init__(
        self,
        model_id: str,
        dtype_note: str = "bf16",
        target_layer_index: int | None = None,
    ) -> None:
        self.model_id = model_id
        self.dtype_note = dtype_note
        self.target_layer_index = target_layer_index
        self.model, self.tokenizer = load(model_id)
        self.base_model, self.lm_head, self.embed_tokens, self.tied = (
            self._detect_model_parts(self.model)
        )

    @staticmethod
    def _detect_model_parts(model: Any) -> tuple[Any, Any | None, Any | None, bool]:
        """Return base model, LM head, embedding table, and tied-weight flag."""
        if hasattr(model, "language_model"):
            language_model = model.language_model
            base_model = getattr(language_model, "model", None)
            lm_head = getattr(language_model, "lm_head", None)
            embed_tokens = getattr(base_model, "embed_tokens", None)
            args = getattr(language_model, "args", getattr(model, "args", None))
            tied = bool(getattr(args, "tie_word_embeddings", False))
            if base_model is not None:
                return base_model, lm_head, embed_tokens, tied

        if hasattr(model, "model"):
            base_model = model.model
            lm_head = getattr(model, "lm_head", None)
            embed_tokens = getattr(base_model, "embed_tokens", None)
            args = getattr(model, "args", None)
            tied = bool(getattr(args, "tie_word_embeddings", False))
            return base_model, lm_head, embed_tokens, tied

        raise TypeError(f"Unsupported mlx-lm model layout: {type(model)!r}")

    def encode_prompt(self, prompt: str, top_k: int = 5) -> HiddenStateResult:
        token_ids = self.tokenizer.encode(prompt)
        if not token_ids:
            raise ValueError("Tokenizer produced no tokens for prompt.")

        input_ids = mx.array([token_ids], dtype=mx.int32)
        if self.target_layer_index is None:
            # Backward compatibility: None uses the exact original mlx-lm base
            # model call and final post-norm hidden state.
            hidden = self.base_model(input_ids)
            # NumPy cannot read MLX bf16 tensors through the buffer protocol, so
            # cast inside MLX before converting the vector to a NumPy array.
            selected_hidden = hidden[:, -1, :].astype(mx.float32)
        else:
            hidden, selected_hidden = self._forward_with_target_layer(input_ids)

        logits = self._project_logits(hidden)[:, -1, :]

        top_indices = mx.argsort(logits, axis=-1)[:, -top_k:][:, ::-1]
        next_token_id = top_indices[:, 0]
        mx.eval(selected_hidden, top_indices, next_token_id)

        vector = np.array(selected_hidden[0])
        vector = _l2_normalize(vector)
        top_ids = [int(x) for x in np.asarray(top_indices[0]).tolist()]
        top_texts = [self.tokenizer.decode([token_id]) for token_id in top_ids]
        metadata = self.layer_metadata()

        return HiddenStateResult(
            next_token_text=top_texts[0],
            vector=vector,
            top_token_ids=top_ids,
            top_token_texts=top_texts,
            layer_index_raw=metadata["hidden_state_layer_index_raw"],
            layer_index_resolved=metadata["hidden_state_layer_index_resolved"],
            num_layers=metadata["hidden_state_num_layers"],
            hidden_state_norm=metadata["hidden_state_norm"],
        )

    def _project_logits(self, hidden: mx.array) -> mx.array:
        if self.tied:
            if self.embed_tokens is None or not hasattr(self.embed_tokens, "as_linear"):
                raise TypeError("Model declares tied embeddings but no as_linear path exists.")
            return self.embed_tokens.as_linear(hidden)

        if self.lm_head is None:
            raise TypeError("Model has no lm_head and does not declare tied embeddings.")
        return self.lm_head(hidden)

    def _forward_with_target_layer(self, input_ids: mx.array) -> tuple[mx.array, mx.array]:
        """Run all layers once while saving one intermediate block output.

        The saved vector is the raw block output at target_layer_index, not final
        norm output. We still continue to the final layer and norm so top-token
        auditing uses the real final logits.
        """
        layers = getattr(self.base_model, "layers", None)
        if not layers:
            raise TypeError("Intermediate layer extraction requires base_model.layers.")

        target_index = self._resolve_layer_index(self.target_layer_index)
        hidden_states = self.base_model.embed_tokens(input_ids)
        cache = [None] * len(layers)
        fa_mask = create_attention_mask(
            hidden_states,
            _cache_subset(cache, self.base_model.fa_idx),
        )
        ssm_mask = create_ssm_mask(
            hidden_states,
            _cache_subset(cache, self.base_model.ssm_idx),
        )
        selected_hidden = None

        for index, (layer, layer_cache) in enumerate(zip(layers, cache, strict=True)):
            mask = ssm_mask if layer.is_linear else fa_mask
            hidden_states = layer(hidden_states, mask, layer_cache)
            if index == target_index:
                # This experiment changes only the layer source. Do not apply
                # final norm to intermediate block outputs; final norm is
                # calibrated for the completed residual stream.
                selected_hidden = hidden_states[:, -1, :].astype(mx.float32)

        if selected_hidden is None:
            raise RuntimeError(f"Target layer {target_index} was not reached.")

        final_hidden = self.base_model.norm(hidden_states)
        return final_hidden, selected_hidden

    def _resolve_layer_index(self, layer_index: int | None) -> int | None:
        if layer_index is None:
            return None
        layer_count = self.num_layers
        if layer_count is None:
            raise TypeError("Cannot resolve layer index without base_model.layers.")
        resolved = layer_index if layer_index >= 0 else layer_count + layer_index
        if resolved < 0 or resolved >= layer_count:
            raise ValueError(
                f"target_layer_index {layer_index} resolves to {resolved}, "
                f"outside valid range [0, {layer_count - 1}]"
            )
        return resolved

    @property
    def num_layers(self) -> int | None:
        layers = getattr(self.base_model, "layers", None)
        return len(layers) if layers is not None else None

    def layer_metadata(self) -> dict[str, int | str | None]:
        resolved = self._resolve_layer_index(self.target_layer_index)
        return {
            "hidden_state_layer_index_raw": self.target_layer_index,
            "hidden_state_layer_index_resolved": resolved,
            "hidden_state_num_layers": self.num_layers,
            "hidden_state_norm": (
                "final_post_norm" if self.target_layer_index is None else "none_for_intermediate"
            ),
        }


def extract_hidden_state(
    model_id: str,
    prompt: str,
    target_layer_index: int | None = None,
) -> tuple[str, np.ndarray]:
    """Return (next_token_text, l2-normalized prompt-final hidden vector)."""
    result = MLXHiddenStateExtractor(
        model_id,
        target_layer_index=target_layer_index,
    ).encode_prompt(prompt)
    return result.next_token_text, result.vector


def _l2_normalize(vector: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if norm == 0.0 or not np.isfinite(norm):
        raise ValueError("Cannot normalize hidden state with zero/non-finite norm.")
    return vector / norm


def _cache_subset(cache: list[Any], indices: int | list[int]) -> Any:
    if isinstance(indices, int):
        return cache[indices]
    return [cache[index] for index in indices]
