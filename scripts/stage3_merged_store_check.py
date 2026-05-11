"""Self-consistency checks for a merged Stage 3 vector store.

This validates a post-merge Stage 3 store after the original source stores may
have been deleted. It checks manifest/chunk consistency and safetensors headers
without importing MLX, NumPy, or model libraries.

This is not a source-vs-merged byte comparison tool. The source-vs-merged audit
for the local prompt-sweep merge was performed before deleting source vectors;
see the merged store's MERGE_NOTES.md for details.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


KNOWN_MERGE_STRATEGIES = {"byte_preserving_chunk_copy_cpu"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--store", required=True, help="Merged Stage 3 store directory.")
    parser.add_argument("--expected-instances", type=int, default=100)
    parser.add_argument("--expected-min-instance", type=int, default=0)
    return parser.parse_args()


def read_header(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        header_len = int.from_bytes(handle.read(8), "little")
        header = json.loads(handle.read(header_len))
    header.pop("__metadata__", None)
    return header


def main() -> int:
    args = parse_args()
    store = Path(args.store)
    manifest_path = store / "manifest.json"
    errors: list[str] = []
    warnings: list[str] = []

    if not manifest_path.exists():
        print(f"FAIL missing manifest: {manifest_path}")
        return 1

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for key in [
        "chunks",
        "prompts",
        "prompt_variants",
        "layers",
        "positions",
        "tensor_key",
        "hidden_dim",
        "storage_dtype",
    ]:
        if key not in manifest:
            errors.append(f"manifest missing {key!r}")

    strategy = manifest.get("merge_strategy")
    if strategy is None:
        warnings.append("merge_strategy missing; this may be a canonical rechunked merge")
    elif strategy not in KNOWN_MERGE_STRATEGIES:
        warnings.append(f"unknown merge_strategy: {strategy!r}")

    if manifest.get("tensor_key") != "states":
        errors.append(f"tensor_key must be 'states', got {manifest.get('tensor_key')!r}")

    chunks = manifest.get("chunks", [])
    prompts = manifest.get("prompts", {})
    seen: set[str] = set()
    instances: set[int] = set()
    query_instances: set[int] = set()
    roles: dict[str, int] = {}
    chunk_files: list[str] = []
    topk_enabled = "topk_logits" in manifest

    for chunk_offset, chunk in enumerate(chunks):
        chunk_file = str(chunk.get("file", ""))
        if not chunk_file:
            errors.append(f"chunk {chunk_offset} missing file")
            continue
        chunk_files.append(chunk_file)
        path = store / chunk_file
        if not path.exists():
            errors.append(f"missing chunk file: {chunk_file}")
            continue

        prompt_ids = list(chunk.get("prompt_ids", []))
        row_count = int(chunk.get("row_count", len(prompt_ids)))
        if row_count != len(prompt_ids):
            errors.append(f"{chunk_file} row_count {row_count} != prompt_ids {len(prompt_ids)}")

        states_shape = chunk.get("states_shape")
        if states_shape and int(states_shape[0]) != row_count:
            errors.append(f"{chunk_file} states_shape rows {states_shape[0]} != {row_count}")

        if topk_enabled:
            for key in ["top_logit_token_ids_shape", "top_logit_values_shape"]:
                shape = chunk.get(key)
                if not shape:
                    errors.append(f"{chunk_file} missing {key}")
                elif int(shape[0]) != row_count:
                    errors.append(f"{chunk_file} {key} rows {shape[0]} != {row_count}")

        try:
            header = read_header(path)
        except Exception as exc:
            errors.append(f"{chunk_file} unreadable safetensors header: {exc}")
            continue

        if "states" not in header:
            errors.append(f"{chunk_file} missing states tensor")
        elif states_shape and list(header["states"].get("shape", [])) != list(states_shape):
            errors.append(f"{chunk_file} header states shape != manifest states_shape")

        if topk_enabled:
            expected_shapes = {
                "top_logit_token_ids": chunk.get("top_logit_token_ids_shape"),
                "top_logit_values": chunk.get("top_logit_values_shape"),
            }
            for tensor_name, expected_shape in expected_shapes.items():
                if tensor_name not in header:
                    errors.append(f"{chunk_file} missing {tensor_name}")
                elif expected_shape and list(header[tensor_name].get("shape", [])) != list(expected_shape):
                    errors.append(f"{chunk_file} header {tensor_name} shape != manifest shape")

        for row_index, prompt_id in enumerate(prompt_ids):
            if prompt_id in seen:
                errors.append(f"duplicate prompt_id in chunks: {prompt_id}")
                continue
            seen.add(prompt_id)
            meta = prompts.get(prompt_id)
            if not isinstance(meta, dict):
                errors.append(f"{prompt_id} missing prompt metadata")
                continue
            if str(meta.get("chunk_file")) != chunk_file:
                errors.append(f"{prompt_id} metadata chunk_file mismatch")
            if int(meta.get("chunk_index", -1)) != row_index:
                errors.append(f"{prompt_id} metadata chunk_index mismatch")
            instance = int(meta.get("instance_index", -1))
            role = str(meta.get("role", ""))
            instances.add(instance)
            roles[role] = roles.get(role, 0) + 1
            if role == "query":
                query_instances.add(instance)

    if seen != set(prompts):
        errors.append("prompt ids in chunks and manifest prompts differ")

    if len(chunk_files) != len(set(chunk_files)):
        errors.append("duplicate chunk file names in manifest")

    if args.expected_instances > 0:
        expected = set(range(args.expected_min_instance, args.expected_min_instance + args.expected_instances))
        if instances != expected:
            errors.append(f"instance set mismatch: n={len(instances)}")
        if query_instances != expected:
            errors.append(f"query instance set mismatch: n={len(query_instances)}")

    print(f"store: {store}")
    print(f"merge_strategy: {strategy if strategy is not None else '<missing>'}")
    print(f"chunks: {len(chunks)}")
    print(f"prompts: {len(prompts)}")
    print(
        "instances: "
        f"{min(instances) if instances else 'NA'}-{max(instances) if instances else 'NA'} "
        f"n={len(instances)}"
    )
    print(f"roles: {roles}")

    for warning in warnings:
        print(f"WARN {warning}")

    if errors:
        print("CHECK_FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CHECK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
