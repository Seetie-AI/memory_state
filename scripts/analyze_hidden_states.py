"""Analyze hidden-state dumps without rerunning the LLM.

This script consumes tensors produced by `dump_hidden_states.py`. It supports
the reusable analysis loop requested after the Phase 2 negative result:
compare layer choices, score normalization, pairwise collapse, and selected
position/diagonal slices. Pooling experiments listed in MVP_Plan.md backburner
can be added here later; the initial implementation keeps those analyses
separate from layer-selection diagnostics.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mlx.core as mx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from eval.longmemeval_metrics import Prediction, evaluate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(ROOT / "tensors" / "dump_v1"))
    parser.add_argument(
        "--analysis",
        choices=[
            "layer_scan_retrieval",
            "pairwise_cosine_per_layer",
            "score_mode_comparison",
            "position_scan_within_layer",
            "diagonal_slice",
            "pool_combinations",
        ],
        required=True,
    )
    parser.add_argument("--layer", type=int, default=23)
    parser.add_argument("--score-mode", choices=["cosine", "dot", "centered_cosine"], default="cosine")
    parser.add_argument("--sample-prompts", type=int, default=256)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dump_dir = Path(args.dump_dir)
    manifest = json.loads((dump_dir / "manifest.json").read_text(encoding="utf-8"))

    if args.analysis == "layer_scan_retrieval":
        result = layer_scan_retrieval(dump_dir, manifest, score_mode=args.score_mode)
    elif args.analysis == "pairwise_cosine_per_layer":
        result = pairwise_cosine_per_layer(dump_dir, manifest, sample_prompts=args.sample_prompts)
    elif args.analysis == "score_mode_comparison":
        result = score_mode_comparison(dump_dir, manifest)
    elif args.analysis == "position_scan_within_layer":
        result = position_scan_within_layer(dump_dir, manifest, layer=args.layer, score_mode=args.score_mode)
    elif args.analysis == "diagonal_slice":
        result = diagonal_slice(dump_dir, manifest, score_mode=args.score_mode)
    elif args.analysis == "pool_combinations":
        result = pool_combinations(dump_dir, manifest, layer=args.layer, score_mode=args.score_mode)
    else:
        raise ValueError(f"Unsupported analysis: {args.analysis}")

    write_analysis_result(args.analysis, result)
    return 0


def layer_scan_retrieval(
    dump_dir: Path,
    manifest: dict[str, Any],
    score_mode: str,
) -> dict[str, Any]:
    """Evaluate retrieval for each Tier A layer and final post-norm vector."""
    records, tensors = load_tier_a(dump_dir, manifest)
    output: dict[str, Any] = {"score_mode": score_mode, "layers": {}}
    layer_count = tensors["last_by_layer"].shape[1]
    for layer in range(layer_count):
        vectors = tensors["last_by_layer"][:, layer, :]
        output["layers"][str(layer)] = evaluate_vectors(records, vectors, score_mode)
    output["final_post_norm"] = evaluate_vectors(records, tensors["final_post_norm"], score_mode)
    return output


def pairwise_cosine_per_layer(
    dump_dir: Path,
    manifest: dict[str, Any],
    sample_prompts: int,
) -> dict[str, Any]:
    """Measure prompt-vector collapse by pairwise cosine distribution per layer."""
    records, tensors = load_tier_a(dump_dir, manifest)
    del records
    vectors = tensors["last_by_layer"][:sample_prompts].astype(np.float32)
    result: dict[str, Any] = {"sample_prompts": int(vectors.shape[0]), "layers": {}}
    for layer in range(vectors.shape[1]):
        cosines = pairwise_cosines(vectors[:, layer, :])
        result["layers"][str(layer)] = summarize_array(cosines)
    result["final_post_norm"] = summarize_array(pairwise_cosines(tensors["final_post_norm"][:sample_prompts]))
    return result


def score_mode_comparison(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Compare raw dot, cosine, and centered cosine for each layer."""
    return {
        mode: layer_scan_retrieval(dump_dir, manifest, score_mode=mode)
        for mode in ["dot", "cosine", "centered_cosine"]
    }


def position_scan_within_layer(
    dump_dir: Path,
    manifest: dict[str, Any],
    layer: int,
    score_mode: str,
) -> dict[str, Any]:
    """Run retrieval on Tier B positions for one layer."""
    records, tensors = load_tier_b(dump_dir, manifest)
    positions = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, -1]
    output: dict[str, Any] = {"layer": layer, "score_mode": score_mode, "positions": {}}
    for position in positions:
        vectors = []
        kept_records = []
        for record, tensor in zip(records, tensors, strict=True):
            seq_len = tensor.shape[1]
            resolved = position if position >= 0 else seq_len + position
            if 0 <= resolved < seq_len:
                vectors.append(tensor[layer, resolved, :])
                kept_records.append(record)
        if vectors:
            output["positions"][str(position)] = evaluate_vectors(
                kept_records,
                np.stack(vectors, axis=0),
                score_mode,
            )
    return output


def diagonal_slice(dump_dir: Path, manifest: dict[str, Any], score_mode: str) -> dict[str, Any]:
    """Evaluate vectors from layer i, token i for Tier B prompts."""
    records, tensors = load_tier_b(dump_dir, manifest)
    vectors = []
    kept_records = []
    for record, tensor in zip(records, tensors, strict=True):
        max_diag = min(tensor.shape[0], tensor.shape[1])
        diag_vectors = [tensor[index, index, :] for index in range(max_diag)]
        vectors.append(np.mean(np.stack(diag_vectors, axis=0), axis=0))
        kept_records.append(record)
    return evaluate_vectors(kept_records, np.stack(vectors, axis=0), score_mode)


