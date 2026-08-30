"""Stage 3 PromptReps-style sparse-logits screening.

This is an offline approximation of PromptReps sparse retrieval over the saved
Stage 3 top-k logits. It does not rerun the model. For each text row, it keeps
only saved top-k logit tokens that also appear in the original text under the
same tokenizer, then uses log1p(relu(logit)) as a sparse impact weight.

The main question is whether logits can be used as a cheap first-stage screen:

1. build top-20 candidate shortlists with logits and/or BM25
2. rerank the shortlist with either
   - 0.50 hidden concat + 0.25 BM25 + 0.25 logits
   - pure logits

This belongs to Stage 3 step 2 prompt fusion. BM25 is included here only as a
shortlist/rerank signal so logits screening can be compared against the current
K=3 hidden-state fusion plan.
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
from baselines.bm25 import BM25Retriever
from eval.longmemeval_metrics import Prediction, evaluate


DEFAULT_CONFIG = "concat_k3_norm_weighted_userword_tag_assoc"
DEFAULT_DUMP_DIR = fusion.DEFAULT_DUMP_DIR
DEFAULT_DATA = fusion.DEFAULT_DATA
DEFAULT_TOKENIZER_PATH = ROOT / "models" / "Qwen3.5-9B-MLX-4bit"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "prompt_fusion" / "logits_screening"
DEFAULT_SCREEN_TOP_K = 20
DEFAULT_EVAL_TOP_K = 50
DEFAULT_LOGIT_VARIANTS = ["2-4-1_user_word", "1-3", "2-5", "2-3-2_mem"]
DEFAULT_FUSED_LOGIT_VARIANTS = ["2-4-1_user_word", "1-3", "2-5"]
DEFAULT_SCREEN_MODES = [
    "logits_top20",
    "bm25_top20",
    "logits_bm25_union20",
    "logits_bm25_fused_top20",
    "hidden_top20",
]
DEFAULT_SCORE_MODES = [
    "mix_50_hidden_25_bm25_25_logits",
    "logits_only",
    "hidden_bm25_75_25",
]


@dataclass
class SparseVariant:
    variant: str
    maps: list[dict[int, float]]
    stats: dict[str, Any]


@dataclass
class BucketScores:
    question_id: str
    query_text: str
    candidate_ids: list[str]
    candidate_texts: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool
    hidden_scores: np.ndarray
    bm25_scores: np.ndarray
    logits_scores: dict[str, np.ndarray]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--tokenizer-path", default=str(DEFAULT_TOKENIZER_PATH))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=None)
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--logit-variants", default=",".join(DEFAULT_LOGIT_VARIANTS))
    parser.add_argument("--fused-logit-variants", default=",".join(DEFAULT_FUSED_LOGIT_VARIANTS))
    parser.add_argument("--screen-modes", default=",".join(DEFAULT_SCREEN_MODES))
    parser.add_argument("--score-modes", default=",".join(DEFAULT_SCORE_MODES))
    parser.add_argument("--screen-top-k", type=int, default=DEFAULT_SCREEN_TOP_K)
    parser.add_argument("--top-k", type=int, default=DEFAULT_EVAL_TOP_K)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    config = bm25_sweep.CONFIG_BY_NAME[args.config]
    logit_variants = parse_str_list(args.logit_variants)
    fused_logit_variants = parse_str_list(args.fused_logit_variants)
    screen_modes = parse_str_list(args.screen_modes)
    score_modes = parse_str_list(args.score_modes)
    logit_sources = [*logit_variants, "fused_k3"]

    dump_dir = Path(args.dump_dir)
    manifest = offline.load_manifest(dump_dir)
    offline.validate_manifest(manifest)
    if not manifest.get("topk_logits", {}).get("enabled"):
        raise ValueError(f"Store does not have top-k logits enabled: {dump_dir}")
    for variant in sorted(set(logit_variants + fused_logit_variants)):
        if variant not in manifest["prompt_variants"]:
            raise ValueError(f"Variant missing from manifest: {variant}")

    records = offline.load_records(dump_dir, manifest, Path(args.data))
    buckets = offline.group_by_instance(records)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_prefix or f"promptreps_screening_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    json_path = output_dir / f"{prefix}.json"
    md_path = output_dir / f"{prefix}.md"
    if not args.overwrite:
        existing = [path for path in [json_path, md_path] if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    print(
        f"records={len(records)} config={config.name} screen_top_k={args.screen_top_k} "
        f"logit_variants={logit_variants}",
        flush=True,
    )
    reprs = union_helpers.build_config_reprs_cpu(dump_dir, manifest, records, config)
    raw_logits = load_logits_for_variants(dump_dir, manifest, records, logit_variants)
    sparse_variants = build_sparse_variants(
        records,
        raw_logits,
        tokenizer_path=Path(args.tokenizer_path),
    )
    del raw_logits
    gc.collect()

    bucket_rows = build_bucket_scores(
        records,
        buckets,
        config,
        reprs,
        sparse_variants,
        fused_logit_variants=fused_logit_variants,
    )

    result_rows: list[dict[str, Any]] = []
    shortlist_rows: list[dict[str, Any]] = []
    for logit_source in logit_sources:
        for screen_mode in screen_modes:
            shortlist_rows.append(
                shortlist_summary(
                    bucket_rows,
                    logit_source=logit_source,
                    screen_mode=screen_mode,
                    screen_top_k=args.screen_top_k,
                )
            )
            for score_mode in score_modes:
                predictions = predictions_from_rows(
                    bucket_rows,
                    logit_source=logit_source,
                    screen_mode=screen_mode,
                    score_mode=score_mode,
                    screen_top_k=args.screen_top_k,
                    top_k=args.top_k,
                )
                result_rows.append(
                    evaluate_row(
                        logit_source=logit_source,
                        screen_mode=screen_mode,
                        score_mode=score_mode,
                        predictions=predictions,
                        bootstrap_samples=args.bootstrap_samples,
                    )
                )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "stage3_logits_promptreps_screening",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "tokenizer_path": str(Path(args.tokenizer_path)),
            "config": bm25_sweep.config_to_json(config),
            "logit_variants": logit_variants,
            "fused_logit_variants": fused_logit_variants,
            "screen_modes": screen_modes,
            "score_modes": score_modes,
            "screen_top_k": args.screen_top_k,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "topk_logits": manifest.get("topk_logits"),
        },
        "sparse_stats": {variant: sparse.stats for variant, sparse in sparse_variants.items()},
        "shortlist_rows": sorted(
            shortlist_rows,
            key=lambda row: (row["oracle_recall_all"], -row["avg_candidate_count"]),
            reverse=True,
        ),
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


def build_sparse_variants(
    records: list[offline.Stage2Record],
    raw_logits: dict[str, dict[str, np.ndarray]],
    *,
    tokenizer_path: Path,
) -> dict[str, SparseVariant]:
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path), trust_remote_code=False)
    variants = list(raw_logits)
    maps_by_variant: dict[str, list[dict[int, float]]] = {variant: [] for variant in variants}
    counts_by_variant: dict[str, list[int]] = {variant: [] for variant in variants}
    text_token_counts: list[int] = []

    for row_index, record in enumerate(records):
        text_ids = set(int(token_id) for token_id in tokenizer.encode(record.text or "\n", add_special_tokens=False))
        text_token_counts.append(len(text_ids))
        for variant in variants:
            sparse_map = sparse_impact_map(
                raw_logits[variant]["token_ids"][row_index],
                raw_logits[variant]["logit_values"][row_index],
                text_ids=text_ids,
            )
            maps_by_variant[variant].append(sparse_map)
            counts_by_variant[variant].append(len(sparse_map))
        if row_index == 0 or (row_index + 1) % 5000 == 0 or row_index + 1 == len(records):
            print(f"  token-filtered {row_index + 1}/{len(records)} rows", flush=True)

    output = {}
    for variant in variants:
        counts = np.asarray(counts_by_variant[variant], dtype=np.float64)
        output[variant] = SparseVariant(
            variant=variant,
            maps=maps_by_variant[variant],
            stats={
                "avg_kept_logit_tokens": float(np.mean(counts)),
                "median_kept_logit_tokens": float(np.median(counts)),
                "zero_fraction": float(np.mean(counts == 0)),
                "avg_unique_text_tokens": float(np.mean(text_token_counts)),
                "max_kept_logit_tokens": int(np.max(counts)) if len(counts) else 0,
            },
        )
    return output


def sparse_impact_map(
    token_ids: np.ndarray,
    logit_values: np.ndarray,
    *,
    text_ids: set[int],
) -> dict[int, float]:
    output: dict[int, float] = {}
    for token_id, logit in zip(token_ids.tolist(), logit_values.tolist(), strict=True):
        token = int(token_id)
        if token not in text_ids:
            continue
        weight = float(np.log1p(max(float(logit), 0.0)))
        if weight <= 0.0:
            continue
        output[token] = max(output.get(token, 0.0), weight)
    return output


def build_bucket_scores(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    config: bm25_sweep.FusionConfig,
    reprs: list[fusion.VectorRepr],
    sparse_variants: dict[str, SparseVariant],
    *,
    fused_logit_variants: list[str],
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
        hidden_scores = bm25_sweep.score_config_bucket(config, bucket, reprs)
        bm25_scores = union_helpers.full_bm25_scores(query_record, candidate_records)
        logits_scores: dict[str, np.ndarray] = {}
        for variant, sparse in sparse_variants.items():
            logits_scores[variant] = sparse_scores_for_bucket(bucket, sparse.maps)
        fused_parts = [
            offline.zscore_1d(logits_scores[variant])
            for variant in fused_logit_variants
        ]
        logits_scores["fused_k3"] = np.mean(np.stack(fused_parts, axis=0), axis=0)
        output.append(
            BucketScores(
                question_id=query_record.question_id,
                query_text=query_record.text,
                candidate_ids=candidate_ids,
                candidate_texts=[record.text for record in candidate_records],
                gold_ids=list(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
                hidden_scores=hidden_scores,
                bm25_scores=bm25_scores,
                logits_scores=logits_scores,
            )
        )
    return output


def sparse_scores_for_bucket(
    bucket: offline.InstanceBucket,
    sparse_maps: list[dict[int, float]],
) -> np.ndarray:
    query_map = sparse_maps[bucket.query_index]
    scores = []
    for candidate_index in bucket.candidate_indices:
        candidate_map = sparse_maps[candidate_index]
        if not query_map or not candidate_map:
            scores.append(0.0)
            continue
        if len(query_map) <= len(candidate_map):
            shared = set(query_map).intersection(candidate_map)
        else:
            shared = set(candidate_map).intersection(query_map)
        scores.append(sum(query_map[token] * candidate_map[token] for token in shared))
    return np.asarray(scores, dtype=np.float64)


def predictions_from_rows(
    rows: list[BucketScores],
    *,
    logit_source: str,
    screen_mode: str,
    score_mode: str,
    screen_top_k: int,
    top_k: int,
) -> list[Prediction]:
    predictions = []
    for row in rows:
        shortlist = shortlist_indices(
            row,
            logit_source=logit_source,
            screen_mode=screen_mode,
            screen_top_k=screen_top_k,
        )
        if len(shortlist) == 0:
            order = np.asarray([], dtype=np.int64)
        else:
            scores = score_shortlist(
                row,
                shortlist,
                logit_source=logit_source,
                score_mode=score_mode,
            )
            order = shortlist[np.argsort(scores)[::-1]]
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


def shortlist_indices(
    row: BucketScores,
    *,
    logit_source: str,
    screen_mode: str,
    screen_top_k: int,
) -> np.ndarray:
    logits = row.logits_scores[logit_source]
    if screen_mode == "logits_top20":
        return top_indices(logits, screen_top_k)
    if screen_mode == "bm25_top20":
        return top_indices(row.bm25_scores, screen_top_k)
    if screen_mode == "hidden_top20":
        return top_indices(row.hidden_scores, screen_top_k)
    if screen_mode == "logits_bm25_union20":
        indices = set(int(index) for index in top_indices(logits, screen_top_k))
        indices.update(int(index) for index in top_indices(row.bm25_scores, screen_top_k))
        return np.asarray(sorted(indices), dtype=np.int64)
    if screen_mode == "logits_bm25_fused_top20":
        fused = 0.5 * offline.zscore_1d(logits) + 0.5 * offline.zscore_1d(row.bm25_scores)
        return top_indices(fused, screen_top_k)
    raise ValueError(f"Unsupported screen_mode: {screen_mode}")


def score_shortlist(
    row: BucketScores,
    indices: np.ndarray,
    *,
    logit_source: str,
    score_mode: str,
) -> np.ndarray:
    hidden = row.hidden_scores[indices]
    bm25 = local_bm25_scores(row, indices)
    logits = row.logits_scores[logit_source][indices]
    if score_mode == "mix_50_hidden_25_bm25_25_logits":
        return (
            0.50 * offline.zscore_1d(hidden)
            + 0.25 * offline.zscore_1d(bm25)
            + 0.25 * offline.zscore_1d(logits)
        )
    if score_mode == "logits_only":
        return logits
    if score_mode == "hidden_bm25_75_25":
        return 0.75 * offline.zscore_1d(hidden) + 0.25 * offline.zscore_1d(bm25)
    raise ValueError(f"Unsupported score_mode: {score_mode}")


def local_bm25_scores(row: BucketScores, indices: np.ndarray) -> np.ndarray:
    texts = [row.candidate_texts[int(index)] for index in indices]
    scores = np.zeros(len(indices), dtype=np.float64)
    if not texts:
        return scores
    retriever = BM25Retriever().fit(texts)
    for local_rank, score in retriever.query(row.query_text, top_k=len(texts)):
        scores[int(local_rank)] = float(score)
    return scores


def top_indices(scores: np.ndarray, k: int) -> np.ndarray:
    order = np.argsort(scores)[::-1]
    return order[: min(k, len(order))].astype(np.int64, copy=False)


def shortlist_summary(
    rows: list[BucketScores],
    *,
    logit_source: str,
    screen_mode: str,
    screen_top_k: int,
) -> dict[str, Any]:
    scored = [row for row in rows if not row.is_abstention and row.has_target and row.gold_ids]
    sizes = []
    oracle = []
    for row in scored:
        indices = shortlist_indices(
            row,
            logit_source=logit_source,
            screen_mode=screen_mode,
            screen_top_k=screen_top_k,
        )
        sizes.append(len(indices))
        oracle.append(gold_in_indices(row.gold_ids, row.candidate_ids, indices))
    return {
        "logit_source": logit_source,
        "screen_mode": screen_mode,
        "avg_candidate_count": float(np.mean(sizes)) if sizes else float("nan"),
        "max_candidate_count": int(max(sizes)) if sizes else 0,
        "oracle_recall_all": float(np.mean(oracle)) if oracle else float("nan"),
        "n_scored": len(scored),
    }


def gold_in_indices(gold_ids: list[str], candidate_ids: list[str], indices: np.ndarray) -> float:
    retrieved = {candidate_ids[int(index)] for index in indices}
    return float(set(gold_ids).issubset(retrieved)) if gold_ids else 0.0


def evaluate_row(
    *,
    logit_source: str,
    screen_mode: str,
    score_mode: str,
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
        f"{logit_source} {screen_mode} {score_mode} "
        f"R@5={summary['recall_all@5']:.3f} NDCG@5={summary['ndcg_any@5']:.3f} "
        f"MRR={summary['mrr']:.3f}",
        flush=True,
    )
    return {
        "logit_source": logit_source,
        "screen_mode": screen_mode,
        "score_mode": score_mode,
        "metrics": metrics,
        "session_metrics": session,
        "rank_metrics": rank,
        "summary": summary,
    }


def result_sort_key(row: dict[str, Any]) -> tuple[float, float, float, float]:
    summary = row["summary"]
    return (
        summary["recall_all@5"],
        summary["ndcg_any@5"],
        summary["mrr"],
        summary["recall_all@3"],
    )


def parse_str_list(value: str) -> list[str]:
    output = [item.strip() for item in value.split(",") if item.strip()]
    if not output:
        raise ValueError("No values parsed.")
    return output


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage 3 PromptReps-Style Logits Screening",
        "",
        "Offline approximation: saved top-k logits are intersected with original text tokens, then weighted with `log1p(relu(logit))`.",
        "",
        "## Sparse Stats",
        "",
        "| variant | avg kept logits | median kept logits | zero fraction | avg text tokens |",
        "|---|---:|---:|---:|---:|",
    ]
    for variant, stats in payload["sparse_stats"].items():
        lines.append(
            f"| `{variant}` | {stats['avg_kept_logit_tokens']:.1f} | "
            f"{stats['median_kept_logit_tokens']:.1f} | {stats['zero_fraction']:.3f} | "
            f"{stats['avg_unique_text_tokens']:.1f} |"
        )
    lines.extend(
        [
            "",
            "## Shortlist Oracle",
            "",
            "| logit source | screen mode | avg candidates | oracle R |",
            "|---|---|---:|---:|",
        ]
    )
    for row in payload["shortlist_rows"]:
        lines.append(
            f"| `{row['logit_source']}` | `{row['screen_mode']}` | "
            f"{row['avg_candidate_count']:.1f} | {row['oracle_recall_all']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Rerank Results",
            "",
            "| rank | logit source | screen mode | score mode | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |",
            "|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for index, row in enumerate(payload["rows"], start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | `{row['logit_source']}` | `{row['screen_mode']}` | `{row['score_mode']}` | "
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
            f"- tokenizer: `{payload['inputs']['tokenizer_path']}`",
            f"- logit variants: `{payload['inputs']['logit_variants']}`",
            f"- fused logit variants: `{payload['inputs']['fused_logit_variants']}`",
            f"- screen top-k: {payload['inputs']['screen_top_k']}",
            f"- score modes: `{payload['inputs']['score_modes']}`",
            f"- elapsed_seconds: {payload['elapsed_seconds']:.1f}",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
