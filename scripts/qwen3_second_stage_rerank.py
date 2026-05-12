"""Temporary Qwen3-Embedding-8B second-stage rerank tests.

This reuses existing 0-100 Qwen3 embedding tensors and the Stage 3 prompt
fusion tensors. It tests two questions:

1. Does Qwen3 score improve reranking inside the prompt3+BM25 source>=2 set?
2. Does Qwen3 top20 help as a fifth candidate-source?
"""

from __future__ import annotations

import argparse
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
import stage3_prompt_fusion_bm25_sweep as bm25_sweep
import tmp_union_top20_prompt_bm25_fusion as union_helpers
from eval.longmemeval_metrics import Prediction, evaluate


DEFAULT_CONFIG = "concat_k3_norm_weighted_userword_tag_assoc"
DEFAULT_QWEN_DIR = ROOT / "tensors" / "stage3" / "embedding_eval" / "qwen3_embedding_8b_dwq_subset0-100"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "prompt_fusion_bm25"
DEFAULT_OUTPUT_PREFIX = "tmp_qwen3_second_stage"
DEFAULT_BASE_ALPHAS = [0.5, 0.65, 0.75, 0.85]
DEFAULT_BASE_WEIGHTS = [0.0, 0.25, 0.5, 0.75, 1.0]


