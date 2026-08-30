"""Stage 3 LongMemEval sparse-logits retrieval/fusion probe.

Uses Stage 3 saved top-256 next-token logits to test PromptReps-style sparse
representations and simple dense+sparse fusion. This script is intentionally
offline and reads the merged Stage 3 store once for all selected cells.
"""

from __future__ import annotations

import argparse
import gc
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from safetensors.torch import load_file


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
for path in [SCRIPTS, SRC]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import stage2_offline_analyze as offline
from eval.longmemeval_metrics import Prediction, evaluate


DEFAULT_DUMP_DIR = ROOT / "tensors" / "stage3" / "prompt_sweep" / "merged_subset0-100_cache2gb_logits256"
DEFAULT_DATA = ROOT / "data" / "longmemeval_s_cleaned.json"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "prompt_fusion" / "logits_fusion"
DEFAULT_OUTPUT_PREFIX = "logits_sparse_fusion"


@dataclass(frozen=True)
class Cell:
    variant: str
    layer: int
    score_mode: str = "anti_pca_both_k15"

    @property
    def label(self) -> str:
        return f"{self.variant}|L{self.layer}|{self.score_mode}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument(
        "--cells",
        default="1-3:31,2-3-2_mem:31,2-3-1:30",
        help="Comma-separated variant:layer cells.",
    )
    parser.add_argument("--alphas", default="0,0.25,0.5,0.75,0.9,1")
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=200)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    cells = parse_cells(args.cells)
    alphas = [float(x) for x in args.alphas.split(",") if x.strip()]

    dump_dir = Path(args.dump_dir)
    manifest = offline.load_manifest(dump_dir)
    offline.validate_manifest(manifest)
    if not manifest.get("topk_logits", {}).get("enabled"):
        raise ValueError(f"Store does not have top-k logits enabled: {dump_dir}")
    records = offline.load_records(dump_dir, manifest, Path(args.data))
    buckets = offline.group_by_instance(records)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite and (json_path.exists() or md_path.exists()):
        raise FileExistsError(f"Output exists; pass --overwrite: {json_path}")

    print(f"records={len(records)} cells={[cell.label for cell in cells]} alphas={alphas}", flush=True)
    loaded = load_cells_and_logits(dump_dir, manifest, records, cells)

    rows = []
    for cell in cells:
        print(f"scoring {cell.label}", flush=True)
        dense_scores = dense_scores_for_cell(records, buckets, loaded[cell.label]["vectors"])
        dense_predictions = predictions_from_scores(records, buckets, dense_scores, top_k=args.top_k)
        rows.append(evaluate_row(cell, "dense_only", 1.0, dense_predictions, args.bootstrap_samples))

        logit_scores_by_method = sparse_scores_for_variant(
            records,
            buckets,
            token_ids=loaded[cell.label]["token_ids"],
            logit_values=loaded[cell.label]["logit_values"],
        )
        for method, logit_scores in logit_scores_by_method.items():
            logit_predictions = predictions_from_scores(records, buckets, logit_scores, top_k=args.top_k)
            rows.append(evaluate_row(cell, f"logits_{method}", 0.0, logit_predictions, args.bootstrap_samples))
            for alpha in alphas:
                if alpha in {0.0, 1.0}:
                    continue
                fused_scores = fuse_bucket_scores(records, buckets, dense_scores, logit_scores, alpha=alpha)
                fused_predictions = predictions_from_scores(records, buckets, fused_scores, top_k=args.top_k)
                rows.append(
                    evaluate_row(
                        cell,
                        f"dense_plus_{method}",
                        alpha,
                        fused_predictions,
                        args.bootstrap_samples,
                    )
                )
        gc.collect()

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "stage3_logits_sparse_fusion",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "cells": [cell.__dict__ for cell in cells],
            "alphas": alphas,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "topk_logits": manifest.get("topk_logits"),
        },
        "paper_reference": {
            "name": "PromptReps",
            "arxiv": "https://arxiv.org/abs/2404.18424",
            "github": "https://github.com/ielab/PromptReps",
            "note": "PromptReps uses single-word prompting plus last hidden states and next-token logits as dense+sparse retrieval representations.",
        },
        "rows": sorted(rows, key=lambda row: (row["summary"]["recall_all@5"], row["summary"]["ndcg_any@5"], row["summary"]["mrr"]), reverse=True),
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}", flush=True)
    print(f"wrote {md_path}", flush=True)
    return 0


