"""Merge disjoint Stage 3 vector stores from multi-machine runs.

This script is intentionally only a storage merge. It does not compute retrieval
metrics because geometry transforms such as anti-PCA must be fit on the merged
candidate corpus. Per-machine metrics are useful for smoke tests but are not the
final Stage 3 result.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mlx.core as mx
import numpy as np


@dataclass(frozen=True)
class RowRef:
    source_index: int
    store_dir: Path
    chunk_file: str
    chunk_index: int
    prompt_id: str
    metadata: dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store-a", required=True)
    parser.add_argument("--store-b", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--target-chunk-mb", type=int, default=512)
    return parser.parse_args()


def load_manifest(store_dir: Path) -> dict[str, Any]:
    manifest_path = store_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing manifest: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def validate_compatible(manifests: list[dict[str, Any]]) -> None:
    required = ["chunks", "prompts", "prompt_variants", "layers", "positions", "tensor_key"]
    for index, manifest in enumerate(manifests):
        missing = [key for key in required if key not in manifest]
        if missing:
            raise ValueError(f"store {index} manifest missing keys: {missing}")
        if manifest["tensor_key"] != "states":
            raise ValueError(f"store {index} tensor_key must be 'states', got {manifest['tensor_key']!r}")
        if not manifest["chunks"]:
            raise ValueError(f"store {index} has no chunks")

    baseline = manifests[0]
    keys_to_match = [
        "prompt_variants",
        "layers",
        "positions",
        "tensor_shape",
        "hidden_dim",
        "storage_dtype",
    ]
    for key in keys_to_match:
        values = [manifest.get(key) for manifest in manifests]
        if any(value != values[0] for value in values[1:]):
            raise ValueError(f"Stores have incompatible {key}: {values}")

    # The same model can live under different absolute paths on two machines.
    # Compare the final model/tokenizer directory names so obvious checkpoint
    # mismatches fail while `/Users/gordon/.../Qwen...` and `/Users/lin/.../Qwen...`
    # can still merge.
    for key in ["model_path", "tokenizer_path"]:
        labels = [Path(str(manifest.get(key, ""))).name for manifest in manifests]
        if any(label != labels[0] for label in labels[1:]):
            raise ValueError(f"Stores appear to use different {key}: {labels}")

    topk_values = [manifest.get("topk_logits") for manifest in manifests]
    if any(value != topk_values[0] for value in topk_values[1:]):
        raise ValueError("Stores must either all omit topk_logits or use the same topk schema.")


def collect_rows(store_dirs: list[Path], manifests: list[dict[str, Any]]) -> list[RowRef]:
    instance_sets: list[set[int]] = []
    prompt_ids_seen: set[str] = set()
    rows: list[RowRef] = []

    for source_index, (store_dir, manifest) in enumerate(zip(store_dirs, manifests, strict=True)):
        prompt_meta = manifest["prompts"]
        topk_enabled = "topk_logits" in manifest
        instances = {int(meta["instance_index"]) for meta in prompt_meta.values()}
        instance_sets.append(instances)

        for chunk in manifest["chunks"]:
            chunk_file = str(chunk["file"])
            chunk_path = store_dir / chunk_file
            if not chunk_path.exists():
                raise FileNotFoundError(f"Manifest references missing chunk: {chunk_path}")
            prompt_ids = list(chunk["prompt_ids"])
            if int(chunk.get("row_count", len(prompt_ids))) != len(prompt_ids):
                raise ValueError(
                    f"{store_dir} chunk {chunk_file} row_count does not match prompt_ids length."
                )
            if "states_shape" in chunk and int(chunk["states_shape"][0]) != len(prompt_ids):
                raise ValueError(
                    f"{store_dir} chunk {chunk_file} states_shape row count does not match prompt_ids."
                )
            if topk_enabled and (
                "top_logit_token_ids_shape" not in chunk or "top_logit_values_shape" not in chunk
            ):
                raise ValueError(f"{store_dir} chunk {chunk_file} lacks top-logit shape records.")
            for position_in_chunk, prompt_id in enumerate(prompt_ids):
                if prompt_id in prompt_ids_seen:
                    raise ValueError(f"Duplicate prompt_id across stores: {prompt_id}")
                prompt_ids_seen.add(prompt_id)
                meta = dict(prompt_meta[prompt_id])
                if str(meta.get("chunk_file")) != chunk_file:
                    raise ValueError(f"{prompt_id} chunk_file disagrees with chunk list.")
                if int(meta.get("chunk_index", -1)) != position_in_chunk:
                    raise ValueError(f"{prompt_id} chunk_index disagrees with chunk prompt order.")
                rows.append(
                    RowRef(
                        source_index=source_index,
                        store_dir=store_dir,
                        chunk_file=chunk_file,
                        chunk_index=int(meta["chunk_index"]),
                        prompt_id=prompt_id,
                        metadata=meta,
                    )
                )

    overlap = instance_sets[0].intersection(*instance_sets[1:]) if len(instance_sets) > 1 else set()
    if overlap:
        sample = sorted(overlap)[:10]
        raise ValueError(
            "Two-machine slices overlap on instance_index values; "
            f"examples={sample}. Re-run with disjoint --subset-start ranges."
        )

    role_order = {"candidate": 0, "query": 1}
    return sorted(
        rows,
        key=lambda row: (
            int(row.metadata["instance_index"]),
            role_order.get(str(row.metadata["role"]), 99),
            str(row.metadata.get("candidate_id") or ""),
            row.prompt_id,
        ),
    )


def make_output_manifest(
    manifests: list[dict[str, Any]],
    store_dirs: list[Path],
    target_chunk_mb: int,
) -> dict[str, Any]:
    base = manifests[0]
    output = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": os.environ.get("STAGE3_MERGE_GIT_COMMIT", "unknown"),
        "model_path": base.get("model_path"),
        "tokenizer_path": base.get("tokenizer_path"),
        "prompt_variants": base["prompt_variants"],
        "positions": base["positions"],
        "layers": base["layers"],
        "score_modes_evaluated": base.get("score_modes_evaluated", []),
        "tensor_key": "states",
        "tensor_shape": base["tensor_shape"],
        "storage_dtype": base.get("storage_dtype", "bf16"),
        "hidden_dim": base["hidden_dim"],
        "target_chunk_mb": target_chunk_mb,
        "chunks": [],
        "prompts": {},
        "stage3_merged_from": [str(path) for path in store_dirs],
        "merge_note": (
            "Merged disjoint Stage 3 stores. Fit anti-PCA and other geometry "
            "transforms on this merged corpus, not on per-machine split metrics."
        ),
    }
    if "topk_logits" in base:
        output["topk_logits"] = base["topk_logits"]
    return output


def load_source_row(
    row: RowRef,
    cache: dict[tuple[int, str], dict[str, mx.array]],
    *,
    expect_top_logits: bool,
) -> dict[str, np.ndarray]:
    cache_key = (row.source_index, row.chunk_file)
    tensors = cache.get(cache_key)
    if tensors is None:
        cache.clear()
        tensors = mx.load(str(row.store_dir / row.chunk_file))
        cache[cache_key] = tensors

    if row.chunk_index >= int(tensors["states"].shape[0]):
        raise ValueError(f"{row.prompt_id} chunk_index is outside states tensor rows.")
    output = {
        "states": np.array(tensors["states"][row.chunk_index].astype(mx.float32)),
    }
    if expect_top_logits and (
        "top_logit_token_ids" not in tensors or "top_logit_values" not in tensors
    ):
        raise ValueError(
            f"{row.store_dir / row.chunk_file} is missing top-logit tensors "
            "although manifest declares topk_logits."
        )
    if "top_logit_token_ids" in tensors:
        if row.chunk_index >= int(tensors["top_logit_token_ids"].shape[0]):
            raise ValueError(f"{row.prompt_id} chunk_index is outside top-logit tensor rows.")
        output["top_logit_token_ids"] = np.array(
            tensors["top_logit_token_ids"][row.chunk_index],
            dtype=np.int32,
        )
        output["top_logit_values"] = np.array(
            tensors["top_logit_values"][row.chunk_index].astype(mx.float32),
            dtype=np.float32,
        )
    return output


def write_chunk(
    output_dir: Path,
    manifest: dict[str, Any],
    chunk_index: int,
    prompt_ids: list[str],
    metadata_rows: list[dict[str, Any]],
    states_rows: list[np.ndarray],
    top_id_rows: list[np.ndarray],
    top_value_rows: list[np.ndarray],
) -> int:
    if not states_rows:
        return chunk_index

    chunk_name = f"chunk_{chunk_index:04d}.safetensors"
    states_np = np.stack(states_rows, axis=0)
    tensors: dict[str, mx.array] = {"states": mx.array(states_np, dtype=mx.bfloat16)}

    top_ids_np: np.ndarray | None = None
    top_values_np: np.ndarray | None = None
    if top_id_rows:
        if len(top_id_rows) != len(states_rows) or len(top_value_rows) != len(states_rows):
            raise ValueError("Top-logit row count does not match states row count.")
        top_ids_np = np.stack(top_id_rows, axis=0)
        top_values_np = np.stack(top_value_rows, axis=0)
        tensors["top_logit_token_ids"] = mx.array(top_ids_np, dtype=mx.int32)
        tensors["top_logit_values"] = mx.array(top_values_np, dtype=mx.bfloat16)

    mx.save_safetensors(str(output_dir / chunk_name), tensors)

    for row_index, (prompt_id, metadata) in enumerate(zip(prompt_ids, metadata_rows, strict=True)):
        updated = dict(metadata)
        updated["chunk_file"] = chunk_name
        updated["chunk_index"] = row_index
        manifest["prompts"][prompt_id] = updated

    chunk_record = {
        "file": chunk_name,
        "prompt_ids": prompt_ids,
        "row_count": len(prompt_ids),
        "states_shape": list(states_np.shape),
    }
    if top_ids_np is not None and top_values_np is not None:
        chunk_record["top_logit_token_ids_shape"] = list(top_ids_np.shape)
        chunk_record["top_logit_values_shape"] = list(top_values_np.shape)
    manifest["chunks"].append(chunk_record)
    return chunk_index + 1


def main() -> int:
    args = parse_args()
    store_dirs = [Path(args.store_a), Path(args.store_b)]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    existing_files = list(output_dir.iterdir())
    if existing_files:
        raise FileExistsError(
            f"Refusing to write into non-empty merged store directory: {output_dir}. "
            f"Existing entries include: {[path.name for path in existing_files[:5]]}"
        )

    manifests = [load_manifest(path) for path in store_dirs]
    validate_compatible(manifests)
    rows = collect_rows(store_dirs, manifests)
    manifest = make_output_manifest(manifests, store_dirs, args.target_chunk_mb)
    expect_top_logits = "topk_logits" in manifest

    target_bytes = args.target_chunk_mb * 1024 * 1024
    chunk_index = 0
    buffer_bytes = 0
    prompt_ids: list[str] = []
    metadata_rows: list[dict[str, Any]] = []
    states_rows: list[np.ndarray] = []
    top_id_rows: list[np.ndarray] = []
    top_value_rows: list[np.ndarray] = []
    chunk_cache: dict[tuple[int, str], dict[str, mx.array]] = {}

    for row in rows:
        tensors = load_source_row(row, chunk_cache, expect_top_logits=expect_top_logits)
        prompt_ids.append(row.prompt_id)
        metadata_rows.append(row.metadata)
        states_rows.append(tensors["states"])
        buffer_bytes += tensors["states"].nbytes
        if "top_logit_token_ids" in tensors:
            top_id_rows.append(tensors["top_logit_token_ids"])
            top_value_rows.append(tensors["top_logit_values"])
            buffer_bytes += tensors["top_logit_token_ids"].nbytes + tensors["top_logit_values"].nbytes

        if buffer_bytes >= target_bytes:
            chunk_index = write_chunk(
                output_dir,
                manifest,
                chunk_index,
                prompt_ids,
                metadata_rows,
                states_rows,
                top_id_rows,
                top_value_rows,
            )
            prompt_ids = []
            metadata_rows = []
            states_rows = []
            top_id_rows = []
            top_value_rows = []
            buffer_bytes = 0

    write_chunk(
        output_dir,
        manifest,
        chunk_index,
        prompt_ids,
        metadata_rows,
        states_rows,
        top_id_rows,
        top_value_rows,
    )
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Merged {len(rows)} prompt rows into {output_dir}")
    print(f"instances: {min(int(r.metadata['instance_index']) for r in rows)}-"
          f"{max(int(r.metadata['instance_index']) for r in rows)}")
    print(f"chunks: {len(manifest['chunks'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
