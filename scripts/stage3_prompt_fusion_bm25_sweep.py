"""BM25 score-fusion sweep over Stage 3 prompt-vector fusion configs.

This script is intentionally separate from `stage3_prompt_fusion_analyze.py`.
Prompt fusion builds vector representations; BM25 is a score-level overlay that
adds lexical evidence after vector scores are available. Keeping it separate
keeps the vector-fusion script focused and makes the BM25 scope explicit.

By default BM25 is fused over the full per-instance candidate set. Then
alpha=0.0 is a true BM25 baseline and alpha=1.0 is exactly vector-only, which
is the cleanest product-facing interpretation. The optional
`--bm25-scope vector_top50` reproduces the Stage 2 style and the common
deployment pattern "vector shortlist first, lexical rerank/fuse inside it."
`vector_top20` is the tighter shortlist variant.

Fusion uses the Stage 2 convention:

    fused = alpha * zscore(vector_scores) + (1 - alpha) * zscore(bm25_scores)

No quantization is tested here. The user selected a paged-memory design where
K=3 bf16 prompt vectors are about 24KB per memory page, which is acceptable for
the current storage target; this sweep only asks whether cheap BM25 score
fusion adds useful lexical signal to the chosen Stage 3 prompt-vector configs.
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


DEFAULT_DUMP_DIR = fusion.DEFAULT_DUMP_DIR
DEFAULT_DATA = fusion.DEFAULT_DATA
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "prompt_fusion_bm25"
DEFAULT_OUTPUT_PREFIX = "findings"
DEFAULT_TOP_K = 50
DEFAULT_ALPHAS = [0.0, 0.25, 0.5, 0.75, 1.0]
CHECK_TOL = 1e-6


@dataclass(frozen=True)
class ExpectedMetrics:
    recall_all_at_5: float
    ndcg_any_at_5: float
    mrr: float


@dataclass(frozen=True)
class FusionConfig:
    name: str
    description: str
    cells: tuple[fusion.CellConfig, ...]
    scorer: str
    expected_alpha1: ExpectedMetrics


@dataclass
class BucketScores:
    question_id: str
    candidate_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool
    vector_scores: np.ndarray
    bm25_scores: np.ndarray


def cell(variant: str, layer: int, score_mode: str, family: str) -> fusion.CellConfig:
    return fusion.CellConfig(variant, layer, score_mode, family)


CONFIGS: list[FusionConfig] = [
    FusionConfig(
        name="concat_k3_norm_weighted_userword_tag_assoc",
        description="NDCG winner: vertical concat, raw component norms retained as implicit prompt weights.",
        cells=(
            cell("2-4-1_user_word", 30, "anti_pca_both_k15", "persona"),
            cell("1-3", 31, "anti_pca_both_k15", "tag"),
            cell("2-5", 29, "query_only_anti_pca_k2", "association"),
        ),
        scorer="vertical_concat_norm_weighted",
        expected_alpha1=ExpectedMetrics(
            recall_all_at_5=0.7659574468085106,
            ndcg_any_at_5=0.8061935253073595,
            mrr=0.839450354609929,
        ),
    ),
    FusionConfig(
        name="avg_k2_component_norm_l30_userword_tag",
        description="Product-friendly single-vector candidate: component-normalized average at uniform layer 30.",
        cells=(
            cell("2-4-1_user_word", 30, "anti_pca_both_k15", "persona"),
            cell("1-3", 30, "anti_pca_both_k15", "tag"),
        ),
        scorer="vector_average_component_norm",
        expected_alpha1=ExpectedMetrics(
            recall_all_at_5=0.776595744680851,
            ndcg_any_at_5=0.7879640759095615,
            mrr=0.8199387491940683,
        ),
    ),
    FusionConfig(
        name="single_1-3_l31_both",
        description="Best single-prompt NDCG cell.",
        cells=(cell("1-3", 31, "anti_pca_both_k15", "tag"),),
        scorer="single_vector",
        expected_alpha1=ExpectedMetrics(
            recall_all_at_5=0.7553191489361702,
            ndcg_any_at_5=0.7837910207130874,
            mrr=0.8054282596835787,
        ),
    ),
    FusionConfig(
        name="single_2-3-2_mem_l31_both",
        description="Best single-prompt R@5 memory-key cell.",
        cells=(cell("2-3-2_mem", 31, "anti_pca_both_k15", "mem-key"),),
        scorer="single_vector",
        expected_alpha1=ExpectedMetrics(
            recall_all_at_5=0.7659574468085106,
            ndcg_any_at_5=0.7570274420948752,
            mrr=0.7800067544748396,
        ),
    ),
    FusionConfig(
        name="single_P0_l30_both",
        description="Stage 2 anchor prompt.",
        cells=(cell("P0", 30, "anti_pca_both_k15", "anchor"),),
        scorer="single_vector",
        expected_alpha1=ExpectedMetrics(
            recall_all_at_5=0.7553191489361702,
            ndcg_any_at_5=0.7790176206197672,
            mrr=0.8144123606889564,
        ),
    ),
]

CONFIG_BY_NAME = {config.name: config for config in CONFIGS}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--configs", default="all", help="Comma-separated config names or 'all'.")
    parser.add_argument("--alphas", default=",".join(str(alpha) for alpha in DEFAULT_ALPHAS))
    parser.add_argument("--bm25-scope", choices=["full", "vector_top50", "vector_top20"], default="full")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--limit-configs", type=int, default=None)
    parser.add_argument("--limit-alphas", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()

    configs = parse_configs(args.configs)
    if args.limit_configs is not None:
        configs = configs[: args.limit_configs]
    alphas = parse_float_list(args.alphas)
    if args.limit_alphas is not None:
        alphas = alphas[: args.limit_alphas]
    if not configs:
        raise ValueError("No configs selected.")
    if not alphas:
        raise ValueError("No alphas selected.")

    dump_dir = Path(args.dump_dir)
    manifest = offline.load_manifest(dump_dir)
    offline.validate_manifest(manifest)
    records = offline.load_records(dump_dir, manifest, Path(args.data))
    buckets = offline.group_by_instance(records)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in [json_path, md_path] if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    print(
        f"records={len(records)} configs={len(configs)} alphas={alphas} "
        f"bm25_scope={args.bm25_scope} bootstrap={args.bootstrap_samples}"
    )

    rows = []
    config_timings = []
    for index, config in enumerate(configs, start=1):
        config_started = time.perf_counter()
        print(f"[{index}/{len(configs)}] {config.name}")
        reprs = build_config_reprs(dump_dir, manifest, records, config)
        score_rows = score_config_records(records, buckets, config, reprs, bm25_scope=args.bm25_scope)
        for alpha in alphas:
            predictions = predictions_from_scores(score_rows, alpha=alpha, top_k=args.top_k, scope=args.bm25_scope)
            metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=args.bootstrap_samples)
            session_metrics = offline.session_retrieval_metrics(predictions)
            rank_metrics = offline.rank_metrics(predictions)
            summary = summarize_metrics(metrics, session_metrics, rank_metrics)
            row = {
                "config": config_to_json(config),
                "alpha": alpha,
                "bm25_scope": args.bm25_scope,
                "metrics": metrics,
                "session_metrics": session_metrics,
                "rank_metrics": rank_metrics,
                "summary": summary,
            }
            validate_alpha1(config, alpha, summary)
            rows.append(row)
            print(
                f"  alpha={alpha:g} R@5={summary['recall_all@5']:.3f} "
                f"NDCG@5={summary['ndcg_any@5']:.3f} MRR={summary['mrr']:.3f}"
            )
        elapsed = time.perf_counter() - config_started
        config_timings.append({"config": config.name, "elapsed_seconds": elapsed})
        print(f"  done in {format_seconds(elapsed)}")
        del reprs, score_rows
        gc.collect()

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "stage3_prompt_fusion_bm25_sweep",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "configs": [config.name for config in configs],
            "alphas": alphas,
            "bm25_scope": args.bm25_scope,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
        },
        "design_notes": [
            "BM25 is a score-level overlay over Stage 3 prompt-vector configs.",
            "Default full scope makes alpha=0.0 a true BM25 baseline.",
            "vector_top50 scope is retained for Stage 2 anchor comparison and deployment-style shortlist reranking.",
            "Quantization is intentionally excluded because paged memory makes bf16 K=3 storage acceptable for now.",
        ],
        "rows": rows,
        "config_timings": config_timings,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(f"elapsed {format_seconds(payload['elapsed_seconds'])}")
    return 0


def parse_configs(value: str) -> list[FusionConfig]:
    if value.strip() == "all":
        return list(CONFIGS)
    names = [item.strip() for item in value.split(",") if item.strip()]
    missing = [name for name in names if name not in CONFIG_BY_NAME]
    if missing:
        raise ValueError(f"Unknown configs: {missing}; available={sorted(CONFIG_BY_NAME)}")
    return [CONFIG_BY_NAME[name] for name in names]


def parse_float_list(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def build_config_reprs(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    config: FusionConfig,
) -> list[fusion.VectorRepr]:
    repr_by_label = fusion.build_vector_representations(dump_dir, manifest, records, list(config.cells))
    return [repr_by_label[cell.label] for cell in config.cells]


def score_config_records(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    config: FusionConfig,
    reprs: list[fusion.VectorRepr],
    *,
    bm25_scope: str,
) -> list[BucketScores]:
    output = []
    for bucket in buckets.values():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query_record = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        if len(candidate_ids) != len(candidate_records):
            raise ValueError(f"Missing candidate_id in instance {query_record.instance_index}.")
        vector_scores = score_config_bucket(config, bucket, reprs)
        bm25_scores = bm25_scores_for_bucket(query_record, candidate_records, vector_scores, scope=bm25_scope)
        output.append(
            BucketScores(
                question_id=query_record.question_id,
                candidate_ids=candidate_ids,
                gold_ids=list(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
                vector_scores=vector_scores,
                bm25_scores=bm25_scores,
            )
        )
    return output


def score_config_bucket(
    config: FusionConfig,
    bucket: offline.InstanceBucket,
    reprs: list[fusion.VectorRepr],
) -> np.ndarray:
    if config.scorer == "vertical_concat_norm_weighted":
        return fusion.score_vertical_concat(bucket, reprs, component_normalize=False)
    if config.scorer == "vector_average_component_norm":
        return fusion.score_vector_average(bucket, reprs, component_normalize=True)
    if config.scorer == "single_vector":
        if len(reprs) != 1:
            raise ValueError(f"single_vector config expected one repr, got {len(reprs)}")
        repr_ = reprs[0]
        query = fusion.offline.normalize(repr_.query_vectors[bucket.query_index])
        candidates = fusion.offline.normalize(repr_.candidate_vectors[bucket.candidate_indices])
        return candidates @ query
    raise ValueError(f"Unsupported scorer for {config.name}: {config.scorer}")


def bm25_scores_for_bucket(
    query_record: offline.Stage2Record,
    candidate_records: list[offline.Stage2Record],
    vector_scores: np.ndarray,
    *,
    scope: str,
) -> np.ndarray:
    scores = np.zeros(len(candidate_records), dtype=np.float64)
    if scope == "full":
        local_indices = list(range(len(candidate_records)))
    elif scope.startswith("vector_top"):
        shortlist_k = parse_vector_scope_k(scope)
        local_indices = [
            int(index)
            for index in np.argsort(vector_scores)[::-1][: min(shortlist_k, len(candidate_records))]
        ]
    else:
        raise ValueError(f"Unsupported BM25 scope: {scope}")

    texts = [candidate_records[index].text for index in local_indices]
    retriever = BM25Retriever().fit(texts)
    for local_rank, score in retriever.query(query_record.text, top_k=len(texts)):
        scores[local_indices[int(local_rank)]] = float(score)
    return scores


def predictions_from_scores(
    rows: list[BucketScores],
    *,
    alpha: float,
    top_k: int,
    scope: str,
) -> list[Prediction]:
    predictions = []
    for row in rows:
        if scope == "full":
            fused = alpha * offline.zscore_1d(row.vector_scores) + (1.0 - alpha) * offline.zscore_1d(row.bm25_scores)
            order = np.argsort(fused)[::-1]
        elif scope.startswith("vector_top"):
            shortlist_k = parse_vector_scope_k(scope)
            vector_order = np.argsort(row.vector_scores)[::-1]
            top_indices = vector_order[: min(shortlist_k, len(vector_order))]
            fused_top = (
                alpha * offline.zscore_1d(row.vector_scores[top_indices])
                + (1.0 - alpha) * offline.zscore_1d(row.bm25_scores[top_indices])
            )
            reranked_top = top_indices[np.argsort(fused_top)[::-1]]
            top_set = {int(index) for index in top_indices}
            tail = [int(index) for index in vector_order if int(index) not in top_set]
            order = np.asarray([int(index) for index in reranked_top] + tail, dtype=np.int64)
        else:
            raise ValueError(f"Unsupported BM25 scope: {scope}")
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


def parse_vector_scope_k(scope: str) -> int:
    prefix = "vector_top"
    if not scope.startswith(prefix):
        raise ValueError(f"Not a vector shortlist scope: {scope}")
    return int(scope[len(prefix) :])


def summarize_metrics(
    metrics: dict[str, Any],
    session_metrics: dict[str, float],
    rank_metrics: dict[str, Any],
) -> dict[str, Any]:
    values = metrics["metrics"]
    return {
        "recall_all@3": values["recall_all@3"]["mean"],
        "ndcg_any@3": values["ndcg_any@3"]["mean"],
        "recall_all@5": values["recall_all@5"]["mean"],
        "ndcg_any@5": values["ndcg_any@5"]["mean"],
        "session_hit@5": session_metrics["session_hit@5"],
        "session_recall_all@5": session_metrics["session_recall_all@5"],
        "mrr": rank_metrics["mrr"],
        "n_scored": metrics["n_scored"],
    }


def validate_alpha1(config: FusionConfig, alpha: float, summary: dict[str, Any]) -> None:
    if abs(alpha - 1.0) > 1e-12:
        return
    expected = config.expected_alpha1
    checks = [
        ("recall_all@5", summary["recall_all@5"], expected.recall_all_at_5),
        ("ndcg_any@5", summary["ndcg_any@5"], expected.ndcg_any_at_5),
        ("mrr", summary["mrr"], expected.mrr),
    ]
    bad = [
        f"{name}: actual={actual:.12f} expected={expected_value:.12f}"
        for name, actual, expected_value in checks
        if abs(float(actual) - float(expected_value)) > CHECK_TOL
    ]
    if bad:
        joined = "; ".join(bad)
        raise ValueError(f"alpha=1.0 self-check failed for {config.name}: {joined}")


def config_to_json(config: FusionConfig) -> dict[str, Any]:
    return {
        "name": config.name,
        "description": config.description,
        "scorer": config.scorer,
        "cells": [fusion.cell_to_json(cell) for cell in config.cells],
        "expected_alpha1": {
            "recall_all@5": config.expected_alpha1.recall_all_at_5,
            "ndcg_any@5": config.expected_alpha1.ndcg_any_at_5,
            "mrr": config.expected_alpha1.mrr,
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = sorted(
        payload["rows"],
        key=lambda row: (
            row["summary"]["recall_all@5"],
            row["summary"]["ndcg_any@5"],
            row["summary"]["mrr"],
        ),
        reverse=True,
    )
    lines = [
        "# Stage 3 prompt fusion + BM25 sweep",
        "",
        "This run adds BM25 score fusion over saved Stage 3 prompt-vector configs.",
        "",
        f"BM25 scope: `{payload['inputs']['bm25_scope']}`.",
        "",
        "| rank | config | alpha | R@5 | NDCG@5 | MRR | session_hit@5 | n |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(rows, start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | `{row['config']['name']}` | {row['alpha']:.2f} | "
            f"{summary['recall_all@5']:.3f} | {summary['ndcg_any@5']:.3f} | "
            f"{summary['mrr']:.3f} | {summary['session_hit@5']:.3f} | {summary['n_scored']} |"
        )
    lines.extend(["", "## Alpha=1.0 Self-Checks", ""])
    lines.append("All alpha=1.0 rows are checked against hard-coded vector-only baselines at 1e-6 tolerance.")
    lines.extend(["", "## Inputs", ""])
    lines.append(f"- configs: {', '.join(payload['inputs']['configs'])}")
    lines.append(f"- alphas: {payload['inputs']['alphas']}")
    lines.append(f"- elapsed: {format_seconds(payload['elapsed_seconds'])}")
    lines.append("")
    return "\n".join(lines)


def format_seconds(seconds: float) -> str:
    total = int(round(seconds))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}h{minutes:02d}m{secs:02d}s"
    if minutes:
        return f"{minutes}m{secs:02d}s"
    return f"{secs}s"


if __name__ == "__main__":
    raise SystemExit(main())
