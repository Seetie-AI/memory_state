"""Temporary agreement-first second-stage reranker tests.

This script reuses the Stage 3 best K=3 prompt cells and BM25 scores. It tests
the simple rule suggested by the source-overlap audit:

1. build source top-K sets
2. keep only candidates selected by at least two sources
3. rerank the kept candidates by concat+BM25, optionally using source_count as
   the primary sort key

It also compares a simpler two-source setup where the sources are only
`concat` and `BM25`.
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
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "prompt_fusion_bm25"
DEFAULT_OUTPUT_PREFIX = "tmp_agreement_second_stage"
DEFAULT_ALPHAS = [0.5, 0.65, 0.75, 0.85, 1.0]


@dataclass
class BaseBucketScores:
    question_id: str
    candidate_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool
    prompt_scores: list[np.ndarray]
    concat_scores: np.ndarray
    bm25_scores: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(fusion.DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(fusion.DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--alphas", default=",".join(str(alpha) for alpha in DEFAULT_ALPHAS))
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    config = bm25_sweep.CONFIG_BY_NAME[args.config]
    alphas = parse_float_list(args.alphas)

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

    print(f"records={len(records)} config={config.name} alphas={alphas}")
    reprs = union_helpers.build_config_reprs_cpu(dump_dir, manifest, records, config)
    base_rows = build_base_rows(records, buckets, config, reprs)

    strategies = [
        ("prompt3_bm25_top20", "three prompt top20 sources plus BM25 top20"),
        ("concat_bm25_top20", "concat top20 plus BM25 top20"),
        ("concat_bm25_top50", "concat top50 plus BM25 top50"),
    ]
    result_rows = []
    for strategy, description in strategies:
        for mode in ["score_only", "agreement_first"]:
            for alpha in alphas:
                predictions = predictions_for_strategy(
                    base_rows,
                    strategy=strategy,
                    mode=mode,
                    alpha=alpha,
                    top_k=args.top_k,
                )
                result_rows.append(
                    evaluate_row(
                        strategy=strategy,
                        strategy_description=description,
                        mode=mode,
                        alpha=alpha,
                        predictions=predictions,
                        bootstrap_samples=args.bootstrap_samples,
                    )
                )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "tmp_agreement_second_stage_rerank",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "config": bm25_sweep.config_to_json(config),
            "alphas": alphas,
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


def build_base_rows(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    config: bm25_sweep.FusionConfig,
    reprs: list[fusion.VectorRepr],
) -> list[BaseBucketScores]:
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
        output.append(
            BaseBucketScores(
                question_id=query_record.question_id,
                candidate_ids=candidate_ids,
                gold_ids=list(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
                prompt_scores=prompt_scores,
                concat_scores=concat_scores,
                bm25_scores=bm25_scores,
            )
        )
    return output


def predictions_for_strategy(
    rows: list[BaseBucketScores],
    *,
    strategy: str,
    mode: str,
    alpha: float,
    top_k: int,
) -> list[Prediction]:
    predictions = []
    for row in rows:
        source_sets = source_sets_for_strategy(row, strategy)
        source_count = source_count_map(source_sets)
        kept = np.asarray(
            [index for index, count in source_count.items() if count >= 2],
            dtype=np.int64,
        )
        if len(kept) == 0:
            order = np.asarray([], dtype=np.int64)
        else:
            fused = (
                alpha * offline.zscore_1d(row.concat_scores[kept])
                + (1.0 - alpha) * offline.zscore_1d(row.bm25_scores[kept])
            )
            if mode == "score_only":
                order = kept[np.argsort(fused)[::-1]]
            elif mode == "agreement_first":
                fused_by_index = {int(index): float(score) for index, score in zip(kept, fused, strict=True)}
                order = np.asarray(
                    sorted(
                        (int(index) for index in kept),
                        key=lambda index: (source_count[index], fused_by_index[index]),
                        reverse=True,
                    ),
                    dtype=np.int64,
                )
            else:
                raise ValueError(f"Unsupported mode: {mode}")

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
    if strategy == "prompt3_bm25_top20":
        return [
            set(int(index) for index in union_helpers.top_indices(scores, 20))
            for scores in row.prompt_scores
        ] + [set(int(index) for index in union_helpers.top_indices(row.bm25_scores, 20))]
    if strategy == "concat_bm25_top20":
        return [
            set(int(index) for index in union_helpers.top_indices(row.concat_scores, 20)),
            set(int(index) for index in union_helpers.top_indices(row.bm25_scores, 20)),
        ]
    if strategy == "concat_bm25_top50":
        return [
            set(int(index) for index in union_helpers.top_indices(row.concat_scores, 50)),
            set(int(index) for index in union_helpers.top_indices(row.bm25_scores, 50)),
        ]
    raise ValueError(f"Unsupported strategy: {strategy}")


def source_count_map(source_sets: list[set[int]]) -> dict[int, int]:
    counts: dict[int, int] = {}
    for source_set in source_sets:
        for index in source_set:
            counts[index] = counts.get(index, 0) + 1
    return counts


def strategy_oracle_summary(rows: list[BaseBucketScores], *, strategy: str) -> list[dict[str, Any]]:
    scored = [row for row in rows if not row.is_abstention and row.has_target and row.gold_ids]
    max_sources = 4 if strategy == "prompt3_bm25_top20" else 2
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
    mode: str,
    alpha: float,
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
        "mode": mode,
        "alpha": alpha,
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
        raise ValueError("No alpha values parsed.")
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
        "# Temporary agreement second-stage rerank",
        "",
        "All rows keep only candidates with `source_count >= 2`, then rerank with concat+BM25.",
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
            "| rank | strategy | mode | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |",
            "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for index, row in enumerate(rows, start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | `{row['strategy']}` | `{row['mode']}` | {row['alpha']:.2f} | "
            f"{summary['recall_all@3']:.3f} | {summary['ndcg_any@3']:.3f} | "
            f"{summary['recall_all@5']:.3f} | {summary['ndcg_any@5']:.3f} | "
            f"{summary['mrr']:.3f} | {summary['session_hit@5']:.3f} | {summary['n_scored']} |"
        )
    lines.extend(["", "## Inputs", ""])
    lines.append(f"- dump_dir: `{payload['inputs']['dump_dir']}`")
    lines.append(f"- config: `{payload['inputs']['config']['name']}`")
    lines.append(f"- alphas: {payload['inputs']['alphas']}")
    lines.append(f"- elapsed_seconds: {payload['elapsed_seconds']:.1f}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
