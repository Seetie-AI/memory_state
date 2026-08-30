"""Cross-benchmark prompt-pool overlap and combo analysis.

This is a focused offline analysis for the prompt pool that looked promising
on both LongMemEval and PrefEval:

- 2-3-1
- 2-3-2_query
- 2-5
- 1-3
- 2-1

It intentionally does not run any model. LongMemEval vectors are loaded through
safetensors/torch on CPU to avoid requiring MLX/Metal in headless sessions.
PrefEval vectors are loaded from the saved n=1000 PromptReps NPZ cache.
"""

from __future__ import annotations

import argparse
import gc
import itertools
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
PREFEVAL_DIR = ROOT / "benchmarks" / "PrefEval"
for path in (SCRIPTS, SRC, PREFEVAL_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import stage2_offline_analyze as lme_offline
import stage3_prompt_fusion_analyze as lme_fusion
import union_top20_prompt_bm25_fusion as lme_cpu
from eval.longmemeval_metrics import Prediction, evaluate

import prefeval_benchmark as pref_base
import prefeval_stage1_offline as pref_offline


DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "prompt_fusion"
DEFAULT_OUTPUT_PREFIX = "crossbench_prompt_pool_20260512"


@dataclass
class LmeBucketScores:
    question_id: str
    candidate_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool
    scores_by_prompt: dict[str, np.ndarray]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lme-dump-dir", default=str(lme_fusion.DEFAULT_DUMP_DIR))
    parser.add_argument("--lme-data", default=str(lme_fusion.DEFAULT_DATA))
    parser.add_argument("--pref-prepared-jsonl", default=str(pref_offline.DEFAULT_PREPARED_JSONL))
    parser.add_argument("--pref-tensor-dir", default=None)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=200)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in (json_path, md_path) if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite: {existing}")

    print("running LongMemEval prompt-pool analysis")
    lme_payload = run_longmemeval(args)
    gc.collect()
    print("running PrefEval prompt-pool analysis")
    pref_payload = run_prefeval(args)

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "crossbench_prompt_pool_overlap_combo",
        "inputs": {
            "lme_dump_dir": str(Path(args.lme_dump_dir)),
            "lme_data": str(Path(args.lme_data)),
            "pref_prepared_jsonl": str(Path(args.pref_prepared_jsonl)),
            "pref_tensor_dir": str(Path(args.pref_tensor_dir)) if args.pref_tensor_dir else None,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
        },
        "longmemeval": lme_payload,
        "prefeval": pref_payload,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


def run_longmemeval(args: argparse.Namespace) -> dict[str, Any]:
    dump_dir = Path(args.lme_dump_dir)
    manifest = lme_offline.load_manifest(dump_dir)
    lme_offline.validate_manifest(manifest)
    records = lme_offline.load_records(dump_dir, manifest, Path(args.lme_data))
    buckets = lme_offline.group_by_instance(records)

    # Configs follow the best R@3 cells from the current Stage 3 merged table.
    cells = [
        lme_fusion.CellConfig("2-3-1", 31, "anti_pca_both_k15", "memory-key"),
        lme_fusion.CellConfig("2-3-2_query", 30, "anti_pca_both_k15", "query-key"),
        lme_fusion.CellConfig("2-5", 29, "query_only_anti_pca_k2", "association"),
        lme_fusion.CellConfig("1-3", 31, "anti_pca_both_k15", "fact-tag"),
        lme_fusion.CellConfig("2-1", 31, "anti_pca_both_k15", "topic"),
    ]
    reprs: dict[str, lme_fusion.VectorRepr] = {}
    for cell in cells:
        print(f"  LME repr {cell.label}")
        vectors = lme_cpu.load_cell_vectors_torch(
            dump_dir,
            manifest,
            records,
            variant=cell.variant,
            layer=cell.layer,
            position="last",
        )
        reprs[cell.variant] = lme_fusion.build_persistable_repr(cell, vectors, records)
        del vectors
        gc.collect()

    score_rows = build_lme_score_rows(records, buckets, reprs)
    single_rows = [
        evaluate_lme_scores(f"single_{name}", [name], score_rows, args.bootstrap_samples, method="single", top_k=args.top_k)
        for name in reprs
    ]
    pairwise = pairwise_overlap_lme(score_rows, list(reprs), top_values=(3, 5))
    oracle_combos = oracle_combo_coverage_lme(score_rows, list(reprs), combo_sizes=(2, 3), top_values=(3, 5))
    combo_rows = []
    for k in (2, 3):
        for names in itertools.combinations(list(reprs), k):
            combo_reprs = [reprs[name] for name in names]
            for method in ("zsum", "vertical_concat_norm_weighted", "vertical_concat_component_norm", "vector_average_component_norm"):
                combo_rows.append(
                    evaluate_lme_combo(
                        names,
                        method,
                        records,
                        buckets,
                        score_rows,
                        combo_reprs,
                        args.bootstrap_samples,
                        args.top_k,
                    )
                )
    combo_rows.sort(key=lambda row: (row["summary"]["recall_all@3"], row["summary"]["ndcg_any@3"], row["summary"]["recall_all@5"]), reverse=True)
    return {
        "cells": [cell_to_json(cell) for cell in cells],
        "single_rows": sorted(single_rows, key=lambda row: (row["summary"]["recall_all@3"], row["summary"]["ndcg_any@3"]), reverse=True),
        "pairwise": pairwise,
        "oracle_combos": oracle_combos,
        "combo_rows": combo_rows,
        "n_records": len(records),
        "n_queries": len(score_rows),
    }


