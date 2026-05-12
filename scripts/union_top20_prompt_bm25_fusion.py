"""Temporary union-shortlist fusion test for Stage 3 prompt cells.

For each query, build a candidate shortlist from:

- top-N under each of the three best prompt cells
- top-N under BM25 over the full per-instance candidate set

Then rerank only that union with a few simple fusion strategies. This asks a
different question from `vector_top50`: can independent prompt/BM25 candidate
generators rescue items that a single vector concat shortlist would miss?
"""

from __future__ import annotations

import argparse
import gc
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from itertools import combinations
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
from baselines.bm25 import BM25Retriever
from eval.longmemeval_metrics import Prediction, evaluate


DEFAULT_CONFIG = "concat_k3_norm_weighted_userword_tag_assoc"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "prompt_fusion_bm25"
DEFAULT_OUTPUT_PREFIX = "tmp_union_top20_prompt3_bm25"
DEFAULT_ALPHAS = [0.0, 0.25, 0.5, 0.65, 0.75, 0.85, 1.0]


@dataclass
class BucketUnionScores:
    question_id: str
    candidate_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool
    union_indices: np.ndarray
    source_indices: dict[str, np.ndarray]
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
    parser.add_argument("--per-source-top-k", type=int, default=20)
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

    print(
        f"records={len(records)} config={config.name} per_source_top_k={args.per_source_top_k} "
        f"alphas={alphas} bootstrap={args.bootstrap_samples}"
    )
    reprs = build_config_reprs_cpu(dump_dir, manifest, records, config)
    rows = build_union_rows(
        records,
        buckets,
        config,
        reprs,
        per_source_top_k=args.per_source_top_k,
    )

    result_rows: list[dict[str, Any]] = []
    for method in ["concat_bm25", "prompt_zsum_bm25"]:
        for alpha in alphas:
            predictions = predictions_from_union_rows(rows, method=method, alpha=alpha, top_k=args.top_k)
            result_rows.append(evaluate_method(method, alpha, predictions, args.bootstrap_samples))

    rrf_predictions = predictions_from_union_rows(rows, method="rrf_prompt3_bm25", alpha=None, top_k=args.top_k)
    result_rows.append(evaluate_method("rrf_prompt3_bm25", None, rrf_predictions, args.bootstrap_samples))

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "tmp_union_top20_prompt_bm25_fusion",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "config": bm25_sweep.config_to_json(config),
            "per_source_top_k": args.per_source_top_k,
            "alphas": alphas,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
        },
        "union_summary": union_summary(rows),
        "source_oracle_summary": source_oracle_summary(rows),
        "source_overlap_summary": source_overlap_summary(rows),
        "gold_source_count_summary": gold_source_count_summary(rows),
        "candidate_agreement_summary": candidate_agreement_summary(rows),
        "agreement_threshold_summary": agreement_threshold_summary(rows),
        "rows": result_rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


def build_config_reprs_cpu(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    config: bm25_sweep.FusionConfig,
) -> list[fusion.VectorRepr]:
    reprs = []
    for cell in config.cells:
        print(f"repr {cell.label}")
        vectors = load_cell_vectors_torch(
            dump_dir,
            manifest,
            records,
            variant=cell.variant,
            layer=cell.layer,
            position="last",
        )
        reprs.append(fusion.build_persistable_repr(cell, vectors, records))
        del vectors
        gc.collect()
    return reprs


