"""Offline PrefEval fusion experiments with an external Qwen embedding cache.

This script does not run any model. It reads:

- PrefEval prepared JSONL rows.
- Saved 9B hidden-state tensors for the K3 prompt retriever.
- A saved `qwen3_embedding_* / embeddings.npz` cache from `prefeval_benchmark.py`.

The purpose is to test whether a small embedding model, such as
Qwen3-Embedding-0.6B-4bit, adds value to the current PrefEval fusion stack as:

1. A top-k candidate source.
2. A score-level fusion feature.

It intentionally avoids vector-concatenating external embeddings with 9B hidden
states because they live in different representation spaces.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np

import prefeval_benchmark as base
import prefeval_stage1_offline as offline


BENCH_DIR = Path(__file__).resolve().parent
DEFAULT_RESULTS_DIR = BENCH_DIR / "results" / "prefeval_stage1"
DEFAULT_COMBO = ("2-3-1_L30_both_k15", "2-5_L29_both_k15", "2-1_L30_both_k5")
SCORE_FUSION_WEIGHTS = (
    ("d0.75_b0.20_e0.05", (0.75, 0.20, 0.05)),
    ("d0.70_b0.20_e0.10", (0.70, 0.20, 0.10)),
    ("d0.70_b0.07_e0.23", (0.70, 0.07, 0.23)),
    ("d0.65_b0.25_e0.10", (0.65, 0.25, 0.10)),
    ("basealpha0.85_base0.75_qwen0.25", (0.6375, 0.1125, 0.25)),
    ("d0.60_b0.25_e0.15", (0.60, 0.25, 0.15)),
    ("d0.60_b0.10_e0.30", (0.60, 0.10, 0.30)),
    ("d0.50_b0.25_e0.25", (0.50, 0.25, 0.25)),
)
K3_BM25_BASE_WEIGHTS = (
    ("k3bm25_075_025", (0.75, 0.25)),
    ("k3bm25_ratio60_10", (0.60 / 0.70, 0.10 / 0.70)),
)
CONCAT_FUSION_WEIGHTS = tuple(
    (
        f"k{k3_weight:.2f}_e{embedding_weight:.2f}_b{bm25_weight:.2f}",
        (k3_weight, embedding_weight, bm25_weight),
    )
    for bm25_weight in (0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30)
    for embedding_weight in (0.10, 0.15, 0.20, 0.25, 0.30, 0.35)
    for k3_weight in (round(1.0 - embedding_weight - bm25_weight, 2),)
    if k3_weight >= 0.35
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared-jsonl", default=str(offline.DEFAULT_PREPARED_JSONL))
    parser.add_argument("--hidden-tensor-dir", default=None, help="Saved n=1000 hidden tensor dir. Defaults to latest main cache.")
    parser.add_argument(
        "--extra-hidden-tensor-dir",
        action="append",
        default=None,
        help="Additional saved hidden tensor dir(s) to search for custom K3 cells.",
    )
    parser.add_argument(
        "--combo-spec",
        action="append",
        default=None,
        help=(
            "Custom K3 dense cell as name,variant,layer,transform,k,family. "
            "Pass exactly three times. Defaults to the standard 2-3-1 + 2-5 + 2-1 combo."
        ),
    )
    parser.add_argument(
        "--embedding-cache-dir",
        default=None,
        help="Saved qwen3_embedding_* cache dir containing embeddings.npz. Defaults to latest matching cache with embeddings.npz.",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_RESULTS_DIR))
    parser.add_argument("--output-prefix", default=None)
    parser.add_argument("--shortlist-size", type=int, default=20)
    parser.add_argument("--source-min", type=int, default=2)
    parser.add_argument(
        "--concat-source-min",
        type=int,
        default=3,
        help="Source-count threshold for concat experiments before always adding embedding top-k.",
    )
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument(
        "--eval-query-split",
        choices=("all", "train700", "holdout300"),
        default="all",
        help="Evaluate all queries or a deterministic random 700/300 query split.",
    )
    parser.add_argument("--split-seed", type=int, default=0)
    parser.add_argument("--train-size", type=int, default=700)
    parser.add_argument(
        "--allow-legacy-hidden-cache",
        action="store_true",
        help=(
            "Allow old hidden tensor manifests that only bind item_ids and do not "
            "store data_fingerprint/text/gold hashes. Use only for known-good caches."
        ),
    )
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def combo_specs_from_args(combo_args: list[str] | None) -> tuple[tuple[str, ...], dict[str, offline.DenseCellSpec], str]:
    if not combo_args:
        specs = {name: offline.DENSE_CELL_LIBRARY[name] for name in DEFAULT_COMBO}
        return DEFAULT_COMBO, specs, " + ".join(spec.variant for spec in specs.values())

    specs: dict[str, offline.DenseCellSpec] = {}
    names: list[str] = []
    for raw in combo_args:
        parts = [part.strip() for part in raw.split(",")]
        if len(parts) != 6:
            raise ValueError(
                "--combo-spec must be name,variant,layer,transform,k,family; "
                f"got {raw!r}"
            )
        name, variant, layer_text, transform, k_text, family = parts
        k_value = None if k_text.lower() in {"", "none", "null"} else int(k_text)
        specs[name] = offline.DenseCellSpec(
            name=name,
            variant=variant,
            layer=int(layer_text),
            transform=transform,
            k=k_value,
            family=family,
        )
        names.append(name)
    return tuple(names), specs, " + ".join(spec.variant for spec in specs.values())


def spec_to_json(spec: offline.DenseCellSpec) -> dict[str, Any]:
    return {
        "name": spec.name,
        "variant": spec.variant,
        "layer": spec.layer,
        "transform": spec.transform,
        "k": spec.k,
        "family": spec.family,
        "storage_label": spec.storage_label,
    }


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    data = offline.load_prepared_jsonl(Path(args.prepared_jsonl))
    hidden_tensor_dir = Path(args.hidden_tensor_dir) if args.hidden_tensor_dir else offline.latest_hidden_tensor_dir()
    extra_hidden_tensor_dirs = [Path(path) for path in (args.extra_hidden_tensor_dir or [])]
    hidden_tensor_dirs = [hidden_tensor_dir, *extra_hidden_tensor_dirs]
    embedding_cache_dir = (
        Path(args.embedding_cache_dir)
        if args.embedding_cache_dir
        else latest_embedding_cache_dir(data)
    )

    hidden_manifests = [
        validate_hidden_cache(data, tensor_dir, allow_legacy=args.allow_legacy_hidden_cache)
        for tensor_dir in hidden_tensor_dirs
    ]
    embedding_manifest = validate_embedding_cache(data, embedding_cache_dir)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_prefix or f"embedding_fusion_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    json_path = output_dir / f"{prefix}.json"
    md_path = output_dir / f"{prefix}.md"
    if not args.overwrite:
        existing = [path for path in (json_path, md_path) if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    base.log("PrefEval external embedding fusion")
    base.log(f"prepared={args.prepared_jsonl}")
    base.log(f"hidden_tensor_dirs={', '.join(str(path) for path in hidden_tensor_dirs)}")
    base.log(f"embedding_cache_dir={embedding_cache_dir}")

    combo_names, specs, combo_label = combo_specs_from_args(args.combo_spec)
    if len(combo_names) != 3:
        raise ValueError(f"This script expects exactly 3 prompt cells for K3; got {len(combo_names)}: {combo_names}")
    loaded = offline.load_dense_specs_from_tensor_dirs(hidden_tensor_dirs, specs)
    component_scores = [loaded[name]["scores"] for name in combo_names]
    dense_scores = offline.score_vector_average([loaded[name] for name in combo_names], component_normalize=True)
    bm25_scores = base.score_bm25(data)
    embedding_candidates, embedding_queries = load_embedding_vectors(embedding_cache_dir)
    embedding_scores = score_embedding_vectors(embedding_candidates, embedding_queries)
    five_source_score = weighted_zsum(
        tuple([*component_scores, bm25_scores, embedding_scores]),
        (0.20, 0.20, 0.20, 0.10, 0.30),
    )

    if embedding_scores.shape != dense_scores.shape:
        raise ValueError(f"Embedding score shape {embedding_scores.shape} != dense score shape {dense_scores.shape}")

    eval_indices, eval_split_name = query_split_indices(
        len(data.query_ids),
        split=args.eval_query_split,
        train_size=args.train_size,
        seed=args.split_seed,
    )
    eval_args = SimpleNamespace(
        top_k=args.top_k,
        bootstrap_samples=args.bootstrap_samples,
        query_indices=eval_indices,
        query_split=eval_split_name,
    )
    rows: list[dict[str, Any]] = []

    rows.append(
        evaluate(
            "k3_custom_vector_average",
            f"K3 dense baseline: {combo_label}, vector_average_component_norm.",
            dense_scores,
            data,
            eval_args,
            {
                "phase": "embedding_fusion_reference",
                "scorer": "vector_average_component_norm",
                "combo": combo_label,
            },
        )
    )
    rows.append(
        evaluate(
            "bm25",
            "BM25 standalone reference.",
            bm25_scores,
            data,
            eval_args,
            {"phase": "embedding_fusion_reference", "scorer": "bm25"},
        )
    )
    rows.append(
        evaluate(
            "external_embedding",
            "External Qwen embedding standalone reference loaded from cache.",
            embedding_scores,
            data,
            eval_args,
            {"phase": "embedding_fusion_reference", "scorer": "embedding_dot"},
        )
    )

    dense_bm25 = weighted_zsum((dense_scores, bm25_scores), (0.75, 0.25))
    rows.append(
        evaluate(
            "k3_bm25_full_d0.75_b0.25",
            "Full-corpus z-score fusion: K3 dense 0.75 + BM25 0.25.",
            dense_bm25,
            data,
            eval_args,
            {"phase": "embedding_fusion_reference", "scope": "full", "dense_weight": 0.75, "bm25_weight": 0.25},
        )
    )

    rows.append(
        evaluate(
            f"k3_bm25_dense_top{args.shortlist_size}_d0.75_b0.25",
            f"Dense top-{args.shortlist_size} shortlist reranked by K3 dense 0.75 + BM25 0.25.",
            offline.shortlist_fusion_scores(dense_scores, bm25_scores, alpha=0.75, shortlist_size=args.shortlist_size),
            data,
            eval_args,
            {
                "phase": "embedding_fusion_reference",
                "scope": "dense_topk",
                "shortlist_size": args.shortlist_size,
                "dense_weight": 0.75,
                "bm25_weight": 0.25,
            },
        )
    )

    for base_name, (k3_weight, bm25_weight) in K3_BM25_BASE_WEIGHTS:
        base_scores = weighted_zsum((dense_scores, bm25_scores), (k3_weight, bm25_weight))
        rows.append(
            evaluate(
                f"result_fusion_{base_name}_slots_1_2_4_5_embedding_slot3",
                (
                    "Result-level fusion: K3+BM25 supplies slots 1/2/4/5, "
                    "external embedding supplies slot 3 using its first non-duplicate candidate."
                ),
                result_slot_injection_scores(base_scores, embedding_scores),
                data,
                eval_args,
                {
                    "phase": "embedding_result_slot_injection",
                    "k3_weight": k3_weight,
                    "bm25_weight": bm25_weight,
                    "embedding_slot": 3,
                    "base_slots": [1, 2, 4, 5],
                },
            )
        )
        embedding_only_scores, embedding_only_stats = embedding_only_rerank_scores(
            base_scores,
            [*component_scores, bm25_scores],
            embedding_scores,
            data,
            shortlist_size=args.shortlist_size,
        )
        rows.append(
            evaluate(
                f"embedding_only_top{args.shortlist_size}_rerank_{base_name}",
                (
                    f"Only candidates that appear in embedding top{args.shortlist_size} and no other source top{args.shortlist_size}; "
                    "rerank by K3+BM25."
                ),
                embedding_only_scores,
                data,
                eval_args,
                {
                    "phase": "embedding_only_rerank",
                    "shortlist_size": args.shortlist_size,
                    "k3_weight": k3_weight,
                    "bm25_weight": bm25_weight,
                    "shortlist_stats": embedding_only_stats,
                },
            )
        )
        source_ge3_plus_embedding_only, source_ge3_plus_embedding_only_stats = source_agreement_plus_embedding_only_scores(
            base_scores,
            [*component_scores, bm25_scores, embedding_scores],
            [*component_scores, bm25_scores],
            embedding_scores,
            data,
            shortlist_size=args.shortlist_size,
            min_sources=args.concat_source_min,
        )
        rows.append(
            evaluate(
                f"source_ge{args.concat_source_min}_plus_embedding_only_top{args.shortlist_size}_rerank_{base_name}",
                (
                    f"Candidate set=top{args.shortlist_size} source_count>={args.concat_source_min} plus embedding-only top{args.shortlist_size}; "
                    "rerank by K3+BM25."
                ),
                source_ge3_plus_embedding_only,
                data,
                eval_args,
                {
                    "phase": "source_agreement_plus_embedding_only_rerank",
                    "source_rule": f"source_ge{args.concat_source_min}_plus_embedding_only_top{args.shortlist_size}",
                    "shortlist_size": args.shortlist_size,
                    "k3_weight": k3_weight,
                    "bm25_weight": bm25_weight,
                    "shortlist_stats": source_ge3_plus_embedding_only_stats,
                },
            )
        )

    for source_topk in (3, 5, 10):
        topk_union_scores, topk_union_stats = source_union_rerank_scores(
            five_source_score,
            [*component_scores, bm25_scores, embedding_scores],
            data,
            source_topk=source_topk,
        )
        rows.append(
            evaluate(
                f"five_source_top{source_topk}_union_ge1_score_fusion_k0.60_e0.30_b0.10",
                (
                    f"Union of each source top{source_topk} with source_count>=1; "
                    "rerank by five-source score fusion: prompt sources total 0.60, embedding 0.30, BM25 0.10."
                ),
                topk_union_scores,
                data,
                eval_args,
                {
                    "phase": "small_topk_source_union_score_fusion",
                    "source_rule": "source_ge1",
                    "source_count": 5,
                    "source_topk": source_topk,
                    "source_weights": [0.20, 0.20, 0.20, 0.10, 0.30],
                    "shortlist_stats": topk_union_stats,
                },
            )
        )

    source_baseline, source_baseline_stats = offline.source_agreement_rerank_scores(
        dense_bm25,
        [*component_scores, bm25_scores],
        data,
        shortlist_size=args.shortlist_size,
        min_sources=args.source_min,
    )
    rows.append(
        evaluate(
            f"four_source_top{args.shortlist_size}_source_ge{args.source_min}_rerank_d0.75_b0.25",
            f"Four-source candidate screening: 3 prompt sources + BM25, source_count>={args.source_min}, rerank=K3/BM25.",
            source_baseline,
            data,
            eval_args,
            {
                "phase": "embedding_topk_source_baseline",
                "source_count": 4,
                "source_rule": f"source_ge{args.source_min}",
                "shortlist_size": args.shortlist_size,
                "shortlist_stats": source_baseline_stats,
            },
        )
    )

    source_with_embedding, source_with_embedding_stats = offline.source_agreement_rerank_scores(
        dense_bm25,
        [*component_scores, bm25_scores, embedding_scores],
        data,
        shortlist_size=args.shortlist_size,
        min_sources=args.source_min,
    )
    rows.append(
        evaluate(
            f"five_source_top{args.shortlist_size}_source_ge{args.source_min}_rerank_d0.75_b0.25",
            f"Five-source candidate screening: 3 prompt sources + BM25 + external embedding, source_count>={args.source_min}, rerank=K3/BM25.",
            source_with_embedding,
            data,
            eval_args,
            {
                "phase": "embedding_topk_source",
                "source_count": 5,
                "source_rule": f"source_ge{args.source_min}",
                "shortlist_size": args.shortlist_size,
                "shortlist_stats": source_with_embedding_stats,
            },
        )
    )

    for weight_name, weights in SCORE_FUSION_WEIGHTS:
        dense_weight, bm25_weight, embedding_weight = weights
        full_scores = weighted_zsum((dense_scores, bm25_scores, embedding_scores), weights)
        rows.append(
            evaluate(
                f"k3_bm25_embedding_full_{weight_name}",
                (
                    "Full-corpus z-score fusion: "
                    f"K3 dense {dense_weight:.2f} + BM25 {bm25_weight:.2f} + embedding {embedding_weight:.2f}."
                ),
                full_scores,
                data,
                eval_args,
                {
                    "phase": "embedding_score_fusion",
                    "scope": "full",
                    "dense_weight": dense_weight,
                    "bm25_weight": bm25_weight,
                    "embedding_weight": embedding_weight,
                },
            )
        )
        source_rerank, source_stats = offline.source_agreement_rerank_scores(
            full_scores,
            [*component_scores, bm25_scores, embedding_scores],
            data,
            shortlist_size=args.shortlist_size,
            min_sources=args.source_min,
        )
        rows.append(
            evaluate(
                f"five_source_top{args.shortlist_size}_source_ge{args.source_min}_rerank_{weight_name}",
                (
                    f"Five-source candidate screening with same score rerank: source_count>={args.source_min}, "
                    f"K3 dense {dense_weight:.2f} + BM25 {bm25_weight:.2f} + embedding {embedding_weight:.2f}."
                ),
                source_rerank,
                data,
                eval_args,
                {
                    "phase": "embedding_topk_source_score_fusion",
                    "source_count": 5,
                    "source_rule": f"source_ge{args.source_min}",
                    "shortlist_size": args.shortlist_size,
                    "dense_weight": dense_weight,
                    "bm25_weight": bm25_weight,
                    "embedding_weight": embedding_weight,
                    "shortlist_stats": source_stats,
                },
            )
        )

    k3_candidates_raw, k3_queries_raw = k3_vector_average_vectors(
        [loaded[name] for name in combo_names],
        component_normalize=True,
        final_normalize=False,
    )
    k3_candidates_norm = base.normalize_rows(k3_candidates_raw)
    k3_queries_norm = base.normalize_rows(k3_queries_raw)
    embedding_candidates_norm = base.normalize_rows(embedding_candidates)
    embedding_queries_norm = base.normalize_rows(embedding_queries)
    for weight_name, weights in CONCAT_FUSION_WEIGHTS:
        k3_weight, embedding_weight, bm25_weight = weights
        dense_weight = k3_weight + embedding_weight
        concat_scores = {
            "norm_first": score_weighted_concat(
                k3_candidates_norm,
                k3_queries_norm,
                embedding_candidates_norm,
                embedding_queries_norm,
                k3_weight=k3_weight,
                embedding_weight=embedding_weight,
            ),
            "concat_first": score_weighted_concat(
                k3_candidates_raw,
                k3_queries_raw,
                embedding_candidates,
                embedding_queries,
                k3_weight=k3_weight,
                embedding_weight=embedding_weight,
            ),
        }
        score_level = weighted_zsum((dense_scores, embedding_scores, bm25_scores), weights)
        for concat_mode, concat_score in concat_scores.items():
            rerank_scores = dense_weight * base.row_zscore(concat_score) + bm25_weight * base.row_zscore(bm25_scores)
            screened_scores, screened_stats = source_agreement_plus_embedding_scores(
                rerank_scores,
                [*component_scores, bm25_scores, embedding_scores],
                embedding_scores,
                data,
                shortlist_size=args.shortlist_size,
                min_sources=args.concat_source_min,
            )
            rows.append(
                evaluate(
                    (
                        f"k3_embedding_concat_{concat_mode}_bm25_"
                        f"source_ge{args.concat_source_min}_plus_embedding_top{args.shortlist_size}_{weight_name}"
                    ),
                    (
                        f"K3 vector average + external embedding weighted concat ({concat_mode}), then BM25 score fusion; "
                        f"candidate set=top{args.shortlist_size} source_count>={args.concat_source_min} plus embedding top{args.shortlist_size}."
                    ),
                    screened_scores,
                    data,
                    eval_args,
                    {
                        "phase": "embedding_vector_concat_source_screen",
                        "concat_mode": concat_mode,
                        "source_count": 5,
                        "source_rule": f"source_ge{args.concat_source_min}_plus_embedding_top{args.shortlist_size}",
                        "shortlist_size": args.shortlist_size,
                        "k3_weight": k3_weight,
                        "embedding_weight": embedding_weight,
                        "bm25_weight": bm25_weight,
                        "dense_weight_after_concat": dense_weight,
                        "shortlist_stats": screened_stats,
                    },
                )
            )
        screened_score_level, screened_score_level_stats = source_agreement_plus_embedding_scores(
            score_level,
            [*component_scores, bm25_scores, embedding_scores],
            embedding_scores,
            data,
            shortlist_size=args.shortlist_size,
            min_sources=args.concat_source_min,
        )
        rows.append(
            evaluate(
                f"k3_embedding_score_zfusion_bm25_source_ge{args.concat_source_min}_plus_embedding_top{args.shortlist_size}_{weight_name}",
                (
                    f"Score-level z-fusion baseline for the same candidate set: K3 {k3_weight:.2f} + "
                    f"embedding {embedding_weight:.2f} + BM25 {bm25_weight:.2f}."
                ),
                screened_score_level,
                data,
                eval_args,
                {
                    "phase": "embedding_score_fusion_source_screen",
                    "source_count": 5,
                    "source_rule": f"source_ge{args.concat_source_min}_plus_embedding_top{args.shortlist_size}",
                    "shortlist_size": args.shortlist_size,
                    "k3_weight": k3_weight,
                    "embedding_weight": embedding_weight,
                    "bm25_weight": bm25_weight,
                    "shortlist_stats": screened_score_level_stats,
                },
            )
        )

    payload = {
        "created_utc": base.now_utc(),
        "analysis": "prefeval_embedding_fusion",
        "inputs": {
            "prepared_jsonl": args.prepared_jsonl,
            "hidden_tensor_dir": str(hidden_tensor_dir),
            "hidden_tensor_dirs": [str(path) for path in hidden_tensor_dirs],
            "hidden_model_paths": [manifest.get("model_path") for manifest in hidden_manifests],
            "hidden_cache_has_data_fingerprint": all(bool(manifest.get("data_fingerprint")) for manifest in hidden_manifests),
            "embedding_cache_dir": str(embedding_cache_dir),
            "embedding_model_path": embedding_manifest.get("model_path"),
            "embedding_backend": embedding_manifest.get("backend"),
            "combo": combo_label,
            "combo_specs": [spec_to_json(spec) for spec in specs.values()],
            "shortlist_size": args.shortlist_size,
            "source_min": args.source_min,
            "concat_source_min": args.concat_source_min,
            "bootstrap_samples": args.bootstrap_samples,
            "top_k": args.top_k,
            "eval_query_split": eval_split_name,
            "split_seed": args.split_seed,
            "train_size": args.train_size,
        },
        "task_summary": {
            "task": data.task,
            "dataset_id": data.dataset_id,
            "items": len(data.items),
            "candidate_count": len(data.candidate_ids),
            "query_count": len(data.query_ids),
            "gold_policy": "prepared_jsonl_gold_ids",
        },
        "notes": [
            "External embeddings are used only as a score matrix/source, not concatenated with 9B hidden vectors.",
            f"Primary K3 dense baseline is {combo_label} with vector_average_component_norm.",
            "source_count>=2 experiments use per-source top-k lists, with prompt components kept as separate sources.",
            "Concat experiments use source_count>=concat_source_min plus embedding top-k candidates, then rerank only that candidate set.",
        ],
        "rows": sorted(rows, key=lambda row: (row["summary"]["recall_all@5"], row["summary"]["ndcg_any@5"]), reverse=True),
        "elapsed_seconds": time.monotonic() - started,
    }
    json_path.write_text(json.dumps(base.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    base.log(f"wrote {json_path}")
    base.log(f"wrote {md_path}")
    return 0


def latest_embedding_cache_dir(data: base.BenchmarkData) -> Path:
    pattern = f"qwen3_embedding_{data.task}_n{len(data.items)}_*"
    candidates = [
        path
        for path in (BENCH_DIR / "tensors").glob(pattern)
        if (path / "embeddings.npz").exists() and (path / "manifest.json").exists()
    ]
    if not candidates:
        raise FileNotFoundError(
            "No matching embedding cache with embeddings.npz found. Run prefeval_benchmark.py "
            "with --retrievers qwen3_embedding_bm25 first, or pass --embedding-cache-dir."
        )
    return sorted(candidates, key=lambda path: path.stat().st_mtime, reverse=True)[0]


def query_split_indices(
    query_count: int,
    *,
    split: str,
    train_size: int,
    seed: int,
) -> tuple[list[int] | None, str]:
    if split == "all":
        return None, "all"
    if train_size <= 0 or train_size >= query_count:
        raise ValueError(f"train_size must be between 1 and query_count-1; got {train_size} for {query_count}")
    rng = np.random.default_rng(seed)
    permutation = rng.permutation(query_count)
    if split == "train700":
        return sorted(int(index) for index in permutation[:train_size]), f"train{train_size}_seed{seed}"
    if split == "holdout300":
        return sorted(int(index) for index in permutation[train_size:]), f"holdout{query_count - train_size}_seed{seed}"
    raise ValueError(f"Unknown split: {split}")


def validate_hidden_cache(data: base.BenchmarkData, tensor_dir: Path, *, allow_legacy: bool) -> dict[str, Any]:
    manifest = offline.load_manifest(tensor_dir)
    item_ids = [item.item_id for item in data.items]
    if manifest.get("item_ids") != item_ids:
        raise ValueError("Hidden tensor item_ids do not match prepared JSONL.")
    if manifest.get("task") and manifest["task"] != data.task:
        raise ValueError(f"Hidden tensor task mismatch: {manifest['task']} != {data.task}")
    if manifest.get("dataset_id") and manifest["dataset_id"] != data.dataset_id:
        raise ValueError(f"Hidden tensor dataset mismatch: {manifest['dataset_id']} != {data.dataset_id}")
    expected_fingerprint = base.benchmark_data_fingerprint(data)
    manifest_fingerprint = manifest.get("data_fingerprint")
    if manifest_fingerprint:
        if manifest_fingerprint != expected_fingerprint:
            raise ValueError(
                "Hidden tensor data_fingerprint does not match prepared JSONL "
                f"(prepared={expected_fingerprint}, cache={manifest_fingerprint})."
            )
        return manifest
    if not allow_legacy:
        raise ValueError(
            "Hidden tensor manifest lacks data_fingerprint/text/gold hashes. "
            "This old cache can only be used with --allow-legacy-hidden-cache after manually confirming it matches."
        )
    base.log(
        "warning: using legacy hidden tensor cache without data_fingerprint; "
        "item_ids/task/dataset matched, but text/gold binding is not available in this old manifest"
    )
    return manifest


def validate_embedding_cache(data: base.BenchmarkData, cache_dir: Path) -> dict[str, Any]:
    manifest_path = cache_dir / "manifest.json"
    vectors_path = cache_dir / "embeddings.npz"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing embedding manifest: {manifest_path}")
    if not vectors_path.exists():
        raise FileNotFoundError(f"Missing embedding vectors: {vectors_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")).get("expected", {})
    expected_fingerprint = base.benchmark_data_fingerprint(data)
    if manifest.get("item_ids") != [item.item_id for item in data.items]:
        raise ValueError("Embedding cache item_ids do not match prepared JSONL.")
    if manifest.get("data_fingerprint") != expected_fingerprint:
        raise ValueError(
            "Embedding cache data_fingerprint does not match prepared JSONL "
            f"(prepared={expected_fingerprint}, cache={manifest.get('data_fingerprint')})."
        )
    return manifest


def load_embedding_vectors(cache_dir: Path) -> tuple[np.ndarray, np.ndarray]:
    with np.load(cache_dir / "embeddings.npz") as arrays:
        candidates = np.asarray(arrays["candidate_embeddings"], dtype=np.float32)
        queries = np.asarray(arrays["query_embeddings"], dtype=np.float32)
    return candidates, queries


def score_embedding_vectors(candidates: np.ndarray, queries: np.ndarray) -> np.ndarray:
    # The benchmark cache is already normalized, but normalize defensively so
    # caches from older scripts remain comparable.
    return base.normalize_rows(queries) @ base.normalize_rows(candidates).T


def k3_vector_average_vectors(
    combo_specs: list[dict[str, Any]],
    *,
    component_normalize: bool,
    final_normalize: bool,
) -> tuple[np.ndarray, np.ndarray]:
    candidate_parts = []
    query_parts = []
    for item in combo_specs:
        candidates = item["candidates"]
        queries = item["queries"]
        if component_normalize:
            candidates = base.normalize_rows(candidates)
            queries = base.normalize_rows(queries)
        candidate_parts.append(candidates)
        query_parts.append(queries)
    candidate_vectors = np.mean(np.stack(candidate_parts, axis=0), axis=0).astype(np.float32, copy=False)
    query_vectors = np.mean(np.stack(query_parts, axis=0), axis=0).astype(np.float32, copy=False)
    if final_normalize:
        candidate_vectors = base.normalize_rows(candidate_vectors)
        query_vectors = base.normalize_rows(query_vectors)
    return candidate_vectors, query_vectors


def score_weighted_concat(
    k3_candidates: np.ndarray,
    k3_queries: np.ndarray,
    embedding_candidates: np.ndarray,
    embedding_queries: np.ndarray,
    *,
    k3_weight: float,
    embedding_weight: float,
) -> np.ndarray:
    if k3_candidates.shape[0] != embedding_candidates.shape[0] or k3_queries.shape[0] != embedding_queries.shape[0]:
        raise ValueError(
            "K3 and embedding vector row counts differ: "
            f"k3_candidates={k3_candidates.shape}, embedding_candidates={embedding_candidates.shape}, "
            f"k3_queries={k3_queries.shape}, embedding_queries={embedding_queries.shape}"
        )
    k3_scale = np.sqrt(np.float32(k3_weight))
    embedding_scale = np.sqrt(np.float32(embedding_weight))
    candidates = np.concatenate(
        [k3_scale * k3_candidates.astype(np.float32, copy=False), embedding_scale * embedding_candidates.astype(np.float32, copy=False)],
        axis=1,
    )
    queries = np.concatenate(
        [k3_scale * k3_queries.astype(np.float32, copy=False), embedding_scale * embedding_queries.astype(np.float32, copy=False)],
        axis=1,
    )
    return base.normalize_rows(queries) @ base.normalize_rows(candidates).T


def weighted_zsum(score_matrices: tuple[np.ndarray, ...], weights: tuple[float, ...]) -> np.ndarray:
    output = np.zeros_like(score_matrices[0], dtype=np.float32)
    for weight, scores in zip(weights, score_matrices, strict=True):
        output += np.float32(weight) * base.row_zscore(scores)
    return output


def source_agreement_plus_embedding_scores(
    rerank_scores: np.ndarray,
    source_scores: list[np.ndarray],
    embedding_scores: np.ndarray,
    data: base.BenchmarkData,
    *,
    shortlist_size: int,
    min_sources: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    query_count, candidate_count = rerank_scores.shape
    output = np.empty_like(rerank_scores, dtype=np.float32)
    shortlist_sizes: list[int] = []
    oracle_hits = 0
    source_ge_hits = 0
    embedding_only_gold_hits = 0
    for query_index in range(query_count):
        base_order = np.argsort(rerank_scores[query_index])[::-1]
        output[query_index, base_order] = -1_000_000.0 - np.arange(candidate_count, dtype=np.float32)
        source_counts: dict[int, int] = {}
        embedding_top = set(int(index) for index in np.argsort(embedding_scores[query_index])[::-1][:shortlist_size])
        for source in source_scores:
            order = np.argsort(source[query_index])[::-1][:shortlist_size]
            for candidate_index in order:
                index = int(candidate_index)
                source_counts[index] = source_counts.get(index, 0) + 1
        source_ge = {index for index, count in source_counts.items() if count >= min_sources}
        shortlist = source_ge | embedding_top
        shortlist_indices = np.asarray(sorted(shortlist), dtype=np.int32)
        shortlist_sizes.append(int(shortlist_indices.size))
        gold = set(data.gold_ids_by_query[query_index])
        if shortlist_indices.size:
            retrieved = {data.candidate_ids[int(index)] for index in shortlist_indices}
            oracle_hits += int(bool(gold & retrieved))
            source_ge_retrieved = {data.candidate_ids[int(index)] for index in source_ge}
            embedding_only_retrieved = {data.candidate_ids[int(index)] for index in (embedding_top - source_ge)}
            source_ge_hits += int(bool(gold & source_ge_retrieved))
            embedding_only_gold_hits += int(bool(gold & embedding_only_retrieved))
            output[query_index, shortlist_indices] = (
                1_000_000.0 + offline.zscore_1d(rerank_scores[query_index, shortlist_indices])
            )
    stats = {
        "avg_shortlist_size": float(np.mean(shortlist_sizes)) if shortlist_sizes else 0.0,
        "min_shortlist_size": int(min(shortlist_sizes)) if shortlist_sizes else 0,
        "max_shortlist_size": int(max(shortlist_sizes)) if shortlist_sizes else 0,
        "oracle_hit": float(oracle_hits / max(query_count, 1)),
        "source_ge_oracle_hit": float(source_ge_hits / max(query_count, 1)),
        "embedding_only_added_oracle_hit": float(embedding_only_gold_hits / max(query_count, 1)),
        "min_sources": min_sources,
        "per_source_topk": shortlist_size,
        "plus_embedding_topk": shortlist_size,
    }
    return output, stats


def result_slot_injection_scores(
    base_scores: np.ndarray,
    embedding_scores: np.ndarray,
) -> np.ndarray:
    if base_scores.shape != embedding_scores.shape:
        raise ValueError(f"Score matrices differ: {base_scores.shape} vs {embedding_scores.shape}")
    query_count, candidate_count = base_scores.shape
    output = np.empty_like(base_scores, dtype=np.float32)
    for query_index in range(query_count):
        base_order = [int(index) for index in np.argsort(base_scores[query_index])[::-1]]
        embedding_order = [int(index) for index in np.argsort(embedding_scores[query_index])[::-1]]
        final_order: list[int] = []
        used: set[int] = set()

        for index in base_order:
            final_order.append(index)
            used.add(index)
            if len(final_order) == 2:
                break

        for index in embedding_order:
            if index not in used:
                final_order.append(index)
                used.add(index)
                break

        for index in base_order:
            if index not in used:
                final_order.append(index)
                used.add(index)
            if len(final_order) == 5:
                break

        for index in base_order:
            if index not in used:
                final_order.append(index)
                used.add(index)

        output[query_index, np.asarray(final_order, dtype=np.int32)] = (
            1_000_000.0 - np.arange(len(final_order), dtype=np.float32)
        )
    return output


def embedding_only_rerank_scores(
    rerank_scores: np.ndarray,
    non_embedding_sources: list[np.ndarray],
    embedding_scores: np.ndarray,
    data: base.BenchmarkData,
    *,
    shortlist_size: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    query_count, candidate_count = rerank_scores.shape
    output = np.empty_like(rerank_scores, dtype=np.float32)
    shortlist_sizes: list[int] = []
    oracle_hits = 0
    for query_index in range(query_count):
        base_order = np.argsort(rerank_scores[query_index])[::-1]
        output[query_index, base_order] = -1_000_000.0 - np.arange(candidate_count, dtype=np.float32)
        embedding_top = set(int(index) for index in np.argsort(embedding_scores[query_index])[::-1][:shortlist_size])
        other_top: set[int] = set()
        for source in non_embedding_sources:
            other_top.update(int(index) for index in np.argsort(source[query_index])[::-1][:shortlist_size])
        shortlist = embedding_top - other_top
        shortlist_indices = np.asarray(sorted(shortlist), dtype=np.int32)
        shortlist_sizes.append(int(shortlist_indices.size))
        if shortlist_indices.size:
            gold = set(data.gold_ids_by_query[query_index])
            retrieved = {data.candidate_ids[int(index)] for index in shortlist_indices}
            oracle_hits += int(bool(gold & retrieved))
            output[query_index, shortlist_indices] = (
                1_000_000.0 + offline.zscore_1d(rerank_scores[query_index, shortlist_indices])
            )
    return output, {
        "avg_shortlist_size": float(np.mean(shortlist_sizes)) if shortlist_sizes else 0.0,
        "min_shortlist_size": int(min(shortlist_sizes)) if shortlist_sizes else 0,
        "max_shortlist_size": int(max(shortlist_sizes)) if shortlist_sizes else 0,
        "oracle_hit": float(oracle_hits / max(query_count, 1)),
        "per_source_topk": shortlist_size,
    }


def source_agreement_plus_embedding_only_scores(
    rerank_scores: np.ndarray,
    all_sources: list[np.ndarray],
    non_embedding_sources: list[np.ndarray],
    embedding_scores: np.ndarray,
    data: base.BenchmarkData,
    *,
    shortlist_size: int,
    min_sources: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    query_count, candidate_count = rerank_scores.shape
    output = np.empty_like(rerank_scores, dtype=np.float32)
    shortlist_sizes: list[int] = []
    oracle_hits = 0
    source_ge_hits = 0
    embedding_only_added_hits = 0
    for query_index in range(query_count):
        base_order = np.argsort(rerank_scores[query_index])[::-1]
        output[query_index, base_order] = -1_000_000.0 - np.arange(candidate_count, dtype=np.float32)
        source_counts: dict[int, int] = {}
        for source in all_sources:
            for index in np.argsort(source[query_index])[::-1][:shortlist_size]:
                candidate_index = int(index)
                source_counts[candidate_index] = source_counts.get(candidate_index, 0) + 1
        source_ge = {index for index, count in source_counts.items() if count >= min_sources}
        embedding_top = set(int(index) for index in np.argsort(embedding_scores[query_index])[::-1][:shortlist_size])
        other_top: set[int] = set()
        for source in non_embedding_sources:
            other_top.update(int(index) for index in np.argsort(source[query_index])[::-1][:shortlist_size])
        embedding_only = embedding_top - other_top
        shortlist = source_ge | embedding_only
        shortlist_indices = np.asarray(sorted(shortlist), dtype=np.int32)
        shortlist_sizes.append(int(shortlist_indices.size))
        if shortlist_indices.size:
            gold = set(data.gold_ids_by_query[query_index])
            retrieved = {data.candidate_ids[int(index)] for index in shortlist_indices}
            source_ge_retrieved = {data.candidate_ids[int(index)] for index in source_ge}
            embedding_only_retrieved = {data.candidate_ids[int(index)] for index in embedding_only}
            oracle_hits += int(bool(gold & retrieved))
            source_ge_hits += int(bool(gold & source_ge_retrieved))
            embedding_only_added_hits += int(bool(gold & embedding_only_retrieved))
            output[query_index, shortlist_indices] = (
                1_000_000.0 + offline.zscore_1d(rerank_scores[query_index, shortlist_indices])
            )
    return output, {
        "avg_shortlist_size": float(np.mean(shortlist_sizes)) if shortlist_sizes else 0.0,
        "min_shortlist_size": int(min(shortlist_sizes)) if shortlist_sizes else 0,
        "max_shortlist_size": int(max(shortlist_sizes)) if shortlist_sizes else 0,
        "oracle_hit": float(oracle_hits / max(query_count, 1)),
        "source_ge_oracle_hit": float(source_ge_hits / max(query_count, 1)),
        "embedding_only_added_oracle_hit": float(embedding_only_added_hits / max(query_count, 1)),
        "min_sources": min_sources,
        "per_source_topk": shortlist_size,
    }


def source_union_rerank_scores(
    rerank_scores: np.ndarray,
    source_scores: list[np.ndarray],
    data: base.BenchmarkData,
    *,
    source_topk: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    query_count, candidate_count = rerank_scores.shape
    output = np.empty_like(rerank_scores, dtype=np.float32)
    shortlist_sizes: list[int] = []
    oracle_hits = 0
    for query_index in range(query_count):
        base_order = np.argsort(rerank_scores[query_index])[::-1]
        output[query_index, base_order] = -1_000_000.0 - np.arange(candidate_count, dtype=np.float32)
        shortlist: set[int] = set()
        for source in source_scores:
            shortlist.update(int(index) for index in np.argsort(source[query_index])[::-1][:source_topk])
        shortlist_indices = np.asarray(sorted(shortlist), dtype=np.int32)
        shortlist_sizes.append(int(shortlist_indices.size))
        if shortlist_indices.size:
            gold = set(data.gold_ids_by_query[query_index])
            retrieved = {data.candidate_ids[int(index)] for index in shortlist_indices}
            oracle_hits += int(bool(gold & retrieved))
            output[query_index, shortlist_indices] = (
                1_000_000.0 + offline.zscore_1d(rerank_scores[query_index, shortlist_indices])
            )
    return output, {
        "avg_shortlist_size": float(np.mean(shortlist_sizes)) if shortlist_sizes else 0.0,
        "min_shortlist_size": int(min(shortlist_sizes)) if shortlist_sizes else 0,
        "max_shortlist_size": int(max(shortlist_sizes)) if shortlist_sizes else 0,
        "oracle_hit": float(oracle_hits / max(query_count, 1)),
        "per_source_topk": source_topk,
        "min_sources": 1,
    }


def evaluate(
    name: str,
    description: str,
    scores: np.ndarray,
    data: base.BenchmarkData,
    eval_args: argparse.Namespace,
    extra: dict[str, Any],
) -> dict[str, Any]:
    indices = getattr(eval_args, "query_indices", None)
    split_name = getattr(eval_args, "query_split", "all")
    eval_data = data
    eval_scores = scores
    if indices is not None:
        eval_scores = scores[indices]
        eval_data = offline.subset_queries(data, indices)
    row = base.evaluate_score_matrix(name, description, eval_scores, eval_data, eval_args, extra=extra)
    row["split"] = split_name
    return row


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# PrefEval External Embedding Fusion",
        "",
        f"- Created UTC: `{payload['created_utc']}`",
        f"- Items: `{payload['task_summary']['items']}`",
        f"- Hidden tensor dir: `{payload['inputs']['hidden_tensor_dir']}`",
        f"- K3 combo: `{payload['inputs'].get('combo')}`",
        f"- Embedding cache dir: `{payload['inputs']['embedding_cache_dir']}`",
        f"- Embedding model: `{payload['inputs'].get('embedding_model_path')}`",
        f"- Source rule: `top{payload['inputs']['shortlist_size']} source_count>={payload['inputs']['source_min']}`",
        f"- Eval split: `{payload['inputs'].get('eval_query_split', 'all')}`",
        f"- Elapsed: `{base.fmt_duration(float(payload.get('elapsed_seconds', 0.0)))}`",
        "",
        "## Notes",
        "",
    ]
    lines.extend(f"- {note}" for note in payload.get("notes", []))
    lines.extend(
        [
            "",
            "## Results",
            "",
            "| rank | config | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR | avg shortlist | oracle@shortlist |",
            "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for index, row in enumerate(payload["rows"], start=1):
        summary = row["summary"]
        shortlist_stats = row.get("shortlist_stats", {})
        avg_shortlist = shortlist_stats.get("avg_shortlist_size")
        oracle = shortlist_stats.get("oracle_hit")
        avg_text = "" if avg_shortlist is None else f"{avg_shortlist:.1f}"
        oracle_text = "" if oracle is None else f"{oracle:.3f}"
        lines.append(
            f"| {index} | `{row['name']}` | {summary['recall_all@1']:.3f} | "
            f"{summary['recall_all@3']:.3f} | {summary['recall_all@5']:.3f} | "
            f"{summary['ndcg_any@3']:.3f} | {summary['ndcg_any@5']:.3f} | "
            f"{summary['mrr']:.3f} | {avg_text} | {oracle_text} |"
        )
    lines.extend(["", "## Configs", ""])
    for row in payload["rows"]:
        lines.append(f"- `{row['name']}`: {row['description']}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