def build_lme_score_rows(
    records: list[lme_offline.Stage2Record],
    buckets: dict[int, lme_offline.InstanceBucket],
    reprs: dict[str, lme_fusion.VectorRepr],
) -> list[LmeBucketScores]:
    rows = []
    for bucket in buckets.values():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query_record = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        if len(candidate_ids) != len(candidate_records):
            raise ValueError(f"Missing candidate_id in instance {query_record.instance_index}.")
        scores_by_prompt = {}
        for name, repr_ in reprs.items():
            query = lme_offline.normalize(repr_.query_vectors[bucket.query_index])
            candidates = lme_offline.normalize(repr_.candidate_vectors[bucket.candidate_indices])
            scores_by_prompt[name] = candidates @ query
        rows.append(
            LmeBucketScores(
                question_id=query_record.question_id,
                candidate_ids=candidate_ids,
                gold_ids=list(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
                scores_by_prompt=scores_by_prompt,
            )
        )
    return rows


def evaluate_lme_scores(
    name: str,
    prompt_names: list[str],
    rows: list[LmeBucketScores],
    bootstrap_samples: int,
    *,
    method: str,
    top_k: int,
) -> dict[str, Any]:
    predictions = []
    for row in rows:
        if method == "single":
            scores = row.scores_by_prompt[prompt_names[0]]
        elif method == "zsum":
            scores = np.zeros_like(row.scores_by_prompt[prompt_names[0]], dtype=np.float32)
            for prompt_name in prompt_names:
                scores += zscore_1d(row.scores_by_prompt[prompt_name])
        else:
            raise ValueError(f"Unsupported LME score-row method: {method}")
        order = np.argsort(scores)[::-1]
        predictions.append(
            Prediction(
                question_id=row.question_id,
                retrieved_ids=[row.candidate_ids[int(index)] for index in order[:top_k]],
                gold_ids=row.gold_ids,
                is_abstention=row.is_abstention,
                has_target=row.has_target,
            )
        )
    metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
    session_metrics = lme_offline.session_retrieval_metrics(predictions)
    rank_metrics = lme_offline.rank_metrics(predictions)
    return {
        "name": name,
        "prompts": prompt_names,
        "method": method,
        "summary": lme_fusion.summarize_metrics(metrics, session_metrics, rank_metrics),
        "metrics": metrics,
        "session_metrics": session_metrics,
        "rank_metrics": rank_metrics,
    }


def evaluate_lme_combo(
    prompt_names: tuple[str, ...],
    method: str,
    records: list[lme_offline.Stage2Record],
    buckets: dict[int, lme_offline.InstanceBucket],
    score_rows: list[LmeBucketScores],
    reprs: list[lme_fusion.VectorRepr],
    bootstrap_samples: int,
    top_k: int,
) -> dict[str, Any]:
    if method == "zsum":
        return evaluate_lme_scores(
            f"{method}_{'+'.join(prompt_names)}",
            list(prompt_names),
            score_rows,
            bootstrap_samples,
            method="zsum",
            top_k=top_k,
        )
    predictions = lme_fusion.predictions_from_vector_fusion(
        records,
        buckets,
        reprs,
        method=method,
        top_k=top_k,
    )
    metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
    session_metrics = lme_offline.session_retrieval_metrics(predictions)
    rank_metrics = lme_offline.rank_metrics(predictions)
    return {
        "name": f"{method}_{'+'.join(prompt_names)}",
        "prompts": list(prompt_names),
        "method": method,
        "summary": lme_fusion.summarize_metrics(metrics, session_metrics, rank_metrics),
        "metrics": metrics,
        "session_metrics": session_metrics,
        "rank_metrics": rank_metrics,
    }


def run_prefeval(args: argparse.Namespace) -> dict[str, Any]:
    prepared_jsonl = Path(args.pref_prepared_jsonl)
    tensor_dir = Path(args.pref_tensor_dir) if args.pref_tensor_dir else pref_offline.latest_hidden_tensor_dir()
    data = pref_offline.load_prepared_jsonl(prepared_jsonl)
    manifest = pref_offline.load_manifest(tensor_dir)
    pref_offline.validate_inputs(data, manifest)
    vectors_path = tensor_dir / "raw_hidden_vectors.npz"
    if not vectors_path.exists():
        raise FileNotFoundError(f"Missing PrefEval vectors: {vectors_path}")

    # Configs follow the best R@3/R@5 cells from the n=1000 prompt sweep.
    specs = {
        "2-3-1": pref_offline.DenseCellSpec("2-3-1_L30_both_k15", "2-3-1", 30, "anti_pca_both", 15, "memory-key"),
        "2-3-2_query": pref_offline.DenseCellSpec(
            "2-3-2_query_L30_both_k15", "2-3-2_query", 30, "anti_pca_both", 15, "query-key"
        ),
        "2-5": pref_offline.DenseCellSpec("2-5_L29_both_k15", "2-5", 29, "anti_pca_both", 15, "association"),
        "1-3": pref_offline.DenseCellSpec("1-3_L30_both_k15", "1-3", 30, "anti_pca_both", 15, "fact-tag"),
        "2-1": pref_offline.DenseCellSpec("2-1_L30_both_k15", "2-1", 30, "anti_pca_both", 15, "topic"),
    }
    with np.load(vectors_path) as arrays:
        loaded = pref_offline.load_dense_specs(arrays, {spec.name: spec for spec in specs.values()})
    by_prompt = {spec.variant: loaded[spec.name] for spec in specs.values()}

    eval_args = argparse.Namespace(top_k=args.top_k, bootstrap_samples=args.bootstrap_samples)
    single_rows = [
        evaluate_pref_matrix(f"single_{name}", by_prompt[name]["scores"], data, eval_args, "single", [name])
        for name in by_prompt
    ]
    pairwise = pairwise_overlap_pref(data, by_prompt, top_values=(3, 5))
    oracle_combos = oracle_combo_coverage_pref(data, by_prompt, combo_sizes=(2, 3), top_values=(3, 5))
    combo_rows = []
    prompt_names = list(by_prompt)
    for k in (2, 3):
        for names in itertools.combinations(prompt_names, k):
            combo_items = [by_prompt[name] for name in names]
            matrices = {
                "zsum": pref_score_zsum(combo_items),
                "vertical_concat_norm_weighted": pref_score_vertical_concat(combo_items, component_normalize=False),
                "vertical_concat_component_norm": pref_score_vertical_concat(combo_items, component_normalize=True),
                "vector_average_component_norm": pref_score_vector_average(combo_items, component_normalize=True),
            }
            for method, scores in matrices.items():
                combo_rows.append(evaluate_pref_matrix(f"{method}_{'+'.join(names)}", scores, data, eval_args, method, list(names)))
    combo_rows.sort(key=lambda row: (row["summary"]["recall_all@3"], row["summary"]["ndcg_any@3"], row["summary"]["recall_all@5"]), reverse=True)
    return {
        "cells": [dense_cell_to_json(spec) for spec in specs.values()],
        "single_rows": sorted(single_rows, key=lambda row: (row["summary"]["recall_all@3"], row["summary"]["ndcg_any@3"]), reverse=True),
        "pairwise": pairwise,
        "oracle_combos": oracle_combos,
        "combo_rows": combo_rows,
        "n_queries": len(data.query_ids),
        "n_candidates": len(data.candidate_ids),
    }


def evaluate_pref_matrix(
    name: str,
    scores: np.ndarray,
    data: pref_base.BenchmarkData,
    eval_args: argparse.Namespace,
    method: str,
    prompts: list[str],
) -> dict[str, Any]:
    row = pref_base.evaluate_score_matrix(name, f"{method} {'+'.join(prompts)}", scores, data, eval_args, extra={})
    return {
        "name": name,
        "prompts": prompts,
        "method": method,
        "summary": row["summary"],
        "metrics": row["metrics"],
    }


def pref_score_zsum(combo_items: list[dict[str, Any]]) -> np.ndarray:
    output = np.zeros_like(combo_items[0]["scores"], dtype=np.float32)
    for item in combo_items:
        output += pref_base.row_zscore(item["scores"])
    return output


def pref_score_vertical_concat(combo_items: list[dict[str, Any]], *, component_normalize: bool) -> np.ndarray:
    candidate_parts = []
    query_parts = []
    for item in combo_items:
        candidates = item["candidates"]
        queries = item["queries"]
        if component_normalize:
            candidates = pref_base.normalize_rows(candidates)
            queries = pref_base.normalize_rows(queries)
        candidate_parts.append(candidates)
        query_parts.append(queries)
    candidates = pref_base.normalize_rows(np.concatenate(candidate_parts, axis=1))
    queries = pref_base.normalize_rows(np.concatenate(query_parts, axis=1))
    return queries @ candidates.T


def pref_score_vector_average(combo_items: list[dict[str, Any]], *, component_normalize: bool) -> np.ndarray:
    candidate_parts = []
    query_parts = []
    for item in combo_items:
        candidates = item["candidates"]
        queries = item["queries"]
        if component_normalize:
            candidates = pref_base.normalize_rows(candidates)
            queries = pref_base.normalize_rows(queries)
        candidate_parts.append(candidates)
        query_parts.append(queries)
    candidates = pref_base.normalize_rows(np.mean(np.stack(candidate_parts, axis=0), axis=0))
    queries = pref_base.normalize_rows(np.mean(np.stack(query_parts, axis=0), axis=0))
    return queries @ candidates.T


def pairwise_overlap_lme(
    rows: list[LmeBucketScores],
    prompt_names: list[str],
    *,
    top_values: tuple[int, ...],
) -> list[dict[str, Any]]:
    output = []
    valid_rows = [row for row in rows if not row.is_abstention and row.has_target]
    for left, right in itertools.combinations(prompt_names, 2):
        item: dict[str, Any] = {"left": left, "right": right}
        for top_n in top_values:
            item.update(overlap_for_lme_pair(valid_rows, left, right, top_n))
        output.append(item)
    return sorted(output, key=lambda row: (row["top3_union_hit"], -row["top3_jaccard"]), reverse=True)


def oracle_combo_coverage_lme(
    rows: list[LmeBucketScores],
    prompt_names: list[str],
    *,
    combo_sizes: tuple[int, ...],
    top_values: tuple[int, ...],
) -> list[dict[str, Any]]:
    valid_rows = [row for row in rows if not row.is_abstention and row.has_target]
    output = []
    for size in combo_sizes:
        for combo in itertools.combinations(prompt_names, size):
            item: dict[str, Any] = {"prompts": list(combo), "k": size}
            for top_n in top_values:
                item.update(oracle_combo_for_lme(valid_rows, combo, top_n))
            output.append(item)
    return sorted(output, key=lambda row: (row["top3_union_hit"], row["top5_union_hit"]), reverse=True)


def oracle_combo_for_lme(rows: list[LmeBucketScores], combo: tuple[str, ...], top_n: int) -> dict[str, Any]:
    hit_counts = []
    union_hits = 0
    component_hits = {name: 0 for name in combo}
    pair_jaccards = []
    for row in rows:
        gold = set(row.gold_ids)
        union_ids: set[str] = set()
        per_prompt_sets = []
        per_query_hit_count = 0
        for name in combo:
            ids = top_ids(row.candidate_ids, row.scores_by_prompt[name], top_n)
            per_prompt_sets.append(ids)
            union_ids.update(ids)
            hit = bool(gold & ids)
            component_hits[name] += int(hit)
            per_query_hit_count += int(hit)
        hit_counts.append(per_query_hit_count)
        union_hits += int(bool(gold & union_ids))
        for left, right in itertools.combinations(per_prompt_sets, 2):
            pair_jaccards.append(jaccard(left, right))
    total = max(len(rows), 1)
    prefix = f"top{top_n}"
    return {
        f"{prefix}_union_hit": union_hits / total,
        f"{prefix}_best_component_hit": max(component_hits.values()) / total if component_hits else 0.0,
        f"{prefix}_gain_vs_best": (union_hits - max(component_hits.values(), default=0)) / total,
        f"{prefix}_mean_source_hits_when_gold_found": float(np.mean([count for count in hit_counts if count > 0])) if any(hit_counts) else 0.0,
        f"{prefix}_mean_pairwise_jaccard": float(np.mean(pair_jaccards)) if pair_jaccards else 0.0,
    }


def overlap_for_lme_pair(rows: list[LmeBucketScores], left: str, right: str, top_n: int) -> dict[str, float]:
    jaccards = []
    left_hits = right_hits = only_left = only_right = both = union = 0
    for row in rows:
        gold = set(row.gold_ids)
        left_ids = top_ids(row.candidate_ids, row.scores_by_prompt[left], top_n)
        right_ids = top_ids(row.candidate_ids, row.scores_by_prompt[right], top_n)
        jaccards.append(jaccard(left_ids, right_ids))
        lhit = bool(gold & left_ids)
        rhit = bool(gold & right_ids)
        left_hits += int(lhit)
        right_hits += int(rhit)
        only_left += int(lhit and not rhit)
        only_right += int(rhit and not lhit)
        both += int(lhit and rhit)
        union += int(lhit or rhit)
    total = max(len(rows), 1)
    prefix = f"top{top_n}"
    return {
        f"{prefix}_jaccard": float(np.mean(jaccards)) if jaccards else 0.0,
        f"{prefix}_left_hit": left_hits / total,
        f"{prefix}_right_hit": right_hits / total,
        f"{prefix}_only_left": only_left / total,
        f"{prefix}_only_right": only_right / total,
        f"{prefix}_both_hit": both / total,
        f"{prefix}_union_hit": union / total,
    }


def pairwise_overlap_pref(
    data: pref_base.BenchmarkData,
    by_prompt: dict[str, dict[str, Any]],
    *,
    top_values: tuple[int, ...],
) -> list[dict[str, Any]]:
    output = []
    prompt_names = list(by_prompt)
    for left, right in itertools.combinations(prompt_names, 2):
        item: dict[str, Any] = {"left": left, "right": right}
        for top_n in top_values:
            item.update(overlap_for_pref_pair(data, by_prompt[left]["scores"], by_prompt[right]["scores"], top_n))
        output.append(item)
    return sorted(output, key=lambda row: (row["top3_union_hit"], -row["top3_jaccard"]), reverse=True)


def oracle_combo_coverage_pref(
    data: pref_base.BenchmarkData,
    by_prompt: dict[str, dict[str, Any]],
    *,
    combo_sizes: tuple[int, ...],
    top_values: tuple[int, ...],
) -> list[dict[str, Any]]:
    output = []
    prompt_names = list(by_prompt)
    for size in combo_sizes:
        for combo in itertools.combinations(prompt_names, size):
            item: dict[str, Any] = {"prompts": list(combo), "k": size}
            for top_n in top_values:
                item.update(oracle_combo_for_pref(data, by_prompt, combo, top_n))
            output.append(item)
    return sorted(output, key=lambda row: (row["top3_union_hit"], row["top5_union_hit"]), reverse=True)


def oracle_combo_for_pref(
    data: pref_base.BenchmarkData,
    by_prompt: dict[str, dict[str, Any]],
    combo: tuple[str, ...],
    top_n: int,
) -> dict[str, Any]:
    hit_counts = []
    union_hits = 0
    component_hits = {name: 0 for name in combo}
    pair_jaccards = []
    for query_index in range(len(data.query_ids)):
        gold = set(data.gold_ids_by_query[query_index])
        union_ids: set[str] = set()
        per_prompt_sets = []
        per_query_hit_count = 0
        for name in combo:
            ids = top_ids(data.candidate_ids, by_prompt[name]["scores"][query_index], top_n)
            per_prompt_sets.append(ids)
            union_ids.update(ids)
            hit = bool(gold & ids)
            component_hits[name] += int(hit)
            per_query_hit_count += int(hit)
        hit_counts.append(per_query_hit_count)
        union_hits += int(bool(gold & union_ids))
        for left, right in itertools.combinations(per_prompt_sets, 2):
            pair_jaccards.append(jaccard(left, right))
    total = max(len(data.query_ids), 1)
    prefix = f"top{top_n}"
    return {
        f"{prefix}_union_hit": union_hits / total,
        f"{prefix}_best_component_hit": max(component_hits.values()) / total if component_hits else 0.0,
        f"{prefix}_gain_vs_best": (union_hits - max(component_hits.values(), default=0)) / total,
        f"{prefix}_mean_source_hits_when_gold_found": float(np.mean([count for count in hit_counts if count > 0])) if any(hit_counts) else 0.0,
        f"{prefix}_mean_pairwise_jaccard": float(np.mean(pair_jaccards)) if pair_jaccards else 0.0,
    }


def overlap_for_pref_pair(
    data: pref_base.BenchmarkData,
    left_scores: np.ndarray,
    right_scores: np.ndarray,
    top_n: int,
) -> dict[str, float]:
    jaccards = []
    left_hits = right_hits = only_left = only_right = both = union = 0
    for query_index in range(len(data.query_ids)):
        gold = set(data.gold_ids_by_query[query_index])
        left_ids = top_ids(data.candidate_ids, left_scores[query_index], top_n)
        right_ids = top_ids(data.candidate_ids, right_scores[query_index], top_n)
        jaccards.append(jaccard(left_ids, right_ids))
        lhit = bool(gold & left_ids)
        rhit = bool(gold & right_ids)
        left_hits += int(lhit)
        right_hits += int(rhit)
        only_left += int(lhit and not rhit)
        only_right += int(rhit and not lhit)
        both += int(lhit and rhit)
        union += int(lhit or rhit)
    total = max(len(data.query_ids), 1)
    prefix = f"top{top_n}"
    return {
        f"{prefix}_jaccard": float(np.mean(jaccards)) if jaccards else 0.0,
        f"{prefix}_left_hit": left_hits / total,
        f"{prefix}_right_hit": right_hits / total,
        f"{prefix}_only_left": only_left / total,
        f"{prefix}_only_right": only_right / total,
        f"{prefix}_both_hit": both / total,
        f"{prefix}_union_hit": union / total,
    }


def top_ids(candidate_ids: list[str], scores: np.ndarray, top_n: int) -> set[str]:
    order = np.argsort(scores)[::-1][: min(top_n, len(scores))]
    return {candidate_ids[int(index)] for index in order}


def jaccard(left: set[str], right: set[str]) -> float:
    denom = len(left | right)
    return 0.0 if denom == 0 else len(left & right) / denom


def zscore_1d(scores: np.ndarray) -> np.ndarray:
    scores = np.asarray(scores, dtype=np.float32)
    std = float(np.std(scores))
    if std <= 1e-12:
        return np.zeros_like(scores, dtype=np.float32)
    return ((scores - float(np.mean(scores))) / std).astype(np.float32, copy=False)


def cell_to_json(cell: lme_fusion.CellConfig) -> dict[str, Any]:
    return {
        "variant": cell.variant,
        "layer": cell.layer,
        "score_mode": cell.score_mode,
        "family": cell.family,
        "label": cell.label,
    }


def dense_cell_to_json(cell: pref_offline.DenseCellSpec) -> dict[str, Any]:
    return {
        "name": cell.name,
        "variant": cell.variant,
        "layer": cell.layer,
        "transform": cell.transform,
        "k": cell.k,
        "family": cell.family,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Cross-Benchmark Prompt Pool Analysis",
        "",
        f"- Created UTC: `{payload['created_utc']}`",
        f"- Elapsed: `{format_seconds(payload['elapsed_seconds'])}`",
        "",
        "Prompt pool: `2-3-1`, `2-3-2_query`, `2-5`, `1-3`, `2-1`.",
        "",
    ]
    lines.extend(render_dataset_section("LongMemEval", payload["longmemeval"]))
    lines.extend(render_dataset_section("PrefEval", payload["prefeval"]))
    return "\n".join(lines) + "\n"


def render_dataset_section(title: str, data: dict[str, Any]) -> list[str]:
    lines = [f"## {title}", ""]
    lines.extend(["### Cells", "", "| prompt | config |", "|---|---|"])
    for cell in data["cells"]:
        if "score_mode" in cell:
            config = f"L{cell['layer']} {cell['score_mode']}"
            prompt = cell["variant"]
        else:
            config = f"L{cell['layer']} {cell['transform']}_k{cell['k']}"
            prompt = cell["variant"]
        lines.append(f"| `{prompt}` | {config} |")
    lines.extend(["", "### Single Prompt By R@3", "", *render_rows(data["single_rows"], limit=10)])
    lines.extend(["", "### Pairwise Overlap @3", "", *render_pairwise(data["pairwise"], top_key="top3", limit=10)])
    lines.extend(["", "### Oracle Combo Coverage", "", *render_oracle_combos(data.get("oracle_combos", []), limit=10)])
    lines.extend(["", "### Top Combos By R@3", "", *render_rows(data["combo_rows"], limit=15)])
    lines.append("")
    return lines


def render_rows(rows: list[dict[str, Any]], *, limit: int) -> list[str]:
    lines = ["| rank | method | prompts | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR |", "|---:|---|---|---:|---:|---:|---:|---:|"]
    for index, row in enumerate(rows[:limit], start=1):
        summary = row["summary"]
        prompts = "+".join(row["prompts"])
        lines.append(
            "| {rank} | `{method}` | `{prompts}` | {r3:.3f} | {n3:.3f} | {r5:.3f} | {n5:.3f} | {mrr:.3f} |".format(
                rank=index,
                method=row["method"],
                prompts=prompts,
                r3=summary.get("recall_all@3", 0.0),
                n3=summary.get("ndcg_any@3", 0.0),
                r5=summary.get("recall_all@5", 0.0),
                n5=summary.get("ndcg_any@5", 0.0),
                mrr=summary.get("mrr", 0.0),
            )
        )
    return lines


def render_pairwise(rows: list[dict[str, Any]], *, top_key: str, limit: int) -> list[str]:
    lines = [
        "| pair | jaccard | left_hit | right_hit | only_left | only_right | both | union |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows[:limit]:
        lines.append(
            "| `{left}+{right}` | {j:.3f} | {lh:.3f} | {rh:.3f} | {ol:.3f} | {or_:.3f} | {both:.3f} | {union:.3f} |".format(
                left=row["left"],
                right=row["right"],
                j=row[f"{top_key}_jaccard"],
                lh=row[f"{top_key}_left_hit"],
                rh=row[f"{top_key}_right_hit"],
                ol=row[f"{top_key}_only_left"],
                or_=row[f"{top_key}_only_right"],
                both=row[f"{top_key}_both_hit"],
                union=row[f"{top_key}_union_hit"],
            )
        )
    return lines


def render_oracle_combos(rows: list[dict[str, Any]], *, limit: int) -> list[str]:
    lines = [
        "| rank | prompts | top3_union | top3_gain | top3_jaccard | top5_union | top5_gain | top5_jaccard |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(rows[:limit], start=1):
        lines.append(
            "| {rank} | `{prompts}` | {t3:.3f} | {g3:.3f} | {j3:.3f} | {t5:.3f} | {g5:.3f} | {j5:.3f} |".format(
                rank=index,
                prompts="+".join(row["prompts"]),
                t3=row["top3_union_hit"],
                g3=row["top3_gain_vs_best"],
                j3=row["top3_mean_pairwise_jaccard"],
                t5=row["top5_union_hit"],
                g5=row["top5_gain_vs_best"],
                j5=row["top5_mean_pairwise_jaccard"],
            )
        )
    return lines


def format_seconds(seconds: float) -> str:
    seconds_int = int(round(seconds))
    minutes, secs = divmod(seconds_int, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minutes:02d}m{secs:02d}s"
    if minutes:
        return f"{minutes}m{secs:02d}s"
    return f"{secs}s"


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
