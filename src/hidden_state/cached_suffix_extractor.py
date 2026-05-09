"""Cached suffix hidden-state extraction for Stage 2 online evaluation.

Stage 2 keeps the Stage 1 best practices from notes/results_log.md but changes
the execution model: prompt variants share a candidate prefix, so the expensive
prefix forward should be reused and only the short suffix should be recomputed.
This module intentionally uses the model-provided `make_cache()` path because
Qwen3.5 uses a hybrid cache layout (`ArraysCache` for linear layers and
`KVCache` for full-attention layers).

The extractor returns raw block-output vectors, not L2-normalized vectors.
Scoring code decides whether to apply cosine, centering, anti-PCA, or another
Stage 1 winner. It stores only compact suffix/end positions, not full Tier B
all-position tensors.
"""

from __future__ import annotations

import copy
import gc
from dataclasses import dataclass
from typing import Any

import mlx.core as mx
import numpy as np
from mlx_lm.models.base import create_attention_mask, create_ssm_mask

from hidden_state.mlx_wrapper import MLXHiddenStateExtractor


PositionName = str
LayerIndex = int
VectorMap = dict[tuple[LayerIndex, PositionName], np.ndarray]
TopLogitMap = dict[PositionName, tuple[np.ndarray, np.ndarray]]


@dataclass
class ForwardOutput:
    vectors: VectorMap
    top_logits: TopLogitMap


@dataclass
class PrefixState:
    """A populated prefix cache plus prefix-position vectors.

    `cache` is mutable and must be deep-copied before suffix forwarding. The
    prefix vectors cover P1/no-suffix and the `content_end` control position
    for suffix prompts.
    """

    text: str
    token_ids: list[int]
    cache: list[Any]
    vectors: VectorMap
    token_count: int