def parse_cells(spec: str) -> list[Cell]:
    cells = []
    for part in spec.split(","):
        if not part.strip():
            continue
        variant, layer = part.split(":", 1)
        cells.append(Cell(variant.strip(), int(layer)))
    if not cells:
        raise ValueError("No cells selected.")
    return cells


def load_cells_and_logits(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    cells: list[Cell],
) -> dict[str, dict[str, np.ndarray]]:
    variant_indices = {variant: offline.index_of(manifest["prompt_variants"], variant, "variant") for variant in {cell.variant for cell in cells}}
    layer_indices = {cell.layer: offline.index_of(manifest["layers"], cell.layer, "layer") for cell in cells}
    position_index = offline.index_of(manifest["positions"], "last", "position")
    hidden_dim = int(manifest["hidden_dim"])
    topk = int(manifest["topk_logits"]["k"])

    output = {
        cell.label: {
            "vectors": np.empty((len(records), hidden_dim), dtype=np.float32),
            "token_ids": np.empty((len(records), topk), dtype=np.int32),
            "logit_values": np.empty((len(records), topk), dtype=np.float32),
        }
        for cell in cells
    }

    records_by_chunk: dict[str, list[tuple[int, offline.Stage2Record]]] = {}
    for row_index, record in enumerate(records):
        records_by_chunk.setdefault(record.chunk_file, []).append((row_index, record))

    for chunk_index, (chunk_file, rows) in enumerate(sorted(records_by_chunk.items()), start=1):
        path = dump_dir / chunk_file
        tensors = load_file(str(path), device="cpu")
        row_indices = np.fromiter((row_index for row_index, _record in rows), dtype=np.int64)
        chunk_rows = np.fromiter((record.chunk_index for _row_index, record in rows), dtype=np.int64)
        for cell in cells:
            variant_index = variant_indices[cell.variant]
            layer_index = layer_indices[cell.layer]
            output[cell.label]["vectors"][row_indices] = (
                tensors["states"][chunk_rows, variant_index, layer_index, position_index, :]
                .float()
                .numpy()
            )
            output[cell.label]["token_ids"][row_indices] = (
                tensors["top_logit_token_ids"][chunk_rows, variant_index, position_index, :]
                .int()
                .numpy()
            )
            output[cell.label]["logit_values"][row_indices] = (
                tensors["top_logit_values"][chunk_rows, variant_index, position_index, :]
                .float()
                .numpy()
            )
        if chunk_index == 1 or chunk_index == len(records_by_chunk) or chunk_index % 20 == 0:
            print(f"  loaded chunk {chunk_index}/{len(records_by_chunk)}", flush=True)
        del tensors, row_indices, chunk_rows
    return output


def dense_scores_for_cell(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    vectors: np.ndarray,
) -> dict[int, np.ndarray]:
    mean, pcs = offline.global_anti_pca(records, vectors, max_components=15)
    scores: dict[int, np.ndarray] = {}
    for instance_index, bucket in buckets.items():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        scores[instance_index] = offline.anti_pca_scores(
            vectors[bucket.query_index],
            vectors[bucket.candidate_indices],
            mean=mean,
            pcs=pcs[:15],
            mode="both",
        )
    return scores


def sparse_scores_for_variant(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    *,
    token_ids: np.ndarray,
    logit_values: np.ndarray,
) -> dict[str, dict[int, np.ndarray]]:
    weights = softmax_rows(logit_values)
    idf = token_idf(records, token_ids)
    token_maps = [dict(zip(ids.tolist(), row_weights.tolist(), strict=True)) for ids, row_weights in zip(token_ids, weights, strict=True)]

    outputs = {name: {} for name in ["overlap", "weighted_dot", "idf_overlap", "idf_weighted_dot"]}
    for instance_index, bucket in buckets.items():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        q_ids = token_ids[bucket.query_index]
        q_set = set(int(x) for x in q_ids.tolist())
        q_map = token_maps[bucket.query_index]
        method_scores = {name: [] for name in outputs}
        for candidate_index in bucket.candidate_indices:
            c_ids = token_ids[candidate_index]
            c_set = set(int(x) for x in c_ids.tolist())
            c_map = token_maps[candidate_index]
            shared = q_set.intersection(c_set)
            method_scores["overlap"].append(len(shared) / max(np.sqrt(len(q_set) * len(c_set)), 1.0))
            method_scores["weighted_dot"].append(sum(q_map[t] * c_map[t] for t in shared))
            method_scores["idf_overlap"].append(sum(float(idf.get(t, 0.0)) for t in shared))
            method_scores["idf_weighted_dot"].append(sum(float(idf.get(t, 0.0)) * q_map[t] * c_map[t] for t in shared))
        for name in outputs:
            outputs[name][instance_index] = np.asarray(method_scores[name], dtype=np.float64)
    return outputs


