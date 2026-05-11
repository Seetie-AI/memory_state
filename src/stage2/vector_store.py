"""Compact vector storage for Stage 2 online evaluation.

Stage 2 should not recreate Tier B all-position dumps, but it should retain
Tier A-plus suffix/end vectors so future analysis does not rerun the model.
`Stage2VectorWriter` buffers a uniform tensor
`states: (n_prompts, n_variants, n_layers, n_positions, hidden_dim)` and writes
chunked safetensors plus a JSON manifest matching notes/stage_2_plan.md.
Stage 3 can optionally add sparse next-token top-k logits as parallel tensors;
the default schema remains unchanged when that option is disabled.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mlx.core as mx
import numpy as np


VectorKey = tuple[str, int, str]
TopLogitKey = tuple[str, str]
TopLogitValue = tuple[np.ndarray, np.ndarray]


@dataclass(frozen=True)
class PromptMetadata:
    prompt_id: str
    instance_index: int
    question_id: str
    role: str
    candidate_id: str | None
    is_gold: bool
    token_count: int
    resolved_positions: dict[str, int | None]


class Stage2VectorWriter:
    """Write compact Stage 2 vectors in bounded-size safetensor chunks."""

    def __init__(
        self,
        output_dir: str | Path,
        *,
        model_path: str,
        tokenizer_path: str,
        prompt_variants: list[str],
        layers: list[int],
        positions: list[str],
        score_modes_evaluated: list[str],
        target_chunk_mb: int = 512,
        topk_logits: int = 0,
    ) -> None:
        if topk_logits < 0:
            raise ValueError(f"topk_logits must be >= 0, got {topk_logits}.")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        existing_files = list(self.output_dir.iterdir())
        if existing_files:
            raise FileExistsError(
                f"Refusing to write into non-empty vector store directory: {self.output_dir}. "
                "Choose a new --output-dir or remove the old temporary run after review. "
                f"Existing entries include: {[path.name for path in existing_files[:5]]}"
            )
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.prompt_variants = prompt_variants
        self.layers = layers
        self.positions = positions
        self.score_modes_evaluated = score_modes_evaluated
        self.target_chunk_bytes = target_chunk_mb * 1024 * 1024
        self.topk_logits = topk_logits
        self.layer_index = {layer: index for index, layer in enumerate(layers)}
        self.variant_index = {variant: index for index, variant in enumerate(prompt_variants)}
        self.position_index = {position: index for index, position in enumerate(positions)}
        self.hidden_dim: int | None = None
        self.chunk_index = 0
        self.buffer_states: list[np.ndarray] = []
        self.buffer_top_logit_token_ids: list[np.ndarray] = []
        self.buffer_top_logit_values: list[np.ndarray] = []
        self.buffer_metadata: list[PromptMetadata] = []
        self.buffer_bytes = 0
        self.manifest: dict[str, Any] = {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "git_commit": os.environ.get("STAGE2_GIT_COMMIT", "unknown"),
            "model_path": model_path,
            "tokenizer_path": tokenizer_path,
            "prompt_variants": prompt_variants,
            "positions": positions,
            "layers": layers,
            "score_modes_evaluated": score_modes_evaluated,
            "tensor_key": "states",
            "tensor_shape": [
                "n_prompts",
                "n_variants",
                "n_layers",
                "n_positions",
                "hidden_dim",
            ],
            "storage_dtype": "bf16",
            "target_chunk_mb": target_chunk_mb,
            "chunks": [],
            "prompts": {},
        }
        if self.topk_logits > 0:
            self.manifest["topk_logits"] = {
                "enabled": True,
                "k": self.topk_logits,
                "token_ids_key": "top_logit_token_ids",
                "values_key": "top_logit_values",
                "tensor_shape": [
                    "n_prompts",
                    "n_variants",
                    "n_positions",
                    "k",
                ],
                "token_id_dtype": "int32",
                "value_dtype": "bf16",
                "description": "Final-layer next-token top-k logits at each stored prompt position.",
            }

    def add(
        self,
        metadata: PromptMetadata,
        vectors: dict[VectorKey, np.ndarray],
        top_logits: dict[TopLogitKey, TopLogitValue] | None = None,
    ) -> None:
        """Add one prompt row.

        Missing vectors are stored as NaN. This lets P1/no-suffix share the
        same schema while marking suffix-only positions such as `suffix_start`
        unavailable.
        """
        self._initialize_hidden_dim(vectors)
        assert self.hidden_dim is not None

        state = np.full(
            (
                len(self.prompt_variants),
                len(self.layers),
                len(self.positions),
                self.hidden_dim,
            ),
            np.nan,
            dtype=np.float32,
        )
        for (variant, layer, position), vector in vectors.items():
            if variant not in self.variant_index:
                continue
            if layer not in self.layer_index or position not in self.position_index:
                continue
            arr = np.asarray(vector, dtype=np.float32)
            if arr.shape != (self.hidden_dim,):
                raise ValueError(
                    f"{metadata.prompt_id} vector {(variant, layer, position)} "
                    f"shape {arr.shape} != ({self.hidden_dim},)"
                )
            state[
                self.variant_index[variant],
                self.layer_index[layer],
                self.position_index[position],
                :,
            ] = arr

        self.buffer_states.append(state)
        row_bytes = state.nbytes
        if self.topk_logits > 0:
            token_ids = np.full(
                (
                    len(self.prompt_variants),
                    len(self.positions),
                    self.topk_logits,
                ),
                -1,
                dtype=np.int32,
            )
            values = np.full(
                (
                    len(self.prompt_variants),
                    len(self.positions),
                    self.topk_logits,
                ),
                np.nan,
                dtype=np.float32,
            )
            if top_logits:
                for (variant, position), (ids, logits) in top_logits.items():
                    if variant not in self.variant_index or position not in self.position_index:
                        continue
                    ids_arr = np.asarray(ids, dtype=np.int32)
                    logits_arr = np.asarray(logits, dtype=np.float32)
                    expected_shape = (self.topk_logits,)
                    if ids_arr.shape != expected_shape or logits_arr.shape != expected_shape:
                        raise ValueError(
                            f"{metadata.prompt_id} top logits {(variant, position)} "
                            f"shapes {ids_arr.shape}/{logits_arr.shape} != {expected_shape}"
                        )
                    token_ids[
                        self.variant_index[variant],
                        self.position_index[position],
                        :,
                    ] = ids_arr
                    values[
                        self.variant_index[variant],
                        self.position_index[position],
                        :,
                    ] = logits_arr
            self.buffer_top_logit_token_ids.append(token_ids)
            self.buffer_top_logit_values.append(values)
            row_bytes += token_ids.nbytes + values.nbytes
        self.buffer_metadata.append(metadata)
        self.buffer_bytes += row_bytes
        if self.buffer_bytes >= self.target_chunk_bytes:
            self.flush_chunk()

    def flush_chunk(self) -> None:
        if not self.buffer_states:
            return

        chunk_name = f"chunk_{self.chunk_index:04d}.safetensors"
        chunk_path = self.output_dir / chunk_name
        states_np = np.stack(self.buffer_states, axis=0)
        states = mx.array(states_np, dtype=mx.bfloat16)
        tensors = {"states": states}
        top_logit_token_ids_np: np.ndarray | None = None
        top_logit_values_np: np.ndarray | None = None
        if self.topk_logits > 0:
            top_logit_token_ids_np = np.stack(self.buffer_top_logit_token_ids, axis=0)
            top_logit_values_np = np.stack(self.buffer_top_logit_values, axis=0)
            tensors["top_logit_token_ids"] = mx.array(top_logit_token_ids_np, dtype=mx.int32)
            tensors["top_logit_values"] = mx.array(top_logit_values_np, dtype=mx.bfloat16)
        mx.save_safetensors(str(chunk_path), tensors)

        prompt_ids = []
        for index, metadata in enumerate(self.buffer_metadata):
            prompt_ids.append(metadata.prompt_id)
            self.manifest["prompts"][metadata.prompt_id] = {
                "instance_index": metadata.instance_index,
                "question_id": metadata.question_id,
                "role": metadata.role,
                "candidate_id": metadata.candidate_id,
                "is_gold": metadata.is_gold,
                "token_count": metadata.token_count,
                "resolved_positions": metadata.resolved_positions,
                "chunk_file": chunk_name,
                "chunk_index": index,
            }

        chunk_record = {
            "file": chunk_name,
            "prompt_ids": prompt_ids,
            "row_count": len(prompt_ids),
            "states_shape": list(states_np.shape),
        }
        if top_logit_token_ids_np is not None and top_logit_values_np is not None:
            chunk_record["top_logit_token_ids_shape"] = list(top_logit_token_ids_np.shape)
            chunk_record["top_logit_values_shape"] = list(top_logit_values_np.shape)
        self.manifest["chunks"].append(chunk_record)
        self.chunk_index += 1
        self.buffer_states.clear()
        self.buffer_top_logit_token_ids.clear()
        self.buffer_top_logit_values.clear()
        self.buffer_metadata.clear()
        self.buffer_bytes = 0

    def close(self) -> None:
        self.flush_chunk()
        manifest_path = self.output_dir / "manifest.json"
        manifest_path.write_text(
            json.dumps(self.manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _initialize_hidden_dim(self, vectors: dict[VectorKey, np.ndarray]) -> None:
        if self.hidden_dim is not None:
            return
        for vector in vectors.values():
            arr = np.asarray(vector)
            if arr.ndim != 1:
                raise ValueError(f"Expected 1D vector, got shape {arr.shape}.")
            self.hidden_dim = int(arr.shape[0])
            self.manifest["hidden_dim"] = self.hidden_dim
            return
        raise ValueError("Cannot infer hidden_dim from empty vector dict.")
