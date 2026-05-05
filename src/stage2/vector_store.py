"""Compact vector storage for Stage 2 online evaluation.

Stage 2 should not recreate Tier B all-position dumps, but it should retain
Tier A-plus suffix/end vectors so future analysis does not rerun the model.
`Stage2VectorWriter` buffers a uniform tensor
`states: (n_prompts, n_variants, n_layers, n_positions, hidden_dim)` and writes
chunked safetensors plus a JSON manifest matching notes/stage_2_plan.md.
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
    ) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        if (self.output_dir / "manifest.json").exists():
            raise FileExistsError(
                f"Refusing to overwrite existing Stage 2 vector store: {self.output_dir}. "
                "Choose a new --output-dir or remove the old temporary run after review."
            )
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.prompt_variants = prompt_variants
        self.layers = layers
        self.positions = positions
        self.score_modes_evaluated = score_modes_evaluated
        self.target_chunk_bytes = target_chunk_mb * 1024 * 1024
        self.layer_index = {layer: index for index, layer in enumerate(layers)}
        self.variant_index = {variant: index for index, variant in enumerate(prompt_variants)}
        self.position_index = {position: index for index, position in enumerate(positions)}
        self.hidden_dim: int | None = None
        self.chunk_index = 0
        self.buffer_states: list[np.ndarray] = []
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

    def add(
        self,
        metadata: PromptMetadata,
        vectors: dict[VectorKey, np.ndarray],
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
        self.buffer_metadata.append(metadata)
        self.buffer_bytes += state.nbytes
        if self.buffer_bytes >= self.target_chunk_bytes:
            self.flush_chunk()

    def flush_chunk(self) -> None:
        if not self.buffer_states:
            return

        chunk_name = f"chunk_{self.chunk_index:04d}.safetensors"
        chunk_path = self.output_dir / chunk_name
        states_np = np.stack(self.buffer_states, axis=0)
        states = mx.array(states_np, dtype=mx.bfloat16)
        mx.save_safetensors(str(chunk_path), {"states": states})

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

        self.manifest["chunks"].append(
            {
                "file": chunk_name,
                "prompt_ids": prompt_ids,
                "row_count": len(prompt_ids),
                "states_shape": list(states_np.shape),
            }
        )
        self.chunk_index += 1
        self.buffer_states.clear()
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
