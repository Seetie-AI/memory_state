"""MLX hidden-state extraction for the MVP memory retrieval experiment.

This wrapper implements the option (A) definition from MVP_Plan.md sections
3.2 and 6.2: run one forward pass over the prompt and take the prompt-final,
final-layer post-norm hidden state. That vector is the state used to predict
the first one-word summary token. We intentionally do not feed the generated
token back into the model, because that would measure a different "after the
model sees its own token" state.

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


@dataclass(frozen=True)
class HiddenStateResult:
    """Prompt-final hidden-state result used by the sanity-check script."""

    next_token_text: str
    vector: np.ndarray
    top_token_ids: list[int]
    top_token_texts: list[str]


class MLXHiddenStateExtractor:
    """Extract option-A hidden-state vectors from an mlx-lm model."""

    def __init__(self, model_id: str, dtype_note: str = "bf16") -> None:
        self.model_id = model_id
        self.dtype_note = dtype_note
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
        hidden = self.base_model(input_ids)
        last_hidden = hidden[:, -1, :]
        logits = self._project_logits(hidden)[:, -1, :]

        top_indices = mx.argsort(logits, axis=-1)[:, -top_k:][:, ::-1]
        next_token_id = top_indices[:, 0]
        mx.eval(last_hidden, top_indices, next_token_id)

        vector = np.asarray(last_hidden[0], dtype=np.float32)
        vector = _l2_normalize(vector)
        top_ids = [int(x) for x in np.asarray(top_indices[0]).tolist()]
        top_texts = [self.tokenizer.decode([token_id]) for token_id in top_ids]

        return HiddenStateResult(
            next_token_text=top_texts[0],
            vector=vector,
            top_token_ids=top_ids,
            top_token_texts=top_texts,
        )

    def _project_logits(self, hidden: mx.array) -> mx.array:
        if self.tied:
            if self.embed_tokens is None or not hasattr(self.embed_tokens, "as_linear"):
                raise TypeError("Model declares tied embeddings but no as_linear path exists.")
            return self.embed_tokens.as_linear(hidden)

        if self.lm_head is None:
            raise TypeError("Model has no lm_head and does not declare tied embeddings.")
        return self.lm_head(hidden)


def extract_hidden_state(model_id: str, prompt: str) -> tuple[str, np.ndarray]:
    """Return (next_token_text, l2-normalized prompt-final hidden vector)."""
    result = MLXHiddenStateExtractor(model_id).encode_prompt(prompt)
    return result.next_token_text, result.vector


def _l2_normalize(vector: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if norm == 0.0 or not np.isfinite(norm):
        raise ValueError("Cannot normalize hidden state with zero/non-finite norm.")
    return vector / norm

