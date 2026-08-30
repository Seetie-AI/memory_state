"""Stage 3 sparse-logits second-stage reranker for source agreement.

This script keeps the strong Stage 3 shortlist rule fixed:

    top20 from each K=3 prompt source + top20 BM25, keep source_count >= 2

It then tests whether saved top-k next-token logits can improve the second
stage rerank inside that small candidate set. No model is run; the script only
reads existing Stage 3 hidden vectors and top-k logits.
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
from safetensors import safe_open

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
for path in [SCRIPTS, SRC]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import stage2_offline_analyze as offline
import stage3_prompt_fusion_analyze as fusion
import stage3_prompt_fusion_bm25_sweep as bm25_sweep
import union_top20_prompt_bm25_fusion as union_helpers
from eval.longmemeval_metrics import Prediction, evaluate


DEFAULT_CONFIG = "concat_k3_norm_weighted_userword_tag_assoc"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "step3_bm25_fusion" / "second_stage"
DEFAULT_SOURCE_TOP_K = 20
DEFAULT_MIN_SOURCE_COUNT = 2
DEFAULT_BASE_ALPHA = 0.75
DEFAULT_BASE_WEIGHTS = [0.0, 0.25, 0.5, 0.65, 0.75, 0.85, 0.9, 1.0]
DEFAULT_LOGIT_METHODS = ["idf_overlap", "overlap", "idf_weighted_dot"]


@dataclass
class BucketScores:
    question_id: str
    candidate_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool
    source_indices: dict[str, np.ndarray]
    prompt_scores: list[np.ndarray]
    concat_scores: np.ndarray
    bm25_scores: np.ndarray
    logit_scores: dict[str, dict[str, np.ndarray]]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(fusion.DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(fusion.DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=None)
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--source-top-k", type=int, default=DEFAULT_SOURCE_TOP_K)
    parser.add_argument("--min-source-count", type=int, default=DEFAULT_MIN_SOURCE_COUNT)
    parser.add_argument("--base-alpha", type=float, default=DEFAULT_BASE_ALPHA)
    parser.add_argument(
        "--base-weights",
        default=",".join(str(value) for value in DEFAULT_BASE_WEIGHTS),
        help="Weights for base concat+BM25 score when fusing with logits.",
    )
    parser.add_argument(
        "--logit-methods",
        default=",".join(DEFAULT_LOGIT_METHODS),
        help="Comma-separated sparse logit methods.",
    )
    parser.add_argument(
        "--single-logit-variants",
        default="2-4-1_user_word,1-3,2-5",
        help="Comma-separated variants to test as standalone logit rerankers.",
    )
    parser.add_argument(
        "--fused-logit-variants",
        default="2-4-1_user_word,1-3,2-5",
        help="Comma-separated variants to z-average for fused logits.",
    )
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    config = bm25_sweep.CONFIG_BY_NAME[args.config]
    base_weights = parse_float_list(args.base_weights)
    logit_methods = parse_str_list(args.logit_methods)
    single_logit_variants = parse_str_list(args.single_logit_variants)
    fused_logit_variants = parse_str_list(args.fused_logit_variants)
    logit_variants = sorted(set(single_logit_variants + fused_logit_variants))

    dump_dir = Path(args.dump_dir)
    manifest = offline.load_manifest(dump_dir)
    offline.validate_manifest(manifest)
    if not manifest.get("topk_logits", {}).get("enabled"):
        raise ValueError(f"Store does not have top-k logits enabled: {dump_dir}")
    missing = [variant for variant in logit_variants if variant not in manifest["prompt_variants"]]
    if missing:
        raise ValueError(f"Logit variants missing from manifest: {missing}")

    records = offline.load_records(dump_dir, manifest, Path(args.data))
    buckets = offline.group_by_instance(records)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_prefix or f"logits_second_stage_rerank_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    json_path = output_dir / f"{prefix}.json"
    md_path = output_dir / f"{prefix}.md"
    if not args.overwrite:
        existing = [path for path in [json_path, md_path] if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    print(
        f"records={len(records)} config={config.name} source_top_k={args.source_top_k} "
        f"min_source_count={args.min_source_count} base_alpha={args.base_alpha}",
        flush=True,
    )
    print(f"logit_variants={logit_variants} methods={logit_methods}", flush=True)

    reprs = union_helpers.build_config_reprs_cpu(dump_dir, manifest, records, config)
    print("loading sparse logits", flush=True)
    logits = load_logits_for_variants(dump_dir, manifest, records, logit_variants)
    idf_by_variant = {
        variant: token_idf(records, values["token_ids"])
        for variant, values in logits.items()
    }
    rows = build_bucket_scores(
        records,
        buckets,
        config,
        reprs,
        logits,
        idf_by_variant,
        logit_methods=logit_methods,
        source_top_k=args.source_top_k,
    )

    result_rows: list[dict[str, Any]] = []
    baseline_predictions = predictions_from_rows(
        rows,
        reranker="base_concat_bm25",
        logit_method=None,
        base_alpha=args.base_alpha,
        base_weight=1.0,
        min_source_count=args.min_source_count,
        fused_logit_variants=fused_logit_variants,
        top_k=args.top_k,
    )
    result_rows.append(
        evaluate_row(
            reranker="base_concat_bm25",
            logit_method=None,
            base_weight=1.0,
            predictions=baseline_predictions,
            bootstrap_samples=args.bootstrap_samples,
        )
    )

    for method in logit_methods:
        rerankers = [f"logits_{variant}" for variant in single_logit_variants]
        rerankers.append("logits_fused")
        for reranker in rerankers:
            for base_weight in base_weights:
                if reranker == "base_concat_bm25":
                    continue
                predictions = predictions_from_rows(
                    rows,
                    reranker=reranker,
                    logit_method=method,
                    base_alpha=args.base_alpha,
                    base_weight=base_weight,
                    min_source_count=args.min_source_count,
                    fused_logit_variants=fused_logit_variants,
                    top_k=args.top_k,
                )
                result_rows.append(
                    evaluate_row(
                        reranker=reranker,
                        logit_method=method,
                        base_weight=base_weight,
                        predictions=predictions,
                        bootstrap_samples=args.bootstrap_samples,
                    )
                )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "stage3_logits_second_stage_rerank",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "config": bm25_sweep.config_to_json(config),
            "source_top_k": args.source_top_k,
            "min_source_count": args.min_source_count,
            "base_alpha": args.base_alpha,
            "base_weights": base_weights,
            "logit_methods": logit_methods,
            "single_logit_variants": single_logit_variants,
            "fused_logit_variants": fused_logit_variants,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "topk_logits": manifest.get("topk_logits"),
        },
        "shortlist_summary": shortlist_summary(rows, min_source_count=args.min_source_count),
        "rows": sorted(result_rows, key=result_sort_key, reverse=True),
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}", flush=True)
    print(f"wrote {md_path}", flush=True)
    print(f"elapsed {payload['elapsed_seconds']:.1f}s", flush=True)
    return 0


def load_logits_for_variants(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    variants: list[str],
) -> dict[str, dict[str, np.ndarray]]:
    variant_indices = {
        variant: offline.index_of(manifest["prompt_variants"], variant, "variant")
        for variant in variants
    }
    position_index = offline.index_of(manifest["positions"], "last", "position")
    topk = int(manifest["topk_logits"]["k"])
    output = {
        variant: {
            "token_ids": np.empty((len(records), topk), dtype=np.int32),
            "logit_values": np.empty((len(records), topk), dtype=np.float32),
        }
        for variant in variants
    }

    records_by_chunk: dict[str, list[tuple[int, offline.Stage2Record]]] = {}
    for row_index, record in enumerate(records):
        records_by_chunk.setdefault(record.chunk_file, []).append((row_index, record))

    for chunk_number, (chunk_file, rows) in enumerate(sorted(records_by_chunk.items()), start=1):
        path = dump_dir / chunk_file
        if not path.exists():
            raise FileNotFoundError(f"Manifest chunk is missing: {path}")
        output_rows = np.fromiter((row_index for row_index, _record in rows), dtype=np.int64)
        chunk_rows = np.fromiter((record.chunk_index for _row_index, record in rows), dtype=np.int64)
        with safe_open(str(path), framework="pt", device="cpu") as handle:
            token_slice = handle.get_slice("top_logit_token_ids")
            value_slice = handle.get_slice("top_logit_values")
            for variant, variant_index in variant_indices.items():
                token_values = token_slice[:, variant_index, position_index, :].int().numpy()
                logit_values = value_slice[:, variant_index, position_index, :].float().numpy()
                output[variant]["token_ids"][output_rows] = token_values[chunk_rows]
                output[variant]["logit_values"][output_rows] = logit_values[chunk_rows]
        if chunk_number == 1 or chunk_number == len(records_by_chunk) or chunk_number % 20 == 0:
            print(f"  logits chunk {chunk_number}/{len(records_by_chunk)}", flush=True)
        del output_rows, chunk_rows
    return output


def build_bucket_scores(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    config: bm25_sweep.FusionConfig,
    reprs: list[fusion.VectorRepr],
    logits: dict[str, dict[str, np.ndarray]],
    idf_by_variant: dict[str, dict[int, float]],
    *,
    logit_methods: list[str],
    source_top_k: int,
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

        prompt_scores = [union_helpers.score_single_repr(bucket, repr_) for repr_ in reprs]
        concat_scores = bm25_sweep.score_config_bucket(config, bucket, reprs)
        bm25_scores = union_helpers.full_bm25_scores(query_record, candidate_records)
        source_indices: dict[str, np.ndarray] = {}
        for cell, scores in zip(config.cells, prompt_scores, strict=True):
            source_indices[cell.label] = union_helpers.top_indices(scores, source_top_k)
        source_indices["bm25"] = union_helpers.top_indices(bm25_scores, source_top_k)

        logit_scores: dict[str, dict[str, np.ndarray]] = {}
        for variant, arrays in logits.items():
            logit_scores[variant] = sparse_scores_for_bucket(
                bucket,
                token_ids=arrays["token_ids"],
                logit_values=arrays["logit_values"],
                idf=idf_by_variant[variant],
                methods=logit_methods,
            )

        output.append(
            BucketScores(
                question_id=query_record.question_id,
                candidate_ids=candidate_ids,
                gold_ids=list(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
                source_indices=source_indices,
                prompt_scores=prompt_scores,
                concat_scores=concat_scores,
                bm25_scores=bm25_scores,
                logit_scores=logit_scores,
            )
        )
    return output


def sparse_scores_for_bucket(
    bucket: offline.InstanceBucket,
    *,
    token_ids: np.ndarray,
    logit_values: np.ndarray,
    idf: dict[int, float],
    methods: list[str],
) -> dict[str, np.ndarray]:
    q_ids = token_ids[bucket.query_index]
    q_set = set(int(value) for value in q_ids.tolist())
    q_weights = softmax_1d(logit_values[bucket.query_index])
    q_map = dict(zip(q_ids.tolist(), q_weights.tolist(), strict=True))
    scores = {method: [] for method in methods}
    for candidate_index in bucket.candidate_indices:
        c_ids = token_ids[candidate_index]
        c_set = set(int(value) for value in c_ids.tolist())
        c_weights = softmax_1d(logit_values[candidate_index])
        c_map = dict(zip(c_ids.tolist(), c_weights.tolist(), strict=True))
        shared = q_set.intersection(c_set)
        for method in methods:
            if method == "overlap":
                value = len(shared) / max(np.sqrt(len(q_set) * len(c_set)), 1.0)
            elif method == "weighted_dot":
                value = sum(q_map[token] * c_map[token] for token in shared)
            elif method == "idf_overlap":
                value = sum(float(idf.get(token, 0.0)) for token in shared)
            elif method == "idf_weighted_dot":
                value = sum(float(idf.get(token, 0.0)) * q_map[token] * c_map[token] for token in shared)
            else:
                raise ValueError(f"Unsupported logit method: {method}")
            scores[method].append(value)
    return {method: np.asarray(values, dtype=np.float64) for method, values in scores.items()}


def softmax_1d(values: np.ndarray) -> np.ndarray:
    shifted = values.astype(np.float64, copy=False) - float(np.max(values))
    exp = np.exp(shifted)
    return exp / max(float(np.sum(exp)), 1e-12)


def token_idf(records: list[offline.Stage2Record], token_ids: np.ndarray) -> dict[int, float]:
    candidate_indices = [index for index, record in enumerate(records) if record.role != "query"]
    df: dict[int, int] = {}
    for index in candidate_indices:
        for token_id in set(int(value) for value in token_ids[index].tolist()):
            df[token_id] = df.get(token_id, 0) + 1
    n = len(candidate_indices)
    return {token_id: float(np.log((n + 1) / (count + 1)) + 1.0) for token_id, count in df.items()}


def predictions_from_rows(
    rows: list[BucketScores],
    *,
    reranker: str,
    logit_method: str | None,
    base_alpha: float,
    base_weight: float,
    min_source_count: int,
    fused_logit_variants: list[str],
    top_k: int,
) -> list[Prediction]:
    predictions = []
    for row in rows:
        kept = kept_indices(row, min_source_count=min_source_count)
        if len(kept) == 0:
            order = np.asarray([], dtype=np.int64)
        else:
            base = base_concat_bm25(row, kept, base_alpha=base_alpha)
            if reranker == "base_concat_bm25":
                final = base
            else:
                if logit_method is None:
                    raise ValueError("logit_method is required for logits rerankers.")
                logit_score = logit_score_for_reranker(
                    row,
                    kept,
                    reranker=reranker,
                    method=logit_method,
                    fused_logit_variants=fused_logit_variants,
                )
                final = (
                    base_weight * offline.zscore_1d(base)
                    + (1.0 - base_weight) * offline.zscore_1d(logit_score)
                )
            order = kept[np.argsort(final)[::-1]]
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


def kept_indices(row: BucketScores, *, min_source_count: int) -> np.ndarray:
    counts: dict[int, int] = {}
    for indices in row.source_indices.values():
        for index in indices:
            counts[int(index)] = counts.get(int(index), 0) + 1
    kept = [index for index, count in counts.items() if count >= min_source_count]
    return np.asarray(sorted(kept), dtype=np.int64)


def base_concat_bm25(row: BucketScores, indices: np.ndarray, *, base_alpha: float) -> np.ndarray:
    return (
        base_alpha * offline.zscore_1d(row.concat_scores[indices])
        + (1.0 - base_alpha) * offline.zscore_1d(row.bm25_scores[indices])
    )


def logit_score_for_reranker(
    row: BucketScores,
    indices: np.ndarray,
    *,
    reranker: str,
    method: str,
    fused_logit_variants: list[str],
) -> np.ndarray:
    if reranker == "logits_fused":
        parts = [
            offline.zscore_1d(row.logit_scores[variant][method][indices])
            for variant in fused_logit_variants
        ]
        return np.mean(np.stack(parts, axis=0), axis=0)
    prefix = "logits_"
    if reranker.startswith(prefix):
        variant = reranker[len(prefix) :]
        return row.logit_scores[variant][method][indices]
    raise ValueError(f"Unsupported reranker: {reranker}")


def evaluate_row(
    *,
    reranker: str,
    logit_method: str | None,
    base_weight: float,
    predictions: list[Prediction],
    bootstrap_samples: int,
) -> dict[str, Any]:
    metrics = evaluate(
        predictions,
        skip_abstention=True,
        bootstrap_samples=bootstrap_samples,
        ks=(1, 3, 5, 10, 20, 50),
    )
    session = offline.session_retrieval_metrics(predictions)
    rank = offline.rank_metrics(predictions)
    summary = bm25_sweep.summarize_metrics(metrics, session, rank)
    print(
        f"{reranker} method={logit_method or '-'} base_weight={base_weight:g} "
        f"R@5={summary['recall_all@5']:.3f} NDCG@5={summary['ndcg_any@5']:.3f} "
        f"MRR={summary['mrr']:.3f}",
        flush=True,
    )
    return {
        "reranker": reranker,
        "logit_method": logit_method,
        "base_weight": base_weight,
        "metrics": metrics,
        "session_metrics": session,
        "rank_metrics": rank,
        "summary": summary,
    }


def shortlist_summary(rows: list[BucketScores], *, min_source_count: int) -> dict[str, Any]:
    scored = [row for row in rows if not row.is_abstention and row.has_target and row.gold_ids]
    sizes = []
    oracle = []
    count_hist: dict[str, int] = {}
    for row in scored:
        kept = kept_indices(row, min_source_count=min_source_count)
        sizes.append(len(kept))
        oracle.append(gold_in_indices(row.gold_ids, row.candidate_ids, kept))
        gold_sources = count_gold_sources(row)
        count_hist[str(gold_sources)] = count_hist.get(str(gold_sources), 0) + 1
    return {
        "n_scored": len(scored),
        "avg_candidate_count": float(np.mean(sizes)) if sizes else float("nan"),
        "max_candidate_count": int(max(sizes)) if sizes else 0,
        "oracle_recall_all": float(np.mean(oracle)) if oracle else float("nan"),
        "gold_source_count_histogram": dict(sorted(count_hist.items(), key=lambda item: int(item[0]))),
    }


def count_gold_sources(row: BucketScores) -> int:
    return sum(
        int(gold_in_indices(row.gold_ids, row.candidate_ids, indices) > 0.0)
        for indices in row.source_indices.values()
    )


def gold_in_indices(gold_ids: list[str], candidate_ids: list[str], indices: np.ndarray) -> float:
    retrieved = {candidate_ids[int(index)] for index in indices}
    return float(set(gold_ids).issubset(retrieved)) if gold_ids else 0.0


def result_sort_key(row: dict[str, Any]) -> tuple[float, float, float, float]:
    summary = row["summary"]
    return (
        summary["recall_all@5"],
        summary["ndcg_any@5"],
        summary["mrr"],
        summary["recall_all@3"],
    )


def parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise ValueError("No floats parsed.")
    return values


def parse_str_list(value: str) -> list[str]:
    values = [item.strip() for item in value.split(",") if item.strip()]
    if not values:
        raise ValueError("No values parsed.")
    return values


def render_markdown(payload: dict[str, Any]) -> str:
    shortlist = payload["shortlist_summary"]
    lines = [
        "# Stage 3 Logits Second-Stage Rerank",
        "",
        "Shortlist: top20 from each K=3 prompt source plus top20 BM25, keeping `source_count >= 2`.",
        "",
        "## Shortlist",
        "",
        f"- avg candidates: {shortlist['avg_candidate_count']:.1f}",
        f"- max candidates: {shortlist['max_candidate_count']}",
        f"- oracle recall_all: {shortlist['oracle_recall_all']:.3f}",
        f"- gold source-count histogram: `{shortlist['gold_source_count_histogram']}`",
        "",
        "## Results",
        "",
        "| rank | reranker | logit method | base weight | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(payload["rows"], start=1):
        summary = row["summary"]
        method = row["logit_method"] if row["logit_method"] is not None else "-"
        lines.append(
            f"| {index} | `{row['reranker']}` | `{method}` | {row['base_weight']:.2f} | "
            f"{summary['recall_all@3']:.3f} | {summary['ndcg_any@3']:.3f} | "
            f"{summary['recall_all@5']:.3f} | {summary['ndcg_any@5']:.3f} | "
            f"{summary['mrr']:.3f} | {summary['session_hit@5']:.3f} | {summary['n_scored']} |"
        )
    lines.extend(
        [
            "",
            "## Inputs",
            "",
            f"- config: `{payload['inputs']['config']['name']}`",
            f"- base score: `{payload['inputs']['base_alpha']:.2f} * z(concat) + {1.0 - payload['inputs']['base_alpha']:.2f} * z(BM25)`",
            f"- single logit variants: `{payload['inputs']['single_logit_variants']}`",
            f"- fused logit variants: `{payload['inputs']['fused_logit_variants']}`",
            f"- logit methods: `{payload['inputs']['logit_methods']}`",
            f"- top-k logits: `{payload['inputs']['topk_logits']}`",
            f"- elapsed_seconds: {payload['elapsed_seconds']:.1f}",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