def load_cell_vectors_torch(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    *,
    variant: str,
    layer: int,
    position: str,
) -> np.ndarray:
    """Load one bf16 cell through safetensors/torch CPU, avoiding Metal."""

    from safetensors import safe_open

    variant_index = offline.index_of(manifest["prompt_variants"], variant, "variant")
    layer_index = offline.index_of(manifest["layers"], layer, "layer")
    position_index = offline.index_of(manifest["positions"], position, "position")
    hidden_dim = int(manifest["hidden_dim"])
    output = np.empty((len(records), hidden_dim), dtype=np.float32)

    records_by_chunk: dict[str, list[tuple[int, offline.Stage2Record]]] = {}
    for row_index, record in enumerate(records):
        records_by_chunk.setdefault(record.chunk_file, []).append((row_index, record))

    for chunk_file, rows in sorted(records_by_chunk.items()):
        path = dump_dir / chunk_file
        if not path.exists():
            raise FileNotFoundError(f"Manifest chunk is missing: {path}")
        with safe_open(str(path), framework="pt", device="cpu") as handle:
            tensor_slice = handle.get_slice("states")
            cell_tensor = tensor_slice[:, variant_index, layer_index, position_index, :]
            cell_vectors = cell_tensor.float().numpy().astype(np.float32, copy=False)

        output_rows = np.fromiter((row_index for row_index, _record in rows), dtype=np.int64)
        chunk_rows = np.fromiter((record.chunk_index for _row_index, record in rows), dtype=np.int64)
        output[output_rows] = cell_vectors[chunk_rows]
        del cell_tensor, cell_vectors, output_rows, chunk_rows

    if not np.all(np.isfinite(output)):
        raise ValueError(f"Non-finite vector in {variant}|layer{layer}|{position}.")
    return output