def softmax_rows(values: np.ndarray) -> np.ndarray:
    shifted = values - np.max(values, axis=1, keepdims=True)
    exp = np.exp(shifted)
    return (exp / np.maximum(np.sum(exp, axis=1, keepdims=True), 1e-12)).astype(np.float32, copy=False)


def token_idf(records: list[offline.Stage2Record], token_ids: np.ndarray) -> dict[int, float]:
    candidate_indices = [index for index, record in enumerate(records) if record.role != "query"]
    df: dict[int, int] = {}
    for index in candidate_indices:
        for token_id in set(int(x) for x in token_ids[index].tolist()):
            df[token_id] = df.get(token_id, 0) + 1
    n = len(candidate_indices)
    return {token_id: float(np.log((n + 1) / (count + 1)) + 1.0) for token_id, count in df.items()}


def fuse_bucket_scores(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    dense_scores: dict[int, np.ndarray],
    sparse_scores: dict[int, np.ndarray],
    *,
    alpha: float,
) -> dict[int, np.ndarray]:
    output = {}
    for instance_index, bucket in buckets.items():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        output[instance_index] = alpha * offline.zscore_1d(dense_scores[instance_index]) + (1.0 - alpha) * offline.zscore_1d(sparse_scores[instance_index])
    return output


def predictions_from_scores(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    score_rows: dict[int, np.ndarray],
    *,
    top_k: int,
) -> list[Prediction]:
    predictions = []
    for instance_index, bucket in buckets.items():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        scores = score_rows[instance_index]
        order = np.argsort(scores)[::-1]
        predictions.append(
            Prediction(
                question_id=query.question_id,
                retrieved_ids=[candidate_ids[int(index)] for index in order[:top_k]],
                gold_ids=list(bucket.gold_ids),
                is_abstention=query.is_abstention,
                has_target=query.has_target,
            )
        )
    return predictions


def evaluate_row(
    cell: Cell,
    method: str,
    alpha: float,
    predictions: list[Prediction],
    bootstrap_samples: int,
) -> dict[str, Any]:
    metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples, ks=(1, 3, 5, 10, 20, 50))
    session_metrics = offline.session_retrieval_metrics(predictions)
    rank_metrics = offline.rank_metrics(predictions)
    summary = {
        "recall_all@5": metrics["metrics"]["recall_all@5"]["mean"],
        "ndcg_any@5": metrics["metrics"]["ndcg_any@5"]["mean"],
        "session_hit@5": session_metrics["session_hit@5"],
        "mrr": rank_metrics["mrr"],
    }
    print(
        f"  {cell.label} {method} alpha={alpha:g} R@5={summary['recall_all@5']:.3f} "
        f"NDCG@5={summary['ndcg_any@5']:.3f} MRR={summary['mrr']:.3f}",
        flush=True,
    )
    return {
        "cell": cell.__dict__,
        "method": method,
        "alpha": alpha,
        "metrics": metrics,
        "session_metrics": session_metrics,
        "rank_metrics": rank_metrics,
        "summary": summary,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage 3 Sparse Logits Fusion Probe",
        "",
        f"- Created UTC: `{payload['created_utc']}`",
        f"- Dump: `{payload['inputs']['dump_dir']}`",
        f"- Reference: [PromptReps](https://arxiv.org/abs/2404.18424)",
        "",
        "| rank | cell | method | alpha | R@5 | NDCG@5 | MRR |",
        "|---:|---|---|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(payload["rows"], start=1):
        summary = row["summary"]
        cell = row["cell"]
        lines.append(
            f"| {index} | `{cell['variant']}@L{cell['layer']}` | `{row['method']}` | {row['alpha']:.2f} | "
            f"{summary['recall_all@5']:.3f} | {summary['ndcg_any@5']:.3f} | {summary['mrr']:.3f} |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