def pool_combinations(
    dump_dir: Path,
    manifest: dict[str, Any],
    layer: int,
    score_mode: str,
) -> dict[str, Any]:
    """Evaluate simple Tier B mean/max/last pooling combinations for one layer."""
    records, tensors = load_tier_b(dump_dir, manifest)
    pools: dict[str, list[np.ndarray]] = {"last": [], "mean": [], "max": []}
    for tensor in tensors:
        layer_tensor = tensor[layer]
        pools["last"].append(layer_tensor[-1])
        pools["mean"].append(np.mean(layer_tensor, axis=0))
        pools["max"].append(np.max(layer_tensor, axis=0))
    return {
        name: evaluate_vectors(records, np.stack(vectors, axis=0), score_mode)
        for name, vectors in pools.items()
    }


def load_tier_a(dump_dir: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, np.ndarray]]:
    records = []
    last_chunks = []
    final_chunks = []
    prompt_records = manifest["prompts"]
    for chunk in manifest["tier_a_chunks"]:
        arrays = mx.load(str(dump_dir / chunk["file"]))
        last = np.asarray(arrays["last_by_layer"].astype(mx.float32))
        final = np.asarray(arrays["final_post_norm"].astype(mx.float32))
        last_chunks.append(last)
        final_chunks.append(final)
        records.extend(prompt_records[prompt_id] for prompt_id in chunk["prompt_ids"])
    return records, {
        "last_by_layer": np.concatenate(last_chunks, axis=0),
        "final_post_norm": np.concatenate(final_chunks, axis=0),
    }


def load_tier_b(dump_dir: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], list[np.ndarray]]:
    records = []
    tensors = []
    for record in manifest["prompts"].values():
        if "tier_b_file" not in record:
            continue
        arrays = mx.load(str(dump_dir / record["tier_b_file"]))
        tensors.append(np.asarray(arrays["all_by_layer"].astype(mx.float32)))
        records.append(record)
    if not tensors:
        raise ValueError("No Tier B tensors found in manifest.")
    return records, tensors


def evaluate_vectors(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    score_mode: str,
) -> dict[str, Any]:
    by_instance: dict[int, dict[str, Any]] = {}
    for record, vector in zip(records, vectors, strict=True):
        bucket = by_instance.setdefault(
            int(record["instance_index"]),
            {"query": None, "candidates": []},
        )
        if record["role"] == "query":
            bucket["query"] = (record, vector)
        else:
            bucket["candidates"].append((record, vector))

    predictions = []
    for bucket in by_instance.values():
        if bucket["query"] is None or not bucket["candidates"]:
            continue
        query_record, query_vector = bucket["query"]
        candidate_records = [item[0] for item in bucket["candidates"]]
        candidate_vectors = np.stack([item[1] for item in bucket["candidates"]], axis=0)
        scores = score_vectors(query_vector, candidate_vectors, score_mode)
        order = np.argsort(scores)[::-1][:50]
        retrieved = [candidate_records[index]["candidate_id"] for index in order]
        gold = [record["candidate_id"] for record in candidate_records if record["is_gold"]]
        predictions.append(
            Prediction(
                question_id=query_record["question_id"],
                retrieved_ids=retrieved,
                gold_ids=gold,
                is_abstention="_abs" in query_record["question_id"],
                has_target=bool(gold),
            )
        )
    return evaluate(predictions, skip_abstention=True, bootstrap_samples=200)


def score_vectors(query: np.ndarray, candidates: np.ndarray, mode: str) -> np.ndarray:
    if mode == "dot":
        return candidates @ query
    if mode == "cosine":
        return normalize(candidates) @ normalize(query)
    if mode == "centered_cosine":
        centered_candidates = candidates - np.mean(candidates, axis=0, keepdims=True)
        centered_query = query - np.mean(candidates, axis=0)
        return normalize(centered_candidates) @ normalize(centered_query)
    raise ValueError(f"Unsupported score mode: {mode}")


def normalize(array: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(array, axis=-1, keepdims=True)
    return array / np.maximum(norms, 1e-12)


def pairwise_cosines(vectors: np.ndarray) -> np.ndarray:
    normalized = normalize(vectors.astype(np.float32))
    matrix = normalized @ normalized.T
    upper = np.triu_indices(matrix.shape[0], k=1)
    return matrix[upper]


def summarize_array(values: np.ndarray) -> dict[str, float]:
    return {
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
    }


def write_analysis_result(name: str, result: dict[str, Any]) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result_dir = ROOT / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    json_path = result_dir / f"analysis_{name}_{timestamp}.json"
    md_path = result_dir / f"analysis_{name}_{timestamp}.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown_summary(name, result, json_path), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


def render_markdown_summary(name: str, result: dict[str, Any], json_path: Path) -> str:
    return "\n".join(
        [
            f"# Analysis: {name}",
            "",
            f"Full JSON: `{json_path}`",
            "",
            "This summary is intentionally brief; inspect the JSON for per-layer metrics.",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2)[:4000],
            "```",
            "",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