class CachedSuffixExtractor:
    """Extract compact suffix/end hidden-state vectors with prefix KV reuse."""

    def __init__(
        self,
        model_path: str,
        *,
        clear_metal_cache_after_suffix: bool = True,
    ) -> None:
        self.model_path = model_path
        self.clear_metal_cache_after_suffix = clear_metal_cache_after_suffix
        self.extractor = MLXHiddenStateExtractor(model_path, dtype_note="mlx")
        self.model = self.extractor.model
        self.base_model = self.extractor.base_model
        self.tokenizer = self.extractor.tokenizer

    @property
    def num_layers(self) -> int:
        layer_count = self.extractor.num_layers
        if layer_count is None:
            raise TypeError("Loaded model does not expose base_model.layers.")
        return layer_count

    def prefill_prefix(
        self,
        text: str,
        target_layers: list[int],
        target_positions: list[str],
    ) -> PrefixState:
        """Forward the shared text prefix once and retain its cache.

        For P1/no-suffix, `last`/`minus2`/`minus3` are positions inside the
        prefix itself. For suffix prompts, `content_end` is the prefix-final
        vector. `suffix_start` is not defined for the prefix and is filled by
        suffix forwarding.
        """
        token_ids = self.tokenizer.encode(text)
        if not token_ids:
            raise ValueError("Tokenizer produced no prefix tokens.")

        cache = self.make_cache()
        prefix_positions = [
            position
            for position in target_positions
            if position in {"last", "minus2", "minus3", "content_end"}
        ]
        output = self._forward_collect(
            token_ids=token_ids,
            cache=cache,
            target_layers=target_layers,
            target_positions=prefix_positions,
            position_context="prefix",
        )
        return PrefixState(
            text=text,
            token_ids=token_ids,
            cache=cache,
            vectors=output.vectors,
            token_count=len(token_ids),
        )

    def encode_suffix(
        self,
        prefix_state: PrefixState,
        suffix_text: str,
        target_layers: list[int],
        target_positions: list[str],
    ) -> VectorMap:
        vectors, _top_logits = self.encode_suffix_with_logits(
            prefix_state=prefix_state,
            suffix_text=suffix_text,
            target_layers=target_layers,
            target_positions=target_positions,
            topk_logits=0,
        )
        return vectors

    def encode_suffix_with_logits(
        self,
        prefix_state: PrefixState,
        suffix_text: str,
        target_layers: list[int],
        target_positions: list[str],
        topk_logits: int = 0,
    ) -> tuple[VectorMap, TopLogitMap]:
        """Run a suffix from a deep-copied prefix cache and return vectors.

        The tokenizer split is verified exactly. If `encode(text + suffix)` is
        not prefixed by the cached prefix token sequence, reusing the cache
        would compare a different token sequence, so this fails loudly.
        """
        full_tokens = self.tokenizer.encode(prefix_state.text + suffix_text)
        if full_tokens[: len(prefix_state.token_ids)] != prefix_state.token_ids:
            raise ValueError(
                "Cannot reuse prefix cache: tokenizer boundary changed. "
                f"text={prefix_state.text[:80]!r}, suffix={suffix_text!r}, "
                f"prefix_len={len(prefix_state.token_ids)}, full_len={len(full_tokens)}"
            )
        suffix_tokens = full_tokens[len(prefix_state.token_ids) :]
        if not suffix_tokens:
            raise ValueError("Suffix tokenization produced no suffix tokens.")

        suffix_positions = [
            position
            for position in target_positions
            if position in {"last", "minus2", "minus3", "suffix_start"}
        ]
        cache = copy.deepcopy(prefix_state.cache)
        output = self._forward_collect(
            token_ids=suffix_tokens,
            cache=cache,
            target_layers=target_layers,
            target_positions=suffix_positions,
            position_context="suffix",
            topk_logits=topk_logits,
        )
        vectors = output.vectors

        if "content_end" in target_positions:
            for layer in target_layers:
                source = prefix_state.vectors.get((layer, "content_end"))
                if source is not None:
                    vectors[(layer, "content_end")] = source

        del cache
        # Stage 3 may reuse the Metal allocation cache across many short suffix
        # forwards. The live prefix KV cache remains referenced by PrefixState;
        # this only controls whether MLX/Metal reusable buffers are purged after
        # every suffix or at a coarser row/instance boundary by the caller.
        if self.clear_metal_cache_after_suffix:
            clear_mlx_memory(clear_metal_cache=True)
        return vectors, output.top_logits

    def encode_no_suffix(
        self,
        prefix_state: PrefixState,
        target_layers: list[int],
        target_positions: list[str],
    ) -> VectorMap:
        """Return prefix-position vectors for the P1/no-suffix stress test."""
        vectors: VectorMap = {}
        for layer in target_layers:
            for position in target_positions:
                if position == "suffix_start":
                    continue
                source_position = "content_end" if position == "content_end" else position
                source = prefix_state.vectors.get((layer, source_position))
                if source is not None:
                    vectors[(layer, position)] = source
        return vectors

    def make_cache(self) -> list[Any]:
        if hasattr(self.model, "make_cache"):
            return self.model.make_cache()
        if hasattr(self.model, "language_model") and hasattr(self.model.language_model, "make_cache"):
            return self.model.language_model.make_cache()
        raise TypeError("Loaded model does not expose make_cache().")

    def _forward_collect(
        self,
        token_ids: list[int],
        cache: list[Any] | None,
        target_layers: list[int],
        target_positions: list[str],
        position_context: str,
        topk_logits: int = 0,
    ) -> ForwardOutput:
        if topk_logits < 0:
            raise ValueError(f"topk_logits must be >= 0, got {topk_logits}.")
        layers = getattr(self.base_model, "layers", None)
        if not layers:
            raise TypeError("CachedSuffixExtractor requires base_model.layers.")
        if cache is None:
            cache = [None] * len(layers)
        if len(cache) != len(layers):
            raise ValueError(f"Cache length {len(cache)} != layer count {len(layers)}.")

        resolved_layers = [self._resolve_layer(layer) for layer in target_layers]
        target_layer_set = set(resolved_layers)
        input_ids = mx.array([token_ids], dtype=mx.int32)
        hidden_states = self.base_model.embed_tokens(input_ids)
        fa_mask = create_attention_mask(
            hidden_states,
            _cache_subset(cache, self.base_model.fa_idx),
        )
        ssm_mask = create_ssm_mask(
            hidden_states,
            _cache_subset(cache, self.base_model.ssm_idx),
        )

        selected: dict[tuple[int, str], mx.array] = {}
        resolved_top_logit_positions: dict[str, int] = {}
        for layer_index, (layer, layer_cache) in enumerate(zip(layers, cache, strict=True)):
            mask = ssm_mask if layer.is_linear else fa_mask
            hidden_states = layer(hidden_states, mask, layer_cache)
            if layer_index not in target_layer_set:
                continue

            for position_name in target_positions:
                resolved_position = self._resolve_position(
                    position_name,
                    seq_len=hidden_states.shape[1],
                    context=position_context,
                )
                if resolved_position is None:
                    continue
                selected[(layer_index, position_name)] = hidden_states[
                    :, resolved_position, :
                ].astype(mx.float32)
                if topk_logits > 0:
                    resolved_top_logit_positions[position_name] = resolved_position

        mx.eval(hidden_states)
        if selected:
            mx.eval(*selected.values())

        top_logits: TopLogitMap = {}
        if topk_logits > 0 and resolved_top_logit_positions:
            final_hidden = self.base_model.norm(hidden_states)
            logits = self.extractor._project_logits(final_hidden)
            vocab_size = int(logits.shape[-1])
            if topk_logits > vocab_size:
                raise ValueError(f"topk_logits={topk_logits} exceeds vocab_size={vocab_size}.")
            for position_name, resolved_position in resolved_top_logit_positions.items():
                position_logits = logits[:, resolved_position, :]
                top_ids = mx.argpartition(
                    position_logits,
                    kth=vocab_size - topk_logits,
                    axis=-1,
                )[:, -topk_logits:]
                top_values = mx.take_along_axis(position_logits, top_ids, axis=-1)
                order = mx.argsort(top_values, axis=-1)[:, ::-1]
                top_ids = mx.take_along_axis(top_ids, order, axis=-1)
                top_values = mx.take_along_axis(top_values, order, axis=-1)
                mx.eval(top_ids, top_values)
                top_logits[position_name] = (
                    np.array(top_ids[0], dtype=np.int32),
                    np.array(top_values[0], dtype=np.float32),
                )

        output: VectorMap = {}
        for key, value in selected.items():
            output[key] = np.array(value[0], dtype=np.float32)
            if not np.all(np.isfinite(output[key])):
                raise ValueError(f"Non-finite hidden vector for {key}.")
        return ForwardOutput(vectors=output, top_logits=top_logits)

    def _resolve_layer(self, layer_index: int) -> int:
        resolved = layer_index if layer_index >= 0 else self.num_layers + layer_index
        if resolved < 0 or resolved >= self.num_layers:
            raise ValueError(
                f"Layer {layer_index} resolves to {resolved}, outside [0, {self.num_layers - 1}]."
            )
        return resolved

    @staticmethod
    def _resolve_position(position: str, seq_len: int, context: str) -> int | None:
        mapping = {
            "last": -1,
            "minus2": -2,
            "minus3": -3,
            "suffix_start": 0,
            "content_end": -1,
        }
        if position not in mapping:
            raise ValueError(f"Unsupported position: {position}")
        if position == "suffix_start" and context != "suffix":
            return None
        if position == "content_end" and context != "prefix":
            return None

        index = mapping[position]
        resolved = seq_len + index if index < 0 else index
        if resolved < 0 or resolved >= seq_len:
            return None
        return resolved


def _cache_subset(cache: list[Any], indices: int | list[int]) -> Any:
    if isinstance(indices, int):
        return cache[indices]
    return [cache[index] for index in indices]


def clear_mlx_memory(*, clear_metal_cache: bool = True) -> None:
    gc.collect()
    if not clear_metal_cache:
        return
    try:
        if hasattr(mx, "metal") and hasattr(mx.metal, "clear_cache"):
            mx.metal.clear_cache()
    except Exception:
        pass