def build_union_rows(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    config: bm25_sweep.FusionConfig,
    reprs: list[fusion.VectorRepr],
    *,
    per_source_top_k: int,
) -> list[BucketUnionScores]:
    output: list[BucketUnionScores] = []
    for bucket in buckets.values():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query_record = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        if len(candidate_ids) != len(candidate_records):
            raise ValueError(f"Missing candidate_id in instance {query_record.instance_index}.")

        prompt_scores = [score_single_repr(bucket, repr_) for repr_ in reprs]
        concat_scores = bm25_sweep.score_config_bucket(config, bucket, reprs)
        bm25_scores = full_bm25_scores(query_record, candidate_records)

        source_indices: dict[str, np.ndarray] = {}
        union: set[int] = set()
        for cell, scores in zip(config.cells, prompt_scores, strict=True):
            indices = top_indices(scores, per_source_top_k)
            source_indices[cell.label] = indices
            union.update(int(index) for index in indices)
        bm25_indices = top_indices(bm25_scores, per_source_top_k)
        source_indices["bm25"] = bm25_indices
        union.update(int(index) for index in bm25_indices)

        output.append(
            BucketUnionScores(
                question_id=query_record.question_id,
                candidate_ids=candidate_ids,
                gold_ids=list(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
                union_indices=np.asarray(sorted(union), dtype=np.int64),
                source_indices=source_indices,
                prompt_scores=prompt_scores,
                concat_scores=concat_scores,
                bm25_scores=bm25_scores,
            )
        )
    return output


def score_single_repr(bucket: offline.InstanceBucket, repr_: fusion.VectorRepr) -> np.ndarray:
    query = offline.normalize(repr_.query_vectors[bucket.query_index])
    candidates = offline.normalize(repr_.candidate_vectors[bucket.candidate_indices])
    return candidates @ query


def full_bm25_scores(
    query_record: offline.Stage2Record,
    candidate_records: list[offline.Stage2Record],
) -> np.ndarray:
    texts = [record.text for record in candidate_records]
    scores = np.zeros(len(texts), dtype=np.float64)
    retriever = BM25Retriever().fit(texts)
    for local_rank, score in retriever.query(query_record.text, top_k=len(texts)):
        scores[int(local_rank)] = float(score)
    return scores


def top_indices(scores: np.ndarray, k: int) -> np.ndarray:
    order = np.argsort(scores)[::-1]
    return order[: min(k, len(order))].astype(np.int64, copy=False)


def predictions_from_union_rows(
    rows: list[BucketUnionScores],
    *,
    method: str,
    alpha: float | None,
    top_k: int,
) -> list[Prediction]:
    predictions: list[Prediction] = []
    for row in rows:
        union_indices = row.union_indices
        if method == "concat_bm25":
            assert alpha is not None
            fused = (
                alpha * offline.zscore_1d(row.concat_scores[union_indices])
                + (1.0 - alpha) * offline.zscore_1d(row.bm25_scores[union_indices])
            )
            order = union_indices[np.argsort(fused)[::-1]]
        elif method == "prompt_zsum_bm25":
            assert alpha is not None
            prompt_sum = np.zeros(len(union_indices), dtype=np.float64)
            for scores in row.prompt_scores:
                prompt_sum += offline.zscore_1d(scores[union_indices])
            prompt_sum /= max(len(row.prompt_scores), 1)
            fused = (
                alpha * offline.zscore_1d(prompt_sum)
                + (1.0 - alpha) * offline.zscore_1d(row.bm25_scores[union_indices])
            )
            order = union_indices[np.argsort(fused)[::-1]]
        elif method == "rrf_prompt3_bm25":
            order = rrf_union_order(row)
        else:
            raise ValueError(f"Unsupported method: {method}")

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


def rrf_union_order(row: BucketUnionScores, rrf_k: int = 60) -> np.ndarray:
    scores = {int(index): 0.0 for index in row.union_indices}
    source_scores = [*row.prompt_scores, row.bm25_scores]
    for values in source_scores:
        ranked = np.argsort(values)[::-1]
        for rank, local_index in enumerate(ranked, start=1):
            index = int(local_index)
            if index in scores:
                scores[index] += 1.0 / (rrf_k + rank)
    return np.asarray(sorted(scores, key=scores.get, reverse=True), dtype=np.int64)


def evaluate_method(
    method: str,
    alpha: float | None,
    predictions: list[Prediction],
    bootstrap_samples: int,
) -> dict[str, Any]:
    metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
    session = offline.session_retrieval_metrics(predictions)
    rank = offline.rank_metrics(predictions)
    summary = bm25_sweep.summarize_metrics(metrics, session, rank)
    return {
        "method": method,
        "alpha": alpha,
        "metrics": metrics,
        "session_metrics": session,
        "rank_metrics": rank,
        "summary": summary,
    }


def union_summary(rows: list[BucketUnionScores]) -> dict[str, Any]:
    scored = scored_rows(rows)
    union_sizes = [len(row.union_indices) for row in scored]
    oracle_hits = [gold_in_indices(row.gold_ids, row.candidate_ids, row.union_indices) for row in scored]
    return {
        "n_scored": len(scored),
        "avg_union_size": float(np.mean(union_sizes)) if union_sizes else float("nan"),
        "max_union_size": int(max(union_sizes)) if union_sizes else 0,
        "oracle_recall_all": float(np.mean(oracle_hits)) if oracle_hits else float("nan"),
    }


def source_oracle_summary(rows: list[BucketUnionScores]) -> dict[str, Any]:
    scored = scored_rows(rows)
    if not scored:
        return {}
    source_names = source_names_in_order(scored[0])
    output = {}
    for name in source_names:
        values = [
            gold_in_indices(row.gold_ids, row.candidate_ids, row.source_indices[name])
            for row in scored
        ]
        output[source_alias(name)] = float(np.mean(values))
    return output


def source_overlap_summary(rows: list[BucketUnionScores]) -> list[dict[str, Any]]:
    scored = scored_rows(rows)
    if not scored:
        return []
    output = []
    for left, right in combinations(source_names_in_order(scored[0]), 2):
        intersections = []
        jaccards = []
        for row in scored:
            left_set = set(int(index) for index in row.source_indices[left])
            right_set = set(int(index) for index in row.source_indices[right])
            union = left_set | right_set
            intersections.append(len(left_set & right_set))
            jaccards.append(len(left_set & right_set) / len(union) if union else 0.0)
        output.append(
            {
                "source_a": source_alias(left),
                "source_b": source_alias(right),
                "avg_intersection": float(np.mean(intersections)),
                "avg_jaccard": float(np.mean(jaccards)),
            }
        )
    return output


def gold_source_count_summary(rows: list[BucketUnionScores]) -> dict[str, Any]:
    scored = scored_rows(rows)
    if not scored:
        return {}
    count_hist = {str(index): 0 for index in range(5)}
    combo_counts: dict[str, int] = {}
    for row in scored:
        hit_sources = [
            source_alias(name)
            for name in source_names_in_order(row)
            if gold_in_indices(row.gold_ids, row.candidate_ids, row.source_indices[name])
        ]
        count_hist[str(len(hit_sources))] += 1
        combo = "+".join(hit_sources) if hit_sources else "none"
        combo_counts[combo] = combo_counts.get(combo, 0) + 1
    return {
        "n_scored": len(scored),
        "count_histogram": count_hist,
        "count_fraction": {
            count: value / len(scored)
            for count, value in count_hist.items()
        },
        "top_combinations": [
            {"sources": combo, "count": count, "fraction": count / len(scored)}
            for combo, count in sorted(combo_counts.items(), key=lambda item: item[1], reverse=True)
        ],
    }


def candidate_agreement_summary(rows: list[BucketUnionScores]) -> dict[str, Any]:
    scored = scored_rows(rows)
    if not scored:
        return {}
    gold_hist = {str(index): 0 for index in range(1, 5)}
    non_gold_hist = {str(index): 0 for index in range(1, 5)}
    for row in scored:
        source_sets = source_index_sets(row)
        gold_ids = set(row.gold_ids)
        for index in row.union_indices:
            source_count = sum(int(int(index) in source_set) for source_set in source_sets)
            candidate_id = row.candidate_ids[int(index)]
            target = gold_hist if candidate_id in gold_ids else non_gold_hist
            target[str(source_count)] += 1
    return {
        "gold": histogram_with_fraction(gold_hist),
        "non_gold": histogram_with_fraction(non_gold_hist),
    }


def agreement_threshold_summary(rows: list[BucketUnionScores]) -> list[dict[str, Any]]:
    scored = scored_rows(rows)
    output = []
    for threshold in range(1, 5):
        sizes = []
        oracle_values = []
        for row in scored:
            source_sets = source_index_sets(row)
            kept = np.asarray(
                [
                    int(index)
                    for index in row.union_indices
                    if sum(int(int(index) in source_set) for source_set in source_sets) >= threshold
                ],
                dtype=np.int64,
            )
            sizes.append(len(kept))
            oracle_values.append(gold_in_indices(row.gold_ids, row.candidate_ids, kept))
        output.append(
            {
                "min_source_count": threshold,
                "avg_candidate_count": float(np.mean(sizes)) if sizes else float("nan"),
                "oracle_recall_all": float(np.mean(oracle_values)) if oracle_values else float("nan"),
            }
        )
    return output


def scored_rows(rows: list[BucketUnionScores]) -> list[BucketUnionScores]:
    return [
        row
        for row in rows
        if not row.is_abstention and row.has_target and row.gold_ids
    ]


def gold_in_indices(gold_ids: list[str], candidate_ids: list[str], indices: np.ndarray) -> float:
    retrieved = {candidate_ids[int(index)] for index in indices}
    return float(set(gold_ids).issubset(retrieved)) if gold_ids else 0.0


def source_names_in_order(row: BucketUnionScores) -> list[str]:
    return list(row.source_indices)


def source_index_sets(row: BucketUnionScores) -> list[set[int]]:
    return [
        {int(index) for index in row.source_indices[name]}
        for name in source_names_in_order(row)
    ]


def source_alias(name: str) -> str:
    if name == "bm25":
        return "bm25"
    if name.startswith("2-4-1_user_word"):
        return "user_word"
    if name.startswith("1-3"):
        return "tag_1-3"
    if name.startswith("2-5"):
        return "assoc_2-5"
    return name


def histogram_with_fraction(histogram: dict[str, int]) -> dict[str, Any]:
    total = sum(histogram.values())
    return {
        "count": histogram,
        "fraction": {
            key: (value / total if total else float("nan"))
            for key, value in histogram.items()
        },
        "total": total,
    }


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
    union = payload["union_summary"]
    lines = [
        "# Temporary union top20 prompt + BM25 fusion",
        "",
        "Candidate set per query: top20 from each of the three prompt cells plus top20 BM25, then rerank inside the union.",
        "",
        "## Union Ceiling",
        "",
        f"- avg union size: {union['avg_union_size']:.1f}",
        f"- max union size: {union['max_union_size']}",
        f"- oracle recall_all within union: {union['oracle_recall_all']:.3f}",
        "",
        "## Source Oracle Recall",
        "",
    ]
    for name, value in sorted(payload["source_oracle_summary"].items()):
        lines.append(f"- `{name}`: {value:.3f}")
    lines.extend(
        [
            "",
            "## Source Overlap",
            "",
            "| source A | source B | avg intersection | avg Jaccard |",
            "|---|---|---:|---:|",
        ]
    )
    for row in payload["source_overlap_summary"]:
        lines.append(
            f"| `{row['source_a']}` | `{row['source_b']}` | "
            f"{row['avg_intersection']:.1f} | {row['avg_jaccard']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Gold Covered By Source Count",
            "",
            "| source count | questions | fraction |",
            "|---:|---:|---:|",
        ]
    )
    gold_counts = payload["gold_source_count_summary"]["count_histogram"]
    gold_fracs = payload["gold_source_count_summary"]["count_fraction"]
    for count in sorted(gold_counts, key=lambda item: int(item)):
        lines.append(f"| {count} | {gold_counts[count]} | {gold_fracs[count]:.3f} |")
    lines.extend(
        [
            "",
            "## Top Gold Source Combinations",
            "",
            "| sources covering all gold IDs | questions | fraction |",
            "|---|---:|---:|",
        ]
    )
    for row in payload["gold_source_count_summary"]["top_combinations"][:12]:
        lines.append(f"| `{row['sources']}` | {row['count']} | {row['fraction']:.3f} |")
    lines.extend(
        [
            "",
            "## Candidate Agreement Distribution",
            "",
            "| source count | gold candidates | gold fraction | non-gold candidates | non-gold fraction |",
            "|---:|---:|---:|---:|---:|",
        ]
    )
    gold_agree = payload["candidate_agreement_summary"]["gold"]
    nongold_agree = payload["candidate_agreement_summary"]["non_gold"]
    for count in ["1", "2", "3", "4"]:
        lines.append(
            f"| {count} | {gold_agree['count'][count]} | {gold_agree['fraction'][count]:.3f} | "
            f"{nongold_agree['count'][count]} | {nongold_agree['fraction'][count]:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Agreement Threshold Oracle",
            "",
            "| min source count | avg candidate count | oracle recall_all |",
            "|---:|---:|---:|",
        ]
    )
    for row in payload["agreement_threshold_summary"]:
        lines.append(
            f"| {row['min_source_count']} | {row['avg_candidate_count']:.1f} | "
            f"{row['oracle_recall_all']:.3f} |"
        )
    lines.extend(
        [
            "",
            "## Rerank Results",
            "",
            "| rank | method | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |",
            "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for index, row in enumerate(rows, start=1):
        summary = row["summary"]
        alpha = "" if row["alpha"] is None else f"{row['alpha']:.2f}"
        lines.append(
            f"| {index} | `{row['method']}` | {alpha} | "
            f"{summary['recall_all@3']:.3f} | {summary['ndcg_any@3']:.3f} | "
            f"{summary['recall_all@5']:.3f} | {summary['ndcg_any@5']:.3f} | "
            f"{summary['mrr']:.3f} | {summary['session_hit@5']:.3f} | {summary['n_scored']} |"
        )
    lines.extend(["", "## Inputs", ""])
    lines.append(f"- dump_dir: `{payload['inputs']['dump_dir']}`")
    lines.append(f"- config: `{payload['inputs']['config']['name']}`")
    lines.append(f"- per_source_top_k: {payload['inputs']['per_source_top_k']}")
    lines.append(f"- alphas: {payload['inputs']['alphas']}")
    lines.append(f"- elapsed_seconds: {payload['elapsed_seconds']:.1f}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
