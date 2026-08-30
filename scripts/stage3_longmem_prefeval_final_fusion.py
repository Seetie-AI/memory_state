"""Replay PrefEval-style K3 + embedding + BM25 fusion on LongMemEval.

This is an offline scorer. It does not run a model; it reads:

- a Stage 3 prompt-sweep vector store for the selected K3 prompts,
- an existing LongMemEval embedding cache, and
- the LongMemEval cleaned JSON for BM25 text and labels.

The main target is the PrefEval final-style configuration:

    K3 vector_average_component_norm 0.60
  + BM25 full-corpus score             0.10
  + external embedding score           0.30

All score fusion is per-query z-score fusion.
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

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
for path in [SCRIPTS, SRC]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import stage2_offline_analyze as offline
import stage3_prompt_fusion_analyze as fusion
from baselines.bm25 import BM25Retriever
from eval.longmemeval_metrics import Prediction, evaluate


DEFAULT_DUMP_DIR = ROOT / "tensors" / "stage3" / "prompt_sweep" / "prefeval_final_l30_lme100"
DEFAULT_EMBEDDING_DIR = (
    ROOT / "tensors" / "stage3" / "embedding_eval" / "qwen3_embedding_8b_dwq_subset0-100"
)
DEFAULT_DATA = ROOT / "data" / "longmemeval_s_cleaned.json"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "prompt_fusion_prefeval_replay"
DEFAULT_OUTPUT_PREFIX = "prefeval_l30_k3_longmemeval100"
DEFAULT_TOP_K = 50


@dataclass
class BucketScoreRow:
    question_id: str
    candidate_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool
    prompt_scores: list[np.ndarray]
    k3_scores: np.ndarray
    bm25_scores: np.ndarray
    embedding_scores: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP_DIR))
    parser.add_argument("--embedding-dir", default=str(DEFAULT_EMBEDDING_DIR))
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--shortlist-size", type=int, default=20)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()

    dump_dir = Path(args.dump_dir)
    embedding_dir = Path(args.embedding_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in (json_path, md_path) if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    manifest = offline.load_manifest(dump_dir)
    offline.validate_manifest(manifest)
    records = offline.load_records(dump_dir, manifest, Path(args.data))
    buckets = offline.group_by_instance(records)

    cells = [
        fusion.CellConfig("2-3-1_mark", 30, "anti_pca_both_k15", "keyword"),
        fusion.CellConfig("2-5_token", 30, "anti_pca_both_k15", "association"),
        fusion.CellConfig("2-8_emoji", 30, "anti_pca_both_k15", "emotion"),
    ]
    print(f"loading K3 cells from {dump_dir}")
    repr_by_label = build_vector_representations_np(dump_dir, manifest, records, cells)
    reprs = [repr_by_label[cell.label] for cell in cells]

    embedding_manifest = load_embedding_manifest(embedding_dir)
    print(f"scoring buckets={len(buckets)} embedding_dir={embedding_dir}")
    score_rows = build_score_rows(
        records,
        buckets,
        reprs,
        embedding_dir=embedding_dir,
        embedding_manifest=embedding_manifest,
    )

    experiments = build_experiments(shortlist_size=args.shortlist_size)
    rows = []
    for experiment in experiments:
        predictions = predictions_for_experiment(score_rows, experiment, top_k=args.top_k)
        metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=args.bootstrap_samples)
        session_metrics = offline.session_retrieval_metrics(predictions)
        rank_metrics = offline.rank_metrics(predictions)
        summary = summarize(metrics, session_metrics, rank_metrics)
        rows.append(
            {
                "name": experiment["name"],
                "description": experiment["description"],
                "phase": experiment["phase"],
                "weights": experiment.get("weights"),
                "shortlist_rule": experiment.get("shortlist_rule"),
                "metrics": metrics,
                "session_metrics": session_metrics,
                "rank_metrics": rank_metrics,
                "summary": summary,
            }
        )
        print(
            f"{experiment['name']}: "
            f"R@3={summary['recall_all@3']:.3f} "
            f"R@5={summary['recall_all@5']:.3f} "
            f"NDCG@3={summary['ndcg_any@3']:.3f} "
            f"MRR={summary['mrr']:.3f}"
        )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "stage3_longmem_prefeval_final_fusion",
        "inputs": {
            "dump_dir": str(dump_dir),
            "embedding_dir": str(embedding_dir),
            "data": str(Path(args.data)),
            "cells": [fusion.cell_to_json(cell) for cell in cells],
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "shortlist_size": args.shortlist_size,
            "n_records": len(records),
            "n_buckets": len(buckets),
        },
        "notes": [
            "K3 score uses vector_average_component_norm after per-cell anti_pca_both_k15.",
            "External embedding cache is Qwen3-Embedding-8B if the default path is used; no model is run here.",
            "Full-corpus rows rank every per-query LongMemEval round candidate.",
            "Shortlist rows use source top-k agreement only to choose the first-stage candidate set.",
        ],
        "rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


def build_experiments(shortlist_size: int) -> list[dict[str, Any]]:
    return [
        {
            "name": "k3_vector_average",
            "description": "K3 hidden-only vector_average_component_norm.",
            "phase": "baseline",
            "score_source": "k3",
        },
        {
            "name": "embedding_only",
            "description": "External embedding-only baseline.",
            "phase": "baseline",
            "score_source": "embedding",
        },
        {
            "name": "bm25_only",
            "description": "BM25-only baseline.",
            "phase": "baseline",
            "score_source": "bm25",
        },
        {
            "name": "k3_bm25_full_d0.75_b0.25",
            "description": "Full-corpus z-fusion: K3 0.75 + BM25 0.25.",
            "phase": "full_score_fusion",
            "weights": {"k3": 0.75, "bm25": 0.25, "embedding": 0.0},
        },
        {
            "name": "k3_embedding_full_d0.90_e0.10",
            "description": "Full-corpus z-fusion: K3 0.90 + embedding 0.10.",
            "phase": "full_score_fusion",
            "weights": {"k3": 0.90, "bm25": 0.0, "embedding": 0.10},
        },
        {
            "name": "prefeval_final_full_d0.60_b0.10_e0.30",
            "description": "PrefEval final-style full-corpus z-fusion: K3 0.60 + BM25 0.10 + embedding 0.30.",
            "phase": "full_score_fusion",
            "weights": {"k3": 0.60, "bm25": 0.10, "embedding": 0.30},
        },
        {
            "name": "mixed_ratio_full_basealpha0.85_base0.75_qwen0.25",
            "description": (
                "Full-corpus z-fusion using the exploratory second-stage ratio: "
                "0.75 * (K3 0.85 + BM25 0.15) + embedding 0.25."
            ),
            "phase": "full_score_fusion",
            "weights": {"k3": 0.6375, "bm25": 0.1125, "embedding": 0.25},
        },
        {
            "name": "prefeval_ratio_full_d0.70_b0.07_e0.23",
            "description": (
                "Full-corpus z-fusion with K3 0.70 + embedding 0.23 + BM25 0.07 "
                "(stored as dense/BM25/embedding order)."
            ),
            "phase": "full_score_fusion",
            "weights": {"k3": 0.70, "bm25": 0.07, "embedding": 0.23},
        },
        {
            "name": "prefeval_alt_full_d0.60_b0.30_e0.10",
            "description": "Full-corpus z-fusion with more BM25 and less embedding.",
            "phase": "full_score_fusion",
            "weights": {"k3": 0.60, "bm25": 0.30, "embedding": 0.10},
        },
        {
            "name": f"five_source_top{shortlist_size}_source_ge2_prefeval_final",
            "description": "Five-source top-k source_count>=2 shortlist, reranked with PrefEval final weights.",
            "phase": "shortlist_score_fusion",
            "weights": {"k3": 0.60, "bm25": 0.10, "embedding": 0.30},
            "shortlist_rule": {"kind": "source_ge", "min_sources": 2, "top_k": shortlist_size},
        },
        {
            "name": f"source_ge3_plus_embedding_top{shortlist_size}_d0.90_e0.10",
            "description": "Prompt/BM25 source_count>=3 plus embedding top-k, reranked by K3 0.90 + embedding 0.10.",
            "phase": "shortlist_score_fusion",
            "weights": {"k3": 0.90, "bm25": 0.0, "embedding": 0.10},
            "shortlist_rule": {
                "kind": "source_ge_plus_embedding",
                "min_sources": 3,
                "top_k": shortlist_size,
            },
        },
    ]


def build_score_rows(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    reprs: list[fusion.VectorRepr],
    *,
    embedding_dir: Path,
    embedding_manifest: dict[str, Any],
) -> list[BucketScoreRow]:
    output: list[BucketScoreRow] = []
    embedding_by_instance = {
        int(item["instance_index"]): item for item in embedding_manifest.get("instances", [])
    }
    for instance_index, bucket in buckets.items():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query_record = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        if len(candidate_ids) != len(candidate_records):
            raise ValueError(f"Missing candidate_id in instance {instance_index}.")

        prompt_scores = [single_prompt_scores(bucket, repr_) for repr_ in reprs]
        k3_scores = fusion.score_vector_average(bucket, reprs, component_normalize=True)
        bm25_scores = bm25_scores_for_bucket(query_record, candidate_records)
        embedding_scores = embedding_scores_for_bucket(
            embedding_dir,
            embedding_by_instance[instance_index],
            candidate_ids,
        )
        output.append(
            BucketScoreRow(
                question_id=query_record.question_id,
                candidate_ids=candidate_ids,
                gold_ids=list(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
                prompt_scores=prompt_scores,
                k3_scores=k3_scores,
                bm25_scores=bm25_scores,
                embedding_scores=embedding_scores,
            )
        )
    return output


def build_vector_representations_np(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    cells: list[fusion.CellConfig],
) -> dict[str, fusion.VectorRepr]:
    """Build prompt vector representations without requiring a Metal device."""
    output: dict[str, fusion.VectorRepr] = {}
    for cell in cells:
        print(f"phase4 repr {cell.label}")
        vectors = load_vector_matrix_torch_cpu(
            dump_dir,
            manifest,
            records,
            variant=cell.variant,
            layer=cell.layer,
            position="last",
        )
        output[cell.label] = fusion.build_persistable_repr(cell, vectors, records)
        del vectors
        gc.collect()
    return output


def load_vector_matrix_torch_cpu(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    *,
    variant: str,
    layer: int,
    position: str,
) -> np.ndarray:
    """Load one vector slice through torch CPU so bf16 safetensors work headlessly."""
    from safetensors.torch import load_file

    variant_index = offline.index_of(manifest["prompt_variants"], variant, "variant")
    layer_index = offline.index_of(manifest["layers"], layer, "layer")
    position_index = offline.index_of(manifest["positions"], position, "position")
    hidden_dim = int(manifest["hidden_dim"])
    output = np.empty((len(records), hidden_dim), dtype=np.float32)

    records_by_chunk: dict[str, list[tuple[int, offline.Stage2Record]]] = {}
    for row_index, record in enumerate(records):
        records_by_chunk.setdefault(record.chunk_file, []).append((row_index, record))

    for chunk_file, rows in sorted(records_by_chunk.items()):
        states = load_file(str(dump_dir / chunk_file), device="cpu")["states"]
        for row_index, record in rows:
            output[row_index] = (
                states[record.chunk_index, variant_index, layer_index, position_index, :]
                .float()
                .numpy()
            )
        del states
    if not np.all(np.isfinite(output)):
        raise ValueError(f"Non-finite vector in {variant}|layer{layer}|{position}.")
    return output


def single_prompt_scores(bucket: offline.InstanceBucket, repr_: fusion.VectorRepr) -> np.ndarray:
    query = offline.normalize(repr_.query_vectors[bucket.query_index])
    candidates = offline.normalize(repr_.candidate_vectors[bucket.candidate_indices])
    return candidates @ query


def bm25_scores_for_bucket(
    query_record: offline.Stage2Record,
    candidate_records: list[offline.Stage2Record],
) -> np.ndarray:
    texts = [record.text for record in candidate_records]
    retriever = BM25Retriever().fit(texts)
    scores = np.zeros(len(candidate_records), dtype=np.float64)
    for local_rank, score in retriever.query(query_record.text, top_k=len(texts)):
        scores[int(local_rank)] = float(score)
    return scores


def embedding_scores_for_bucket(
    embedding_dir: Path,
    metadata: dict[str, Any],
    candidate_ids: list[str],
) -> np.ndarray:
    stored_ids = [str(value) for value in metadata.get("candidate_ids", [])]
    stored_index = {candidate_id: index for index, candidate_id in enumerate(stored_ids)}
    missing = [candidate_id for candidate_id in candidate_ids if candidate_id not in stored_index]
    if missing:
        raise ValueError(
            f"Embedding cache lacks candidate IDs for instance {metadata.get('instance_index')}: "
            f"{missing[:5]}"
        )
    arrays = np.load(embedding_dir / str(metadata["file"]))
    candidate_embeddings = np.asarray(arrays["candidate_embeddings"], dtype=np.float32)
    query_embedding = np.asarray(arrays["query_embedding"], dtype=np.float32)
    if query_embedding.ndim != 1:
        raise ValueError(f"Expected 1D query embedding, got {query_embedding.shape}")
    aligned_indices = [stored_index[candidate_id] for candidate_id in candidate_ids]
    return query_embedding @ candidate_embeddings[aligned_indices].T


def predictions_for_experiment(
    score_rows: list[BucketScoreRow],
    experiment: dict[str, Any],
    *,
    top_k: int,
) -> list[Prediction]:
    predictions = []
    for row in score_rows:
        scores = fused_scores(row, experiment)
        allowed = candidate_set(row, experiment)
        if allowed is None:
            order = np.argsort(scores)[::-1]
        else:
            allowed_order = allowed[np.argsort(scores[allowed])[::-1]]
            allowed_set = {int(index) for index in allowed_order}
            tail = [int(index) for index in np.argsort(scores)[::-1] if int(index) not in allowed_set]
            order = np.asarray([int(index) for index in allowed_order] + tail, dtype=np.int64)
        predictions.append(
            Prediction(
                question_id=row.question_id,
                retrieved_ids=[row.candidate_ids[int(index)] for index in order[:top_k]],
                gold_ids=row.gold_ids,
                is_abstention=row.is_abstention,
                has_target=row.has_target,
            )
        )
    return predictions


def fused_scores(row: BucketScoreRow, experiment: dict[str, Any]) -> np.ndarray:
    if "score_source" in experiment:
        source = experiment["score_source"]
        if source == "k3":
            return np.asarray(row.k3_scores, dtype=np.float64)
        if source == "embedding":
            return np.asarray(row.embedding_scores, dtype=np.float64)
        if source == "bm25":
            return np.asarray(row.bm25_scores, dtype=np.float64)
        raise ValueError(f"Unknown score source: {source}")
    weights = experiment["weights"]
    return (
        float(weights.get("k3", 0.0)) * offline.zscore_1d(row.k3_scores)
        + float(weights.get("bm25", 0.0)) * offline.zscore_1d(row.bm25_scores)
        + float(weights.get("embedding", 0.0)) * offline.zscore_1d(row.embedding_scores)
    )


def candidate_set(row: BucketScoreRow, experiment: dict[str, Any]) -> np.ndarray | None:
    rule = experiment.get("shortlist_rule")
    if not rule:
        return None
    top_k = int(rule["top_k"])
    source_scores = list(row.prompt_scores) + [row.bm25_scores, row.embedding_scores]
    top_sets = []
    for scores in source_scores:
        order = np.argsort(scores)[::-1][: min(top_k, len(scores))]
        top_sets.append({int(index) for index in order})

    if rule["kind"] == "source_ge":
        counts = np.zeros(len(row.candidate_ids), dtype=np.int16)
        for top_set in top_sets:
            for index in top_set:
                counts[index] += 1
        allowed = np.flatnonzero(counts >= int(rule["min_sources"]))
    elif rule["kind"] == "source_ge_plus_embedding":
        prompt_bm25_sets = top_sets[:4]
        counts = np.zeros(len(row.candidate_ids), dtype=np.int16)
        for top_set in prompt_bm25_sets:
            for index in top_set:
                counts[index] += 1
        embedding_top = np.asarray(sorted(top_sets[4]), dtype=np.int64)
        source_ge = np.flatnonzero(counts >= int(rule["min_sources"]))
        allowed = np.unique(np.concatenate([source_ge, embedding_top]))
    else:
        raise ValueError(f"Unknown shortlist rule: {rule}")

    if len(allowed) == 0:
        return None
    return np.asarray(allowed, dtype=np.int64)


def load_embedding_manifest(embedding_dir: Path) -> dict[str, Any]:
    manifest_path = embedding_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing embedding manifest: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def summarize(
    metrics: dict[str, Any],
    session_metrics: dict[str, float],
    rank_metrics: dict[str, Any],
) -> dict[str, Any]:
    values = metrics["metrics"]
    output = {
        key: values[key]["mean"]
        for key in [
            "recall_all@1",
            "ndcg_any@1",
            "recall_all@3",
            "ndcg_any@3",
            "recall_all@5",
            "ndcg_any@5",
            "recall_all@10",
            "ndcg_any@10",
            "recall_all@50",
            "ndcg_any@50",
        ]
    }
    output["mrr"] = rank_metrics["mrr"]
    output["session_hit@5"] = session_metrics["session_hit@5"]
    output["n_scored"] = metrics["n_scored"]
    return output


def render_markdown(payload: dict[str, Any]) -> str:
    rows = sorted(
        payload["rows"],
        key=lambda row: (
            row["summary"]["recall_all@3"],
            row["summary"]["ndcg_any@3"],
            row["summary"]["recall_all@5"],
        ),
        reverse=True,
    )
    lines = [
        "# PrefEval final replay on LongMemEval",
        "",
        "Offline replay of the PrefEval K3 setup on LongMemEval-S round candidates.",
        "",
        "| rank | config | phase | R@1 | R@3 | NDCG@3 | R@5 | NDCG@5 | R@50 | MRR | n |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(rows, start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | `{row['name']}` | {row['phase']} | "
            f"{summary['recall_all@1']:.3f} | {summary['recall_all@3']:.3f} | "
            f"{summary['ndcg_any@3']:.3f} | {summary['recall_all@5']:.3f} | "
            f"{summary['ndcg_any@5']:.3f} | {summary['recall_all@50']:.3f} | "
            f"{summary['mrr']:.3f} | {summary['n_scored']} |"
        )
    lines.extend(["", "## Inputs", ""])
    lines.append(f"- dump_dir: `{payload['inputs']['dump_dir']}`")
    lines.append(f"- embedding_dir: `{payload['inputs']['embedding_dir']}`")
    lines.append(f"- cells: {', '.join(cell['variant'] for cell in payload['inputs']['cells'])}")
    lines.append(f"- elapsed: {payload['elapsed_seconds']:.1f}s")
    lines.append("")
    return "\n".join(lines)


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


if __name__ == "__main__":
    raise SystemExit(main())