@dataclass
class BaseBucketScores:
    instance_index: int
    question_id: str
    candidate_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool
    prompt_scores: list[np.ndarray]
    concat_scores: np.ndarray
    bm25_scores: np.ndarray
    qwen_scores: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(fusion.DEFAULT_DUMP_DIR))
    parser.add_argument("--qwen-dir", default=str(DEFAULT_QWEN_DIR))
    parser.add_argument("--data", default=str(fusion.DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--base-alphas", default=",".join(str(alpha) for alpha in DEFAULT_BASE_ALPHAS))
    parser.add_argument("--base-weights", default=",".join(str(weight) for weight in DEFAULT_BASE_WEIGHTS))
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    config = bm25_sweep.CONFIG_BY_NAME[args.config]
    base_alphas = parse_float_list(args.base_alphas)
    base_weights = parse_float_list(args.base_weights)

    dump_dir = Path(args.dump_dir)
    qwen_dir = Path(args.qwen_dir)
    manifest = offline.load_manifest(dump_dir)
    offline.validate_manifest(manifest)
    records = offline.load_records(dump_dir, manifest, Path(args.data))
    buckets = offline.group_by_instance(records)
    qwen_manifest = load_qwen_manifest(qwen_dir)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in [json_path, md_path] if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    print(
        f"records={len(records)} config={config.name} qwen_dir={qwen_dir} "
        f"base_alphas={base_alphas} base_weights={base_weights}"
    )
    reprs = union_helpers.build_config_reprs_cpu(dump_dir, manifest, records, config)
    base_rows = build_base_rows(records, buckets, config, reprs, qwen_dir, qwen_manifest)

    strategies = [
        ("prompt3_bm25_top20", "Qwen3 is rerank score only; sources are three prompts + BM25 top20."),
        ("prompt3_bm25_qwen_top20", "Qwen3 is both rerank score and a fifth top20 source."),
    ]
    result_rows = []
    for strategy, description in strategies:
        for base_alpha in base_alphas:
            for base_weight in base_weights:
                predictions = predictions_for_strategy(
                    base_rows,
                    strategy=strategy,
                    base_alpha=base_alpha,
                    base_weight=base_weight,
                    top_k=args.top_k,
                )
                result_rows.append(
                    evaluate_row(
                        strategy=strategy,
                        strategy_description=description,
                        base_alpha=base_alpha,
                        base_weight=base_weight,
                        predictions=predictions,
                        bootstrap_samples=args.bootstrap_samples,
                    )
                )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "tmp_qwen3_second_stage_rerank",
        "inputs": {
            "dump_dir": str(dump_dir),
            "qwen_dir": str(qwen_dir),
            "data": str(Path(args.data)),
            "config": bm25_sweep.config_to_json(config),
            "base_alphas": base_alphas,
            "base_weights": base_weights,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
        },
        "strategy_oracle_summary": {
            strategy: strategy_oracle_summary(base_rows, strategy=strategy)
            for strategy, _description in strategies
        },
        "rows": result_rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


def load_qwen_manifest(qwen_dir: Path) -> dict[str, Any]:
    path = qwen_dir / "manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing Qwen embedding manifest: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_base_rows(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    config: bm25_sweep.FusionConfig,
    reprs: list[fusion.VectorRepr],
    qwen_dir: Path,
    qwen_manifest: dict[str, Any],
) -> list[BaseBucketScores]:
    qwen_by_instance = {
        int(item["instance_index"]): item
        for item in qwen_manifest.get("instances", [])
    }
    output = []
    for bucket in buckets.values():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query_record = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        if len(candidate_ids) != len(candidate_records):
            raise ValueError(f"Missing candidate_id in instance {query_record.instance_index}.")
        prompt_scores = [union_helpers.score_single_repr(bucket, repr_) for repr_ in reprs]
        concat_scores = bm25_sweep.score_config_bucket(config, bucket, reprs)
        bm25_scores = union_helpers.full_bm25_scores(query_record, candidate_records)
        qwen_scores = qwen_scores_for_instance(
            qwen_dir,
            qwen_by_instance,
            int(query_record.instance_index),
            candidate_ids,
        )
        output.append(
            BaseBucketScores(
                instance_index=int(query_record.instance_index),
                question_id=query_record.question_id,
                candidate_ids=candidate_ids,
                gold_ids=list(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
                prompt_scores=prompt_scores,
                concat_scores=concat_scores,
                bm25_scores=bm25_scores,
                qwen_scores=qwen_scores,
            )
        )
    return output


def qwen_scores_for_instance(
    qwen_dir: Path,
    qwen_by_instance: dict[int, dict[str, Any]],
    instance_index: int,
    candidate_ids: list[str],
) -> np.ndarray:
    if instance_index not in qwen_by_instance:
        raise KeyError(f"Qwen embedding store missing instance {instance_index}.")
    meta = qwen_by_instance[instance_index]
    qwen_candidate_ids = list(meta["candidate_ids"])
    with np.load(qwen_dir / meta["file"]) as data:
        candidates = np.asarray(data["candidate_embeddings"], dtype=np.float32)
        query = np.asarray(data["query_embedding"], dtype=np.float32)
    raw_scores = candidates @ query
    if qwen_candidate_ids == candidate_ids:
        return raw_scores.astype(np.float64, copy=False)
    position = {candidate_id: index for index, candidate_id in enumerate(qwen_candidate_ids)}
    missing = [candidate_id for candidate_id in candidate_ids if candidate_id not in position]
    if missing:
        raise ValueError(f"Qwen candidates missing ids for instance {instance_index}: {missing[:5]}")
    return np.asarray([raw_scores[position[candidate_id]] for candidate_id in candidate_ids], dtype=np.float64)


def predictions_for_strategy(
    rows: list[BaseBucketScores],
    *,
    strategy: str,
    base_alpha: float,
    base_weight: float,
    top_k: int,
) -> list[Prediction]:
    predictions = []
    for row in rows:
        source_sets = source_sets_for_strategy(row, strategy)
        counts = source_count_map(source_sets)
        kept = np.asarray(
            [index for index, count in counts.items() if count >= 2],
            dtype=np.int64,
        )
        if len(kept) == 0:
            order = np.asarray([], dtype=np.int64)
        else:
            base_score = (
                base_alpha * offline.zscore_1d(row.concat_scores[kept])
                + (1.0 - base_alpha) * offline.zscore_1d(row.bm25_scores[kept])
            )
            fused = (
                base_weight * offline.zscore_1d(base_score)
                + (1.0 - base_weight) * offline.zscore_1d(row.qwen_scores[kept])
            )
            order = kept[np.argsort(fused)[::-1]]
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


def source_sets_for_strategy(row: BaseBucketScores, strategy: str) -> list[set[int]]:
    sources = [
        set(int(index) for index in union_helpers.top_indices(scores, 20))
        for scores in row.prompt_scores
    ]
    sources.append(set(int(index) for index in union_helpers.top_indices(row.bm25_scores, 20)))
    if strategy == "prompt3_bm25_top20":
        return sources
    if strategy == "prompt3_bm25_qwen_top20":
        return sources + [set(int(index) for index in union_helpers.top_indices(row.qwen_scores, 20))]
    raise ValueError(f"Unsupported strategy: {strategy}")


def source_count_map(source_sets: list[set[int]]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for source_set in source_sets:
        for index in source_set:
            counts[index] = counts.get(index, 0) + 1
    return counts


def strategy_oracle_summary(rows: list[BaseBucketScores], *, strategy: str) -> list[dict[str, Any]]:
    scored = [row for row in rows if not row.is_abstention and row.has_target and row.gold_ids]
    max_sources = 5 if strategy == "prompt3_bm25_qwen_top20" else 4
    output = []
    for threshold in range(1, max_sources + 1):
        sizes = []
        oracle = []
        for row in scored:
            counts = source_count_map(source_sets_for_strategy(row, strategy))
            kept = np.asarray(
                [index for index, count in counts.items() if count >= threshold],
                dtype=np.int64,
            )
            sizes.append(len(kept))
            oracle.append(gold_in_indices(row.gold_ids, row.candidate_ids, kept))
        output.append(
            {
                "min_source_count": threshold,
                "avg_candidate_count": float(np.mean(sizes)) if sizes else float("nan"),
                "oracle_recall_all": float(np.mean(oracle)) if oracle else float("nan"),
            }
        )
    return output


def evaluate_row(
    *,
    strategy: str,
    strategy_description: str,
    base_alpha: float,
    base_weight: float,
    predictions: list[Prediction],
    bootstrap_samples: int,
) -> dict[str, Any]:
    metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
    session = offline.session_retrieval_metrics(predictions)
    rank = offline.rank_metrics(predictions)
    summary = bm25_sweep.summarize_metrics(metrics, session, rank)
    return {
        "strategy": strategy,
        "strategy_description": strategy_description,
        "base_alpha": base_alpha,
        "base_weight": base_weight,
        "qwen_weight": 1.0 - base_weight,
        "metrics": metrics,
        "session_metrics": session,
        "rank_metrics": rank,
        "summary": summary,
    }


def gold_in_indices(gold_ids: list[str], candidate_ids: list[str], indices: np.ndarray) -> float:
    retrieved = {candidate_ids[int(index)] for index in indices}
    return float(set(gold_ids).issubset(retrieved)) if gold_ids else 0.0


def parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise ValueError("No float values parsed.")
    return values


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
        "# Temporary Qwen3 second-stage rerank",
        "",
        "`base_weight` blends concat+BM25 with Qwen3 score: final = base_weight * base + (1-base_weight) * qwen.",
        "All prediction rows keep candidates with `source_count >= 2`.",
        "",
        "## Strategy Oracle",
        "",
    ]
    for strategy, summary_rows in payload["strategy_oracle_summary"].items():
        lines.extend(
            [
                f"### `{strategy}`",
                "",
                "| min source count | avg candidate count | oracle recall_all |",
                "|---:|---:|---:|",
            ]
        )
        for row in summary_rows:
            lines.append(
                f"| {row['min_source_count']} | {row['avg_candidate_count']:.1f} | "
                f"{row['oracle_recall_all']:.3f} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Rerank Results",
            "",
            "| rank | strategy | base alpha | base weight | qwen weight | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |",
            "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for index, row in enumerate(rows, start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | `{row['strategy']}` | {row['base_alpha']:.2f} | "
            f"{row['base_weight']:.2f} | {row['qwen_weight']:.2f} | "
            f"{summary['recall_all@3']:.3f} | {summary['ndcg_any@3']:.3f} | "
            f"{summary['recall_all@5']:.3f} | {summary['ndcg_any@5']:.3f} | "
            f"{summary['mrr']:.3f} | {summary['session_hit@5']:.3f} | {summary['n_scored']} |"
        )
    lines.extend(["", "## Inputs", ""])
    lines.append(f"- dump_dir: `{payload['inputs']['dump_dir']}`")
    lines.append(f"- qwen_dir: `{payload['inputs']['qwen_dir']}`")
    lines.append(f"- config: `{payload['inputs']['config']['name']}`")
    lines.append(f"- base_alphas: {payload['inputs']['base_alphas']}")
    lines.append(f"- base_weights: {payload['inputs']['base_weights']}")
    lines.append(f"- elapsed_seconds: {payload['elapsed_seconds']:.1f}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
