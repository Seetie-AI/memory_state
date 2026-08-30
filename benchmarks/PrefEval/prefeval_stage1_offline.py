"""Offline PrefEval Stage 1 analysis over saved hidden/logit tensors.

This entry point intentionally does not run the 9B model. It reads the raw
hidden states saved by `prefeval_benchmark.py` and applies retrieval transforms
offline. The first Stage 1 pass calibrates whether PrefEval prefers raw cosine,
mean-centering, anti-PCA with a different k, or the query-only simplification
that transferred well from the LongMemEval stages.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np

import prefeval_benchmark as base


BENCH_DIR = Path(__file__).resolve().parent
ROOT = BENCH_DIR.parents[1]
DEFAULT_PREPARED_JSONL = (
    BENCH_DIR
    / "data"
    / "implicit_persona_n1000_pruned_hidden_l28_l29_l30_l31_logits256_promptreps128_20260512.jsonl"
)
DEFAULT_RESULTS_DIR = BENCH_DIR / "results" / "prefeval_stage1"
DEFAULT_FINDINGS = ROOT / "notes" / "prefeval_n1000_findings.md"
ANTI_PCA_KS = (2, 5, 10, 15, 20, 30, 50)
COMBO_SWEEP_SCORERS = ("zsum", "vertical_concat_norm_weighted", "vector_average_component_norm")
WEIGHT_SWEEP_BM25_WEIGHTS = (0.05, 0.10, 0.15, 0.20, 0.25)
WEIGHT_SWEEP_LOGITS_WEIGHTS = (0.0, 0.05, 0.10, 0.15)
CALIBRATION_CELLS = (
    ("2-3-1", 30, "memory-key"),
    ("2-3-2_query", 30, "query-key"),
    ("2-5", 29, "association"),
    ("2-1", 30, "topic"),
)


@dataclass(frozen=True)
class DenseCellSpec:
    name: str
    variant: str
    layer: int
    transform: str
    k: int | None
    family: str

    @property
    def storage_label(self) -> str:
        # The NPZ keys use the original prompt-sweep cell labels. The saved
        # arrays are raw hidden states, so offline transforms may differ from
        # this storage label.
        return f"{self.variant}|L{self.layer}|anti_pca_both_k15"


DENSE_CELL_LIBRARY = {
    "2-3-1_L30_both_k15": DenseCellSpec("2-3-1_L30_both_k15", "2-3-1", 30, "anti_pca_both", 15, "memory-key"),
    "2-3-2_query_L30_both_k15": DenseCellSpec("2-3-2_query_L30_both_k15", "2-3-2_query", 30, "anti_pca_both", 15, "query-key"),
    "2-5_L29_both_k15": DenseCellSpec("2-5_L29_both_k15", "2-5", 29, "anti_pca_both", 15, "association"),
    "2-1_L30_both_k5": DenseCellSpec("2-1_L30_both_k5", "2-1", 30, "anti_pca_both", 5, "topic"),
    "1-2_L30_both_k15": DenseCellSpec("1-2_L30_both_k15", "1-2", 30, "anti_pca_both", 15, "summary"),
    "2-4-1_user_word_L30_both_k15": DenseCellSpec(
        "2-4-1_user_word_L30_both_k15", "2-4-1_user_word", 30, "anti_pca_both", 15, "legacy-user"
    ),
    "1-3_L31_both_k15": DenseCellSpec("1-3_L31_both_k15", "1-3", 31, "anti_pca_both", 15, "legacy-tag"),
    "2-5_L29_query_only_k2": DenseCellSpec("2-5_L29_query_only_k2", "2-5", 29, "anti_pca_query_only", 2, "legacy-association"),
    "2-7_L30_both_k15": DenseCellSpec("2-7_L30_both_k15", "2-7", 30, "anti_pca_both", 15, "interaction"),
}
COMBO_SWEEP_CELL_NAMES = tuple(
    name for name in DENSE_CELL_LIBRARY if name != "2-7_L30_both_k15"
)

DENSE_K3_COMBOS = {
    "k3_key_query_assoc": ("2-3-1_L30_both_k15", "2-3-2_query_L30_both_k15", "2-5_L29_both_k15"),
    "k3_key_assoc_topic": ("2-3-1_L30_both_k15", "2-5_L29_both_k15", "2-1_L30_both_k5"),
    "k3_key_assoc_interaction": ("2-3-1_L30_both_k15", "2-5_L29_both_k15", "2-7_L30_both_k15"),
    "k3_key_assoc_summary": ("2-3-1_L30_both_k15", "2-5_L29_both_k15", "1-2_L30_both_k15"),
    "k3_longmemeval_legacy": (
        "2-4-1_user_word_L30_both_k15",
        "1-3_L31_both_k15",
        "2-5_L29_query_only_k2",
    ),
}
LOGITS_K3_COMBOS = {
    "k3_key_assoc_topic": ("2-3-1_L30_both_k15", "2-5_L29_both_k15", "2-1_L30_both_k5"),
    "k3_key_assoc_tag": ("2-3-1_L30_both_k15", "2-5_L29_both_k15", "1-3_L31_both_k15"),
}
LOGITS_K3_WEIGHT_GRID = (
    (0.50, 0.25, 0.25),
    (0.60, 0.25, 0.15),
    (0.65, 0.25, 0.10),
    (0.70, 0.20, 0.10),
    (0.75, 0.20, 0.05),
)
FIVE_SOURCE_WEIGHT_GRID = (
    ("equal", (0.20, 0.20, 0.20, 0.20, 0.20), 0.60, 0.20, 0.20),
    ("d0.75_b0.20_l0.05", (0.25, 0.25, 0.25, 0.20, 0.05), 0.75, 0.20, 0.05),
    ("d0.70_b0.20_l0.10", (0.70 / 3.0, 0.70 / 3.0, 0.70 / 3.0, 0.20, 0.10), 0.70, 0.20, 0.10),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared-jsonl", default=str(DEFAULT_PREPARED_JSONL))
    parser.add_argument("--tensor-dir", default=None, help="Saved hidden tensor dir. Defaults to latest n=1000 PromptReps cache.")
    parser.add_argument(
        "--extra-tensor-dir",
        action="append",
        default=None,
        help="Additional saved hidden tensor dir(s) for offline phases that can load dense cells from multiple caches.",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_RESULTS_DIR))
    parser.add_argument("--output-prefix", default=None)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument(
        "--phase",
        choices=["anti_pca", "dense_k3", "promptreps", "bm25", "layer_overlap", "combo_sweep", "logits_k3"],
        default="anti_pca",
        help="Offline phase to run. Stage 1 starts with anti-PCA calibration.",
    )
    parser.add_argument(
        "--combo-top-n",
        type=int,
        default=8,
        help="For --phase combo_sweep, run BM25/PromptReps weight sweep on the top N dense K3 rows.",
    )
    parser.add_argument(
        "--combo-selection-split",
        choices=["all", "first500"],
        default="first500",
        help="Split used to select top dense K3 rows before the weight sweep.",
    )
    parser.add_argument(
        "--shortlist-size",
        type=int,
        default=20,
        help="Top-N per source for logits shortlist screening in --phase combo_sweep.",
    )
    parser.add_argument(
        "--screen-alpha",
        type=float,
        default=0.80,
        help="Dense weight for dense+BM25 reranking after shortlist screening.",
    )
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    prepared_jsonl = Path(args.prepared_jsonl)
    tensor_dir = Path(args.tensor_dir) if args.tensor_dir else latest_hidden_tensor_dir()
    tensor_dirs = [tensor_dir, *[Path(path) for path in (args.extra_tensor_dir or [])]]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_prefix or f"{args.phase}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    json_path = output_dir / f"{prefix}.json"
    md_path = output_dir / f"{prefix}.md"
    if not args.overwrite:
        existing = [path for path in (json_path, md_path) if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    data = load_prepared_jsonl(prepared_jsonl)
    manifest = load_manifest(tensor_dir)
    validate_inputs(data, manifest)
    for extra_tensor_dir in tensor_dirs[1:]:
        validate_inputs(data, load_manifest(extra_tensor_dir))
    base.log(f"PrefEval Stage 1 offline phase={args.phase}")
    base.log(f"prepared={prepared_jsonl}")
    base.log(f"tensor_dir={tensor_dir}")
    if len(tensor_dirs) > 1:
        base.log(f"extra_tensor_dirs={[str(path) for path in tensor_dirs[1:]]}")

    if args.phase == "anti_pca":
        rows = run_anti_pca_calibration(tensor_dir, data, args)
        analysis = "prefeval_stage1_anti_pca_calibration"
        extra_payload: dict[str, Any] = {}
    elif args.phase == "dense_k3":
        rows, extra_payload = run_dense_k3(tensor_dirs, data, args)
        analysis = "prefeval_stage1_dense_k3"
    elif args.phase == "promptreps":
        rows, extra_payload = run_promptreps(tensor_dir, data, args)
        analysis = "prefeval_stage1_promptreps"
    elif args.phase == "bm25":
        rows, extra_payload = run_bm25_fusion(tensor_dir, data, args)
        analysis = "prefeval_stage1_bm25_fusion"
    elif args.phase == "layer_overlap":
        rows, extra_payload = run_layer_overlap(tensor_dir, data, args)
        analysis = "prefeval_stage1_layer_overlap"
    elif args.phase == "combo_sweep":
        rows, extra_payload = run_combo_sweep(tensor_dir, data, args)
        analysis = "prefeval_stage1_combo_sweep"
    elif args.phase == "logits_k3":
        rows, extra_payload = run_logits_k3_experiments(tensor_dir, data, args)
        analysis = "prefeval_stage1_logits_k3"
    else:
        raise ValueError(f"Unsupported phase: {args.phase}")

    payload = {
        "created_utc": base.now_utc(),
        "analysis": analysis,
        "inputs": {
            "prepared_jsonl": str(prepared_jsonl),
            "tensor_dir": str(tensor_dir),
            "extra_tensor_dirs": [str(path) for path in tensor_dirs[1:]],
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "phase": args.phase,
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
            "Stored hidden vectors are raw extractor outputs; this offline pass applies retrieval transforms after loading.",
            "The n=1000 prompt-sweep table previously reported anti_pca_both_k15 plus L2-normalized cosine, not untreated raw cosine.",
            "candidate_only k=10 is a sanity check because earlier LongMemEval stages found candidate-only transforms harmful.",
        ],
        "rows": sorted(rows, key=lambda row: (row["summary"]["recall_all@5"], row["summary"]["ndcg_any@5"]), reverse=True),
        "elapsed_seconds": time.monotonic() - started,
        **extra_payload,
    }
    json_path.write_text(json.dumps(base.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    ensure_findings_skeleton(DEFAULT_FINDINGS)
    base.log(f"wrote {json_path}")
    base.log(f"wrote {md_path}")
    return 0


def latest_hidden_tensor_dir() -> Path:
    candidates = sorted(
        (BENCH_DIR / "tensors").glob("hidden_implicit_persona_n1000_*promptreps1x128"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError("No n=1000 PromptReps hidden tensor dir found under benchmarks/PrefEval/tensors.")
    return candidates[0]


def load_prepared_jsonl(path: Path) -> base.BenchmarkData:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    items: list[base.PrefEvalItem] = []
    gold_ids_by_query: list[list[str]] = []
    for row in rows:
        items.append(
            base.PrefEvalItem(
                item_id=row["item_id"],
                preference=base.clean_text(row["preference"]),
                question=base.clean_text(row["question"]),
                topic=base.clean_text(row.get("topic", "")),
                preference_type=base.clean_text(row.get("preference_type", "")),
                metadata=dict(row.get("metadata", {})),
            )
        )
        gold_ids_by_query.append(list(row["gold_ids"]))
    return base.BenchmarkData(
        task="implicit_persona",
        dataset_id="siyanzhao/prefeval_implicit_persona",
        items=items,
        candidate_ids=[item.item_id for item in items],
        candidate_texts=[item.preference for item in items],
        query_ids=[f"{item.item_id}:query" for item in items],
        query_texts=[item.question for item in items],
        gold_ids_by_query=gold_ids_by_query,
    )


def load_manifest(tensor_dir: Path) -> dict[str, Any]:
    manifest_path = tensor_dir / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing manifest: {manifest_path}")
    return json.loads(manifest_path.read_text(encoding="utf-8"))["expected"]


def validate_inputs(data: base.BenchmarkData, manifest: dict[str, Any]) -> None:
    item_ids = [item.item_id for item in data.items]
    if manifest.get("item_ids") != item_ids:
        raise ValueError("Prepared JSONL item ids do not match tensor manifest item ids.")
    expected_fingerprint = base.benchmark_data_fingerprint(data)
    manifest_fingerprint = manifest.get("data_fingerprint")
    if manifest_fingerprint is None:
        base.log(
            "warning: tensor manifest has no data_fingerprint; "
            "using legacy item-id-only validation for this existing cache"
        )
    elif manifest_fingerprint != expected_fingerprint:
        raise ValueError(
            "Prepared JSONL content does not match tensor manifest data_fingerprint "
            f"(prepared={expected_fingerprint}, manifest={manifest_fingerprint})."
        )


def run_anti_pca_calibration(tensor_dir: Path, data: base.BenchmarkData, args: argparse.Namespace) -> list[dict[str, Any]]:
    vectors_path = tensor_dir / "raw_hidden_vectors.npz"
    if not vectors_path.exists():
        raise FileNotFoundError(f"Missing raw hidden vectors: {vectors_path}")
    eval_args = SimpleNamespace(top_k=args.top_k, bootstrap_samples=args.bootstrap_samples)
    rows: list[dict[str, Any]] = []
    with np.load(vectors_path) as arrays:
        for variant, layer, family in CALIBRATION_CELLS:
            label = f"{variant}|L{layer}|anti_pca_both_k15"
            candidates = np.asarray(arrays[f"{label}::candidates"], dtype=np.float32)
            queries = np.asarray(arrays[f"{label}::queries"], dtype=np.float32)
            base.log(f"loaded {label}: candidates={candidates.shape} queries={queries.shape}")
            rows.extend(evaluate_transform_grid(variant, layer, family, candidates, queries, data, eval_args))
    return rows


def run_dense_k3(
    tensor_dirs: list[Path],
    data: base.BenchmarkData,
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    needed_names = sorted({name for combo in DENSE_K3_COMBOS.values() for name in combo})
    specs = {name: DENSE_CELL_LIBRARY[name] for name in needed_names}
    eval_args = SimpleNamespace(top_k=args.top_k, bootstrap_samples=args.bootstrap_samples)
    first500 = list(range(0, min(500, len(data.query_ids))))
    second500 = list(range(min(500, len(data.query_ids)), len(data.query_ids)))

    loaded = load_dense_specs_from_tensor_dirs(tensor_dirs, specs)

    oracle_rows = []
    for combo_name, spec_names in DENSE_K3_COMBOS.items():
        oracle_rows.append(oracle_union_row(combo_name, spec_names, loaded, data, first500, "first500"))
        oracle_rows.append(oracle_union_row(combo_name, spec_names, loaded, data, second500, "second500"))
        oracle_rows.append(oracle_union_row(combo_name, spec_names, loaded, data, list(range(len(data.query_ids))), "all"))

    rows: list[dict[str, Any]] = []
    for combo_name, spec_names in DENSE_K3_COMBOS.items():
        combo_specs = [loaded[name] for name in spec_names]
        score_matrices = {
            "zsum": score_zsum(combo_specs),
            "vertical_concat_norm_weighted": score_vertical_concat(combo_specs, component_normalize=False),
            "vector_average_component_norm": score_vector_average(combo_specs, component_normalize=True),
        }
        for scorer, scores in score_matrices.items():
            rows.append(
                evaluate_matrix_with_split(
                    f"{combo_name}_{scorer}",
                    f"PrefEval Stage 1 K3 dense fusion: {combo_name}, scorer={scorer}",
                    scores,
                    data,
                    eval_args,
                    split_name="all",
                    indices=None,
                    extra={
                        "phase": "dense_k3",
                        "combo": combo_name,
                        "scorer": scorer,
                        "cells": [spec_to_json(loaded[name]["spec"]) for name in spec_names],
                    },
                )
            )
            rows.append(
                evaluate_matrix_with_split(
                    f"{combo_name}_{scorer}_first500",
                    f"First-half validation for {combo_name}, scorer={scorer}",
                    scores,
                    data,
                    eval_args,
                    split_name="first500",
                    indices=first500,
                    extra={"phase": "dense_k3_split", "combo": combo_name, "scorer": scorer},
                )
            )
            rows.append(
                evaluate_matrix_with_split(
                    f"{combo_name}_{scorer}_second500",
                    f"Second-half validation for {combo_name}, scorer={scorer}",
                    scores,
                    data,
                    eval_args,
                    split_name="second500",
                    indices=second500,
                    extra={"phase": "dense_k3_split", "combo": combo_name, "scorer": scorer},
                )
            )
    return rows, {
        "oracle_union_rows": sorted(
            oracle_rows,
            key=lambda row: (row["split"] != "first500", -row["oracle_any_hit_at5"], -row["oracle_recall_all_at5"]),
        ),
        "dense_k3_combos": {
            name: [spec_to_json(DENSE_CELL_LIBRARY[cell_name]) for cell_name in cell_names]
            for name, cell_names in DENSE_K3_COMBOS.items()
        },
    }


def run_promptreps(
    tensor_dir: Path,
    data: base.BenchmarkData,
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    vectors_path = tensor_dir / "raw_hidden_vectors.npz"
    if not vectors_path.exists():
        raise FileNotFoundError(f"Missing raw hidden vectors: {vectors_path}")
    eval_args = SimpleNamespace(top_k=args.top_k, bootstrap_samples=args.bootstrap_samples)
    dense_spec_names = {
        "2-3-1": "2-3-1_L30_both_k15",
        "2-3-2_query": "2-3-2_query_L30_both_k15",
        "2-5": "2-5_L29_both_k15",
        "2-1": "2-1_L30_both_k5",
    }
    sparse_variants = ("2-3-1", "2-3-2_query", "2-5", "2-1")
    alphas = (0.25, 0.5, 0.7, 0.8, 0.9)

    with np.load(vectors_path) as arrays:
        dense_loaded = load_dense_specs(
            arrays,
            {name: DENSE_CELL_LIBRARY[name] for name in sorted(set(dense_spec_names.values()))},
        )
        sparse_scores = {
            variant: score_promptreps_sparse(arrays, variant, candidate_count=len(data.candidate_ids), query_count=len(data.query_ids))
            for variant in sparse_variants
        }

    rows: list[dict[str, Any]] = []
    for variant, sparse in sparse_scores.items():
        rows.append(
            base.evaluate_score_matrix(
                f"promptreps_{variant}_sparse_only",
                f"PromptReps sparse-only score for {variant}",
                sparse,
                data,
                eval_args,
                extra={"phase": "promptreps_sparse_only", "variant": variant, "scorer": "sparse_dot"},
            )
        )
    for variant, spec_name in dense_spec_names.items():
        dense = dense_loaded[spec_name]["scores"]
        sparse = sparse_scores[variant]
        for alpha in alphas:
            scores = alpha * base.row_zscore(dense) + (1.0 - alpha) * base.row_zscore(sparse)
            rows.append(
                base.evaluate_score_matrix(
                    f"promptreps_{variant}_dense_sparse_alpha{alpha:.2f}",
                    f"Same-prompt dense/sparse PromptReps fusion for {variant}; alpha weights dense",
                    scores,
                    data,
                    eval_args,
                    extra={"phase": "promptreps_same_prompt_fusion", "variant": variant, "alpha": alpha, "scorer": "dense_sparse_zfusion"},
                )
            )

    k3_names = DENSE_K3_COMBOS["k3_key_assoc_topic"]
    k3_dense = score_vector_average([dense_loaded[name] for name in k3_names], component_normalize=True)
    k3_sparse = sparse_zsum([sparse_scores["2-3-1"], sparse_scores["2-5"], sparse_scores["2-1"]])
    rows.append(
        base.evaluate_score_matrix(
            "promptreps_k3_key_assoc_topic_sparse_zsum",
            "PromptReps sparse z-sum for the winning K3 key+association+topic variants",
            k3_sparse,
            data,
            eval_args,
            extra={"phase": "promptreps_k3_sparse", "combo": "k3_key_assoc_topic", "scorer": "sparse_zsum"},
        )
    )
    for alpha in alphas:
        scores = alpha * base.row_zscore(k3_dense) + (1.0 - alpha) * base.row_zscore(k3_sparse)
        rows.append(
            base.evaluate_score_matrix(
                f"promptreps_k3_key_assoc_topic_dense_sparse_alpha{alpha:.2f}",
                "Winning dense K3 vector-average fused with K3 PromptReps sparse z-sum; alpha weights dense",
                scores,
                data,
                eval_args,
                extra={"phase": "promptreps_k3_dense_sparse_fusion", "combo": "k3_key_assoc_topic", "alpha": alpha, "scorer": "dense_sparse_zfusion"},
            )
        )
    return rows, {
        "promptreps": {
            "sparse_variants": list(sparse_variants),
            "alphas": list(alphas),
            "sparse_schema": "text-token-filtered ReLU+log1p top128 quantized values from the n=1000 tensor store",
            "note": "Current tensor store used floor(value*100) quantization; PromptReps reference code uses rounding, so this is a close but not byte-identical recipe.",
        }
    }


def score_promptreps_sparse(arrays: Any, variant: str, *, candidate_count: int, query_count: int) -> np.ndarray:
    candidate_ids = np.asarray(arrays[f"{variant}::candidates::promptreps_token_ids"], dtype=np.int32)
    candidate_values = np.asarray(arrays[f"{variant}::candidates::promptreps_values"], dtype=np.float32)
    query_ids = np.asarray(arrays[f"{variant}::queries::promptreps_token_ids"], dtype=np.int32)
    query_values = np.asarray(arrays[f"{variant}::queries::promptreps_values"], dtype=np.float32)
    return score_sparse_arrays(
        candidate_ids,
        candidate_values,
        query_ids,
        query_values,
        candidate_count=candidate_count,
        query_count=query_count,
    )


def score_toplogits_sparse(arrays: Any, variant: str, *, candidate_count: int, query_count: int) -> np.ndarray:
    candidate_ids = np.asarray(arrays[f"{variant}::candidates::top_logit_token_ids"], dtype=np.int32)
    candidate_values = np.log1p(
        np.maximum(np.asarray(arrays[f"{variant}::candidates::top_logit_values"], dtype=np.float32), 0.0)
    )
    query_ids = np.asarray(arrays[f"{variant}::queries::top_logit_token_ids"], dtype=np.int32)
    query_values = np.log1p(
        np.maximum(np.asarray(arrays[f"{variant}::queries::top_logit_values"], dtype=np.float32), 0.0)
    )
    return score_sparse_arrays(
        candidate_ids,
        candidate_values,
        query_ids,
        query_values,
        candidate_count=candidate_count,
        query_count=query_count,
    )


def score_sparse_arrays(
    candidate_ids: np.ndarray,
    candidate_values: np.ndarray,
    query_ids: np.ndarray,
    query_values: np.ndarray,
    *,
    candidate_count: int,
    query_count: int,
) -> np.ndarray:
    postings: dict[int, list[tuple[int, float]]] = {}
    for candidate_index in range(candidate_count):
        for token_id, value in zip(candidate_ids[candidate_index], candidate_values[candidate_index], strict=True):
            if token_id < 0 or value <= 0:
                continue
            postings.setdefault(int(token_id), []).append((candidate_index, float(value)))
    posting_arrays = {
        token_id: (
            np.asarray([item[0] for item in items], dtype=np.int32),
            np.asarray([item[1] for item in items], dtype=np.float32),
        )
        for token_id, items in postings.items()
    }
    scores = np.zeros((query_count, candidate_count), dtype=np.float32)
    for query_index in range(query_count):
        for token_id, query_value in zip(query_ids[query_index], query_values[query_index], strict=True):
            if token_id < 0 or query_value <= 0:
                continue
            posting = posting_arrays.get(int(token_id))
            if posting is None:
                continue
            candidate_indices, candidate_posting_values = posting
            scores[query_index, candidate_indices] += float(query_value) * candidate_posting_values
    return scores


def sparse_zsum(matrices: list[np.ndarray]) -> np.ndarray:
    output = np.zeros_like(matrices[0], dtype=np.float32)
    for matrix in matrices:
        output += base.row_zscore(matrix)
    return output


def run_bm25_fusion(
    tensor_dir: Path,
    data: base.BenchmarkData,
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    vectors_path = tensor_dir / "raw_hidden_vectors.npz"
    if not vectors_path.exists():
        raise FileNotFoundError(f"Missing raw hidden vectors: {vectors_path}")
    eval_args = SimpleNamespace(top_k=args.top_k, bootstrap_samples=args.bootstrap_samples)
    alphas = (0.70, 0.75, 0.80, 0.85, 0.90)
    with np.load(vectors_path) as arrays:
        loaded = load_dense_specs(
            arrays,
            {
                "2-3-1_L30_both_k15": DENSE_CELL_LIBRARY["2-3-1_L30_both_k15"],
                "2-5_L29_both_k15": DENSE_CELL_LIBRARY["2-5_L29_both_k15"],
                "2-1_L30_both_k5": DENSE_CELL_LIBRARY["2-1_L30_both_k5"],
            },
        )
    dense_scores = {
        "single_2-3-1": loaded["2-3-1_L30_both_k15"]["scores"],
        "k3_key_assoc_topic_vector_average": score_vector_average(
            [
                loaded["2-3-1_L30_both_k15"],
                loaded["2-5_L29_both_k15"],
                loaded["2-1_L30_both_k5"],
            ],
            component_normalize=True,
        ),
    }
    bm25 = base.score_bm25(data)
    rows: list[dict[str, Any]] = []
    for base_name, dense in dense_scores.items():
        for alpha in alphas:
            full_scores = alpha * base.row_zscore(dense) + (1.0 - alpha) * base.row_zscore(bm25)
            rows.append(
                base.evaluate_score_matrix(
                    f"bm25_{base_name}_full_alpha{alpha:.2f}",
                    f"Full-candidate BM25 fusion for {base_name}; alpha weights dense",
                    full_scores,
                    data,
                    eval_args,
                    extra={"phase": "bm25_fusion", "base": base_name, "scope": "full", "alpha": alpha, "scorer": "dense_bm25_zfusion"},
                )
            )
            top20_scores = shortlist_fusion_scores(dense, bm25, alpha=alpha, shortlist_size=20)
            rows.append(
                base.evaluate_score_matrix(
                    f"bm25_{base_name}_top20_alpha{alpha:.2f}",
                    f"BM25 fusion inside dense top20 shortlist for {base_name}; alpha weights dense",
                    top20_scores,
                    data,
                    eval_args,
                    extra={"phase": "bm25_fusion", "base": base_name, "scope": "vector_top20", "alpha": alpha, "scorer": "dense_top20_bm25_zfusion"},
                )
            )
    return rows, {"bm25_fusion": {"alphas": list(alphas), "bases": list(dense_scores), "scopes": ["full", "vector_top20"]}}


def shortlist_fusion_scores(
    dense_scores: np.ndarray,
    bm25_scores: np.ndarray,
    *,
    alpha: float,
    shortlist_size: int,
) -> np.ndarray:
    if dense_scores.shape != bm25_scores.shape:
        raise ValueError(f"Score matrices differ: {dense_scores.shape} vs {bm25_scores.shape}")
    query_count, candidate_count = dense_scores.shape
    output = np.empty_like(dense_scores, dtype=np.float32)
    for query_index in range(query_count):
        dense_order = np.argsort(dense_scores[query_index])[::-1]
        # Keep shortlist candidates above non-shortlist candidates, then append
        # the rest by original dense rank. This matches the Stage 3 top-N fusion
        # semantics and prevents BM25 from pulling arbitrary full-corpus lexical
        # false positives into the top results.
        output[query_index, dense_order] = -1_000_000.0 - np.arange(candidate_count, dtype=np.float32)
        shortlist = dense_order[:shortlist_size]
        dense_local = dense_scores[query_index, shortlist]
        bm25_local = bm25_scores[query_index, shortlist]
        dense_local = zscore_1d(dense_local)
        bm25_local = zscore_1d(bm25_local)
        output[query_index, shortlist] = 1_000_000.0 + alpha * dense_local + (1.0 - alpha) * bm25_local
    return output


def zscore_1d(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float32)
    std = float(np.std(values))
    if std <= 1e-12:
        return np.zeros_like(values, dtype=np.float32)
    return ((values - float(np.mean(values))) / std).astype(np.float32, copy=False)


def run_layer_overlap(
    tensor_dir: Path,
    data: base.BenchmarkData,
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    vectors_path = tensor_dir / "raw_hidden_vectors.npz"
    if not vectors_path.exists():
        raise FileNotFoundError(f"Missing raw hidden vectors: {vectors_path}")
    layer_specs = {
        f"2-3-1_L{layer}_both_k15": DenseCellSpec(
            f"2-3-1_L{layer}_both_k15",
            "2-3-1",
            layer,
            "anti_pca_both",
            15,
            "layer-diagnostic",
        )
        for layer in (28, 29, 30, 31)
    }
    layer_sets = {
        "2-3-1_L29_L30": ("2-3-1_L29_both_k15", "2-3-1_L30_both_k15"),
        "2-3-1_L28_L29_L30": ("2-3-1_L28_both_k15", "2-3-1_L29_both_k15", "2-3-1_L30_both_k15"),
        "2-3-1_L28_L29_L30_L31": (
            "2-3-1_L28_both_k15",
            "2-3-1_L29_both_k15",
            "2-3-1_L30_both_k15",
            "2-3-1_L31_both_k15",
        ),
    }
    eval_args = SimpleNamespace(top_k=args.top_k, bootstrap_samples=args.bootstrap_samples)
    with np.load(vectors_path) as arrays:
        loaded = load_dense_specs(arrays, layer_specs)
    rows = []
    for set_name, spec_names in layer_sets.items():
        scores = sparse_zsum([loaded[name]["scores"] for name in spec_names])
        rows.append(
            base.evaluate_score_matrix(
                f"layer_overlap_{set_name}_zsum",
                f"Layer z-sum diagnostic for {set_name}",
                scores,
                data,
                eval_args,
                extra={"phase": "layer_overlap", "layer_set": set_name, "scorer": "zsum", "cells": list(spec_names)},
            )
        )
    indices = list(range(len(data.query_ids)))
    diagnostics = [
        oracle_union_row(set_name, spec_names, loaded, data, indices, "all")
        for set_name, spec_names in layer_sets.items()
    ]
    return rows, {"layer_overlap_rows": diagnostics}


def run_combo_sweep(
    tensor_dir: Path,
    data: base.BenchmarkData,
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Sweep K3 dense combos, then tune BM25/PromptReps weights on top rows."""

    vectors_path = tensor_dir / "raw_hidden_vectors.npz"
    if not vectors_path.exists():
        raise FileNotFoundError(f"Missing raw hidden vectors: {vectors_path}")

    eval_args = SimpleNamespace(top_k=args.top_k, bootstrap_samples=args.bootstrap_samples)
    first500 = list(range(0, min(500, len(data.query_ids))))
    second500 = list(range(min(500, len(data.query_ids)), len(data.query_ids)))
    selection_indices = None if args.combo_selection_split == "all" else first500
    # `2-7` lives in a supplement tensor without logits in the current Stage 1
    # runs. Keep combo_sweep on the fully shared main tensor; 2-7 is evaluated
    # explicitly by the dense_k3 phase with --extra-tensor-dir.
    sweep_library = {name: DENSE_CELL_LIBRARY[name] for name in COMBO_SWEEP_CELL_NAMES}
    spec_names = list(sweep_library)
    combo_specs = [
        tuple(items)
        for items in combinations(spec_names, 3)
        if combo_has_unique_variants(items)
    ]
    base.log(
        f"combo sweep: {len(combo_specs)} K3 combos x {len(COMBO_SWEEP_SCORERS)} dense scorers; "
        f"top_n={args.combo_top_n} selection_split={args.combo_selection_split}"
    )

    with np.load(vectors_path) as arrays:
        loaded = load_dense_specs(arrays, sweep_library)
        sparse_scores = {
            variant: score_promptreps_sparse(
                arrays,
                variant,
                candidate_count=len(data.candidate_ids),
                query_count=len(data.query_ids),
            )
            for variant in sorted({spec.variant for spec in sweep_library.values()})
        }

    rows: list[dict[str, Any]] = []
    selected: list[dict[str, Any]] = []
    oracle_rows: list[dict[str, Any]] = []
    for spec_tuple in combo_specs:
        combo_name = combo_label(spec_tuple)
        combo_loaded = [loaded[name] for name in spec_tuple]
        score_matrices = {
            "zsum": score_zsum(combo_loaded),
            "vertical_concat_norm_weighted": score_vertical_concat(combo_loaded, component_normalize=False),
            "vector_average_component_norm": score_vector_average(combo_loaded, component_normalize=True),
        }
        oracle_rows.append(
            oracle_union_row(combo_name, spec_tuple, loaded, data, list(range(len(data.query_ids))), "all")
        )
        for scorer, scores in score_matrices.items():
            row = base.evaluate_score_matrix(
                f"combo_{combo_name}_{scorer}",
                f"Systematic PrefEval K3 dense combo sweep: {combo_name}, scorer={scorer}",
                scores,
                data,
                eval_args,
                extra={
                    "phase": "combo_sweep_dense",
                    "combo": combo_name,
                    "cells": list(spec_tuple),
                    "scorer": scorer,
                },
            )
            rows.append(row)
            selected.append(
                {
                    "selection_score": recall_all_at_k(scores, data, selection_indices, k=5),
                    "combo": combo_name,
                    "cells": spec_tuple,
                    "scorer": scorer,
                    "scores": scores,
                    "row": row,
                }
            )
            selected.sort(key=lambda item: item["selection_score"], reverse=True)
            del selected[max(args.combo_top_n, 0) :]

    bm25_scores = base.score_bm25(data)
    for item in selected:
        combo_name = item["combo"]
        spec_tuple = item["cells"]
        scorer = item["scorer"]
        dense_scores = item["scores"]
        combo_sparse = sparse_zsum([sparse_scores[DENSE_CELL_LIBRARY[name].variant] for name in spec_tuple])
        rows.extend(
            evaluate_selected_splits(
                f"combo_{combo_name}_{scorer}_dense",
                f"Selected dense K3 combo split validation: {combo_name}, scorer={scorer}",
                dense_scores,
                data,
                eval_args,
                first500,
                second500,
                extra={
                    "phase": "combo_sweep_selected_dense_split",
                    "combo": combo_name,
                    "cells": list(spec_tuple),
                    "scorer": scorer,
                    "selection_score": item["selection_score"],
                    "selection_split": args.combo_selection_split,
                },
            )
        )
        rows.extend(
            run_weight_grid_for_combo(
                combo_name,
                spec_tuple,
                scorer,
                dense_scores,
                bm25_scores,
                combo_sparse,
                data,
                eval_args,
                first500,
                second500,
                selection_score=item["selection_score"],
                selection_split=args.combo_selection_split,
            )
        )
        rows.extend(
            run_logits_screening_for_combo(
                combo_name,
                spec_tuple,
                scorer,
                dense_scores,
                bm25_scores,
                combo_sparse,
                data,
                eval_args,
                first500,
                second500,
                shortlist_size=args.shortlist_size,
                screen_alpha=args.screen_alpha,
            )
        )

    return rows, {
        "oracle_union_rows": sorted(
            oracle_rows,
            key=lambda row: (row["oracle_any_hit_at5"], row["oracle_any_gain_vs_best_component"]),
            reverse=True,
        ),
        "combo_sweep": {
            "combo_count": len(combo_specs),
            "scorers": list(COMBO_SWEEP_SCORERS),
            "selection_split": args.combo_selection_split,
            "top_n": args.combo_top_n,
            "selected": [
                {
                    "combo": item["combo"],
                    "cells": list(item["cells"]),
                    "scorer": item["scorer"],
                    "selection_score": item["selection_score"],
                }
                for item in selected
            ],
            "weight_grid": [
                {"dense": 1.0 - bm25 - logits, "bm25": bm25, "logits": logits}
                for logits in WEIGHT_SWEEP_LOGITS_WEIGHTS
                for bm25 in WEIGHT_SWEEP_BM25_WEIGHTS
                if 0.60 <= 1.0 - bm25 - logits <= 0.90
            ],
            "shortlist_size": args.shortlist_size,
            "screen_alpha": args.screen_alpha,
        },
    }


def run_logits_k3_experiments(
    tensor_dir: Path,
    data: base.BenchmarkData,
    args: argparse.Namespace,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Focused K3 logits/BM25 experiments over the existing n=1000 tensor cache."""

    vectors_path = tensor_dir / "raw_hidden_vectors.npz"
    if not vectors_path.exists():
        raise FileNotFoundError(f"Missing raw hidden vectors: {vectors_path}")

    eval_args = SimpleNamespace(top_k=args.top_k, bootstrap_samples=args.bootstrap_samples)
    spec_names = sorted({name for combo in LOGITS_K3_COMBOS.values() for name in combo})
    sparse_variants = sorted({DENSE_CELL_LIBRARY[name].variant for name in spec_names})
    base.log(
        f"logits K3 experiments: combos={list(LOGITS_K3_COMBOS)} sparse_variants={sparse_variants}"
    )

    with np.load(vectors_path) as arrays:
        loaded = load_dense_specs(arrays, {name: DENSE_CELL_LIBRARY[name] for name in spec_names})
        promptreps_scores = {
            variant: score_promptreps_sparse(
                arrays,
                variant,
                candidate_count=len(data.candidate_ids),
                query_count=len(data.query_ids),
            )
            for variant in sparse_variants
        }
        top_logits_scores = {
            variant: score_toplogits_sparse(
                arrays,
                variant,
                candidate_count=len(data.candidate_ids),
                query_count=len(data.query_ids),
            )
            for variant in sparse_variants
        }

    bm25_scores = base.score_bm25(data)
    bm25_z = base.row_zscore(bm25_scores)
    first500 = list(range(0, min(500, len(data.query_ids))))
    second500 = list(range(min(500, len(data.query_ids)), len(data.query_ids)))

    rows: list[dict[str, Any]] = [
        base.evaluate_score_matrix(
            "bm25",
            "BM25 over preference memory strings",
            bm25_scores,
            data,
            eval_args,
            extra={"phase": "logits_k3_reference", "scorer": "bm25"},
        )
    ]

    for combo_name, spec_tuple in LOGITS_K3_COMBOS.items():
        combo_loaded = [loaded[name] for name in spec_tuple]
        combo_variants = [DENSE_CELL_LIBRARY[name].variant for name in spec_tuple]
        dense_by_scorer = {
            "zsum": score_zsum(combo_loaded),
            "vertical_concat_norm_weighted": score_vertical_concat(combo_loaded, component_normalize=False),
            "vector_average_component_norm": score_vector_average(combo_loaded, component_normalize=True),
        }
        promptreps_sparse = sparse_zsum([promptreps_scores[variant] for variant in combo_variants])
        top_logits_sparse = sparse_zsum([top_logits_scores[variant] for variant in combo_variants])

        rows.append(
            base.evaluate_score_matrix(
                f"logits_k3_{combo_name}_promptreps_sparse_only",
                f"PromptReps paper-style filtered sparse logits only for {combo_name}",
                promptreps_sparse,
                data,
                eval_args,
                extra={
                    "phase": "logits_k3_sparse_only",
                    "combo": combo_name,
                    "cells": list(spec_tuple),
                    "logits_method": "promptreps_text_token_filtered",
                    "scorer": "sparse_zsum",
                },
            )
        )
        rows.append(
            base.evaluate_score_matrix(
                f"logits_k3_{combo_name}_toplogits_sparse_only",
                f"Unfiltered top-256 sparse logits only for {combo_name}",
                top_logits_sparse,
                data,
                eval_args,
                extra={
                    "phase": "logits_k3_sparse_only",
                    "combo": combo_name,
                    "cells": list(spec_tuple),
                    "logits_method": "unfiltered_top256_log1p_relu",
                    "scorer": "sparse_zsum",
                },
            )
        )

        component_dense_sources = [loaded[name]["scores"] for name in spec_tuple]
        five_sources = [*component_dense_sources, bm25_scores, top_logits_sparse]
        for weight_name, weights, dense_total, bm25_weight, logits_weight in FIVE_SOURCE_WEIGHT_GRID:
            five_source_scores = weighted_row_zscore_sum(five_sources, weights)
            rows.extend(
                evaluate_selected_splits(
                    f"logits_k3_{combo_name}_five_source_full_{weight_name}",
                    (
                        f"Five-source full-corpus z-fusion for {combo_name}: "
                        f"3 prompt sources + BM25 + unfiltered logits"
                    ),
                    five_source_scores,
                    data,
                    eval_args,
                    first500,
                    second500,
                    extra={
                        "phase": "logits_k3_five_source_full",
                        "combo": combo_name,
                        "cells": list(spec_tuple),
                        "logits_method": "unfiltered_top256_log1p_relu",
                        "source_count": 5,
                        "source_weights": list(weights),
                        "dense_total_weight": dense_total,
                        "bm25_weight": bm25_weight,
                        "logits_weight": logits_weight,
                    },
                )
            )
            union_scores = shortlist_union_rerank_scores(
                five_source_scores,
                five_sources,
                shortlist_size=args.shortlist_size,
            )
            rows.extend(
                evaluate_selected_splits(
                    f"logits_k3_{combo_name}_five_source_union_top{args.shortlist_size}_{weight_name}",
                    (
                        f"Five-source top-{args.shortlist_size} union for {combo_name}: "
                        f"3 prompt sources + BM25 + unfiltered logits, rerank=same five-source score"
                    ),
                    union_scores,
                    data,
                    eval_args,
                    first500,
                    second500,
                    extra={
                        "phase": "logits_k3_five_source_topk_union",
                        "combo": combo_name,
                        "cells": list(spec_tuple),
                        "logits_method": "unfiltered_top256_log1p_relu",
                        "source_rule": "union_ge1",
                        "source_count": 5,
                        "shortlist_size": args.shortlist_size,
                        "source_weights": list(weights),
                        "dense_total_weight": dense_total,
                        "bm25_weight": bm25_weight,
                        "logits_weight": logits_weight,
                    },
                )
            )
            agreement_scores, agreement_stats = source_agreement_rerank_scores(
                five_source_scores,
                five_sources,
                data,
                shortlist_size=args.shortlist_size,
                min_sources=2,
            )
            rows.extend(
                evaluate_selected_splits(
                    f"logits_k3_{combo_name}_five_source_source_ge2_top{args.shortlist_size}_{weight_name}",
                    (
                        f"Five-source top-{args.shortlist_size} agreement for {combo_name}: "
                        f"3 prompt sources + BM25 + unfiltered logits, source_count>=2, "
                        f"rerank=same five-source score"
                    ),
                    agreement_scores,
                    data,
                    eval_args,
                    first500,
                    second500,
                    extra={
                        "phase": "logits_k3_five_source_topk_agreement",
                        "combo": combo_name,
                        "cells": list(spec_tuple),
                        "logits_method": "unfiltered_top256_log1p_relu",
                        "source_rule": "source_ge2",
                        "source_count": 5,
                        "shortlist_size": args.shortlist_size,
                        "source_weights": list(weights),
                        "dense_total_weight": dense_total,
                        "bm25_weight": bm25_weight,
                        "logits_weight": logits_weight,
                        "shortlist_stats": agreement_stats,
                    },
                )
            )

        for scorer, dense_scores in dense_by_scorer.items():
            rows.append(
                base.evaluate_score_matrix(
                    f"logits_k3_{combo_name}_{scorer}_dense_only",
                    f"K3 dense baseline for {combo_name}, scorer={scorer}",
                    dense_scores,
                    data,
                    eval_args,
                    extra={
                        "phase": "logits_k3_dense_baseline",
                        "combo": combo_name,
                        "cells": list(spec_tuple),
                        "scorer": scorer,
                    },
                )
            )

            dense_z = base.row_zscore(dense_scores)
            rerank_dense_bm25 = 0.75 * dense_z + 0.25 * bm25_z
            rows.append(
                base.evaluate_score_matrix(
                    f"logits_k3_{combo_name}_{scorer}_dense_bm25_d0.75_b0.25",
                    f"K3 dense + BM25 z-fusion for {combo_name}, scorer={scorer}",
                    rerank_dense_bm25,
                    data,
                    eval_args,
                    extra={
                        "phase": "logits_k3_dense_bm25",
                        "combo": combo_name,
                        "cells": list(spec_tuple),
                        "scorer": scorer,
                        "dense_weight": 0.75,
                        "bm25_weight": 0.25,
                    },
                )
            )

            for logits_method, sparse_scores in (
                ("promptreps_text_token_filtered", promptreps_sparse),
                ("unfiltered_top256_log1p_relu", top_logits_sparse),
            ):
                sparse_z = base.row_zscore(sparse_scores)
                rows.append(
                    base.evaluate_score_matrix(
                        f"logits_k3_{combo_name}_{scorer}_{logits_method}_paper_alpha0.50",
                        (
                            f"PromptReps-style dense+sparse hybrid for {combo_name}, "
                            f"scorer={scorer}, alpha=0.50"
                        ),
                        0.50 * dense_z + 0.50 * sparse_z,
                        data,
                        eval_args,
                        extra={
                            "phase": "logits_k3_paper_hybrid",
                            "combo": combo_name,
                            "cells": list(spec_tuple),
                            "scorer": scorer,
                            "logits_method": logits_method,
                            "dense_weight": 0.50,
                            "logits_weight": 0.50,
                        },
                    )
                )
                for dense_weight, bm25_weight, logits_weight in LOGITS_K3_WEIGHT_GRID:
                    scores = dense_weight * dense_z + bm25_weight * bm25_z + logits_weight * sparse_z
                    rows.append(
                        base.evaluate_score_matrix(
                            (
                                f"logits_k3_{combo_name}_{scorer}_{logits_method}_"
                                f"d{dense_weight:.2f}_b{bm25_weight:.2f}_l{logits_weight:.2f}"
                            ),
                            (
                                f"K3 dense + BM25 + logits z-fusion for {combo_name}, "
                                f"scorer={scorer}, logits={logits_method}"
                            ),
                            scores,
                            data,
                            eval_args,
                            extra={
                                "phase": "logits_k3_three_way_fusion",
                                "combo": combo_name,
                                "cells": list(spec_tuple),
                                "scorer": scorer,
                                "logits_method": logits_method,
                                "dense_weight": dense_weight,
                                "bm25_weight": bm25_weight,
                                "logits_weight": logits_weight,
                            },
                        )
                    )

                component_dense_sources = [loaded[name]["scores"] for name in spec_tuple]
                for source_rule in ("source_ge1", "source_ge2"):
                    screen_scores, screen_stats = source_agreement_rerank_scores(
                        rerank_dense_bm25,
                        [*component_dense_sources, bm25_scores, sparse_scores],
                        data,
                        shortlist_size=args.shortlist_size,
                        min_sources=1 if source_rule == "source_ge1" else 2,
                    )
                    rows.extend(
                        evaluate_selected_splits(
                            (
                                f"logits_k3_{combo_name}_{scorer}_{logits_method}_"
                                f"{source_rule}_top{args.shortlist_size}_rerank_d0.75_b0.25"
                            ),
                            (
                                f"Top-{args.shortlist_size} source screening for {combo_name}: "
                                f"3 dense prompt sources + BM25 + logits, {source_rule}, rerank=dense/BM25"
                            ),
                            screen_scores,
                            data,
                            eval_args,
                            first500,
                            second500,
                            extra={
                                "phase": "logits_k3_source_screening",
                                "combo": combo_name,
                                "cells": list(spec_tuple),
                                "scorer": scorer,
                                "logits_method": logits_method,
                                "source_rule": source_rule,
                                "source_count": 5,
                                "shortlist_size": args.shortlist_size,
                                "rerank_dense_weight": 0.75,
                                "rerank_bm25_weight": 0.25,
                                "shortlist_stats": screen_stats,
                            },
                        )
                    )

            for dense_weight, bm25_weight, logits_weight in ((0.75, 0.20, 0.05), (0.70, 0.20, 0.10)):
                rerank_threeway = dense_weight * dense_z + bm25_weight * bm25_z + logits_weight * base.row_zscore(top_logits_sparse)
                for min_sources in (2, 3):
                    screen_scores, screen_stats = source_agreement_rerank_scores(
                        rerank_threeway,
                        [*component_dense_sources, bm25_scores],
                        data,
                        shortlist_size=args.shortlist_size,
                        min_sources=min_sources,
                    )
                    rows.extend(
                        evaluate_selected_splits(
                            (
                                f"logits_k3_{combo_name}_{scorer}_four_source_"
                                f"source_ge{min_sources}_top{args.shortlist_size}_"
                                f"rerank_unfiltered_d{dense_weight:.2f}_b{bm25_weight:.2f}_l{logits_weight:.2f}"
                            ),
                            (
                                f"Four-source shortlist for {combo_name}: 3 dense prompt sources + BM25, "
                                f"source_count>={min_sources}, rerank=dense/BM25/unfiltered logits"
                            ),
                            screen_scores,
                            data,
                            eval_args,
                            first500,
                            second500,
                            extra={
                                "phase": "logits_k3_four_source_screening_threeway_rerank",
                                "combo": combo_name,
                                "cells": list(spec_tuple),
                                "scorer": scorer,
                                "logits_method": "unfiltered_top256_log1p_relu",
                                "source_rule": f"source_ge{min_sources}",
                                "source_count": 4,
                                "shortlist_size": args.shortlist_size,
                                "dense_weight": dense_weight,
                                "bm25_weight": bm25_weight,
                                "logits_weight": logits_weight,
                                "shortlist_stats": screen_stats,
                            },
                        )
                    )

    return rows, {
        "logits_k3": {
            "combos": {
                name: [spec_to_json(DENSE_CELL_LIBRARY[cell_name]) for cell_name in cell_names]
                for name, cell_names in LOGITS_K3_COMBOS.items()
            },
            "dense_scorers": ["zsum", "vertical_concat_norm_weighted", "vector_average_component_norm"],
            "logits_methods": [
                {
                    "name": "promptreps_text_token_filtered",
                    "note": (
                        "Closest to PromptReps paper replication available in the saved tensor: "
                        "source-text token filter, ReLU+log1p, top128 quantized sparse impact weights."
                    ),
                },
                {
                    "name": "unfiltered_top256_log1p_relu",
                    "note": (
                        "Our exploratory semantic-expansion variant: use saved top256 next-token logits "
                        "without requiring the token to appear in the source text."
                    ),
                },
            ],
            "bm25": "Included as a standalone baseline, a dense+BM25 baseline, three-way fusion weight, and top20 screening source.",
            "weight_grid": [
                {"dense": dense, "bm25": bm25, "logits": logits}
                for dense, bm25, logits in LOGITS_K3_WEIGHT_GRID
            ],
            "shortlist_size": args.shortlist_size,
        }
    }


def combo_has_unique_variants(spec_names: tuple[str, ...]) -> bool:
    variants = [DENSE_CELL_LIBRARY[name].variant for name in spec_names]
    return len(variants) == len(set(variants))


def combo_label(spec_names: tuple[str, ...]) -> str:
    return "__".join(name.replace("_both_k15", "").replace("_both_k5", "_k5") for name in spec_names)


def recall_all_at_k(
    scores: np.ndarray,
    data: base.BenchmarkData,
    indices: list[int] | None,
    *,
    k: int,
) -> float:
    query_indices = range(len(data.query_ids)) if indices is None else indices
    hits = 0
    total = 0
    for query_index in query_indices:
        gold = set(data.gold_ids_by_query[query_index])
        order = np.argsort(scores[query_index])[::-1][:k]
        retrieved = {data.candidate_ids[int(index)] for index in order}
        hits += int(bool(gold & retrieved))
        total += 1
    return hits / max(total, 1)


def evaluate_selected_splits(
    name: str,
    description: str,
    scores: np.ndarray,
    data: base.BenchmarkData,
    eval_args: argparse.Namespace,
    first500: list[int],
    second500: list[int],
    *,
    extra: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = [
        evaluate_matrix_with_split(name, description, scores, data, eval_args, split_name="all", indices=None, extra=extra),
        evaluate_matrix_with_split(
            f"{name}_first500",
            f"First-half validation for {description}",
            scores,
            data,
            eval_args,
            split_name="first500",
            indices=first500,
            extra=extra,
        ),
    ]
    if second500:
        rows.append(
            evaluate_matrix_with_split(
                f"{name}_second500",
                f"Second-half validation for {description}",
                scores,
                data,
                eval_args,
                split_name="second500",
                indices=second500,
                extra=extra,
            )
        )
    return rows


def run_weight_grid_for_combo(
    combo_name: str,
    spec_tuple: tuple[str, ...],
    scorer: str,
    dense_scores: np.ndarray,
    bm25_scores: np.ndarray,
    sparse_scores_for_combo: np.ndarray,
    data: base.BenchmarkData,
    eval_args: argparse.Namespace,
    first500: list[int],
    second500: list[int],
    *,
    selection_score: float,
    selection_split: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    dense_z = base.row_zscore(dense_scores)
    bm25_z = base.row_zscore(bm25_scores)
    sparse_z = base.row_zscore(sparse_scores_for_combo)
    for logits_weight in WEIGHT_SWEEP_LOGITS_WEIGHTS:
        for bm25_weight in WEIGHT_SWEEP_BM25_WEIGHTS:
            dense_weight = 1.0 - bm25_weight - logits_weight
            if not 0.60 <= dense_weight <= 0.90:
                continue
            scores = dense_weight * dense_z + bm25_weight * bm25_z + logits_weight * sparse_z
            name = (
                f"combo_{combo_name}_{scorer}_w"
                f"d{dense_weight:.2f}_b{bm25_weight:.2f}_l{logits_weight:.2f}"
            )
            rows.extend(
                evaluate_selected_splits(
                    name,
                    (
                        f"Selected K3 combo dense/BM25/PromptReps weight sweep: {combo_name}, "
                        f"scorer={scorer}, weights=({dense_weight:.2f},{bm25_weight:.2f},{logits_weight:.2f})"
                    ),
                    scores,
                    data,
                    eval_args,
                    first500,
                    second500,
                    extra={
                        "phase": "combo_sweep_weight_grid",
                        "combo": combo_name,
                        "cells": list(spec_tuple),
                        "scorer": scorer,
                        "dense_weight": dense_weight,
                        "bm25_weight": bm25_weight,
                        "logits_weight": logits_weight,
                        "selection_score": selection_score,
                        "selection_split": selection_split,
                    },
                )
            )
    return rows


def run_logits_screening_for_combo(
    combo_name: str,
    spec_tuple: tuple[str, ...],
    scorer: str,
    dense_scores: np.ndarray,
    bm25_scores: np.ndarray,
    sparse_scores_for_combo: np.ndarray,
    data: base.BenchmarkData,
    eval_args: argparse.Namespace,
    first500: list[int],
    second500: list[int],
    *,
    shortlist_size: int,
    screen_alpha: float,
) -> list[dict[str, Any]]:
    rerank_scores = screen_alpha * base.row_zscore(dense_scores) + (1.0 - screen_alpha) * base.row_zscore(bm25_scores)
    screen_sources = {
        "logits": [sparse_scores_for_combo],
        "bm25_logits": [bm25_scores, sparse_scores_for_combo],
        "dense_bm25_logits": [dense_scores, bm25_scores, sparse_scores_for_combo],
    }
    rows: list[dict[str, Any]] = []
    for screen_name, source_scores in screen_sources.items():
        scores = shortlist_union_rerank_scores(rerank_scores, source_scores, shortlist_size=shortlist_size)
        name = f"combo_{combo_name}_{scorer}_screen_{screen_name}_top{shortlist_size}_alpha{screen_alpha:.2f}"
        rows.extend(
            evaluate_selected_splits(
                name,
                (
                    f"Logits shortlist screening for selected K3 combo: {combo_name}, "
                    f"screen={screen_name}, top{shortlist_size}, rerank=dense/BM25 alpha {screen_alpha:.2f}"
                ),
                scores,
                data,
                eval_args,
                first500,
                second500,
                extra={
                    "phase": "combo_sweep_logits_screening",
                    "combo": combo_name,
                    "cells": list(spec_tuple),
                    "scorer": scorer,
                    "screen": screen_name,
                    "shortlist_size": shortlist_size,
                    "screen_alpha": screen_alpha,
                },
            )
        )
    return rows


def shortlist_union_rerank_scores(
    rerank_scores: np.ndarray,
    screen_scores: list[np.ndarray],
    *,
    shortlist_size: int,
) -> np.ndarray:
    query_count, candidate_count = rerank_scores.shape
    output = np.empty_like(rerank_scores, dtype=np.float32)
    for query_index in range(query_count):
        base_order = np.argsort(rerank_scores[query_index])[::-1]
        output[query_index, base_order] = -1_000_000.0 - np.arange(candidate_count, dtype=np.float32)
        shortlist: set[int] = set()
        for source in screen_scores:
            order = np.argsort(source[query_index])[::-1][:shortlist_size]
            shortlist.update(int(index) for index in order)
        shortlist_indices = np.asarray(sorted(shortlist), dtype=np.int32)
        if shortlist_indices.size:
            output[query_index, shortlist_indices] = (
                1_000_000.0 + zscore_1d(rerank_scores[query_index, shortlist_indices])
            )
    return output


def source_agreement_rerank_scores(
    rerank_scores: np.ndarray,
    source_scores: list[np.ndarray],
    data: base.BenchmarkData,
    *,
    shortlist_size: int,
    min_sources: int,
) -> tuple[np.ndarray, dict[str, Any]]:
    query_count, candidate_count = rerank_scores.shape
    output = np.empty_like(rerank_scores, dtype=np.float32)
    shortlist_sizes: list[int] = []
    oracle_hits = 0
    for query_index in range(query_count):
        base_order = np.argsort(rerank_scores[query_index])[::-1]
        output[query_index, base_order] = -1_000_000.0 - np.arange(candidate_count, dtype=np.float32)
        source_counts: dict[int, int] = {}
        for source in source_scores:
            order = np.argsort(source[query_index])[::-1][:shortlist_size]
            for candidate_index in order:
                index = int(candidate_index)
                source_counts[index] = source_counts.get(index, 0) + 1
        shortlist = [index for index, count in source_counts.items() if count >= min_sources]
        shortlist_indices = np.asarray(sorted(shortlist), dtype=np.int32)
        shortlist_sizes.append(int(shortlist_indices.size))
        if shortlist_indices.size:
            gold = set(data.gold_ids_by_query[query_index])
            retrieved = {data.candidate_ids[int(index)] for index in shortlist_indices}
            oracle_hits += int(bool(gold & retrieved))
            output[query_index, shortlist_indices] = (
                1_000_000.0 + zscore_1d(rerank_scores[query_index, shortlist_indices])
            )
    stats = {
        "avg_shortlist_size": float(np.mean(shortlist_sizes)) if shortlist_sizes else 0.0,
        "min_shortlist_size": int(min(shortlist_sizes)) if shortlist_sizes else 0,
        "max_shortlist_size": int(max(shortlist_sizes)) if shortlist_sizes else 0,
        "oracle_hit": float(oracle_hits / max(query_count, 1)),
        "min_sources": min_sources,
        "per_source_topk": shortlist_size,
    }
    return output, stats


def load_dense_specs(arrays: Any, specs: dict[str, DenseCellSpec]) -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    for name, spec in specs.items():
        candidates = np.asarray(arrays[f"{spec.storage_label}::candidates"], dtype=np.float32)
        queries = np.asarray(arrays[f"{spec.storage_label}::queries"], dtype=np.float32)
        mean, pcs = fit_pcs(candidates, max(ANTI_PCA_KS))
        candidate_vectors, query_vectors = transform_vectors(candidates, queries, mean, pcs, spec.transform, spec.k)
        scores = base.normalize_rows(query_vectors) @ base.normalize_rows(candidate_vectors).T
        loaded[name] = {
            "spec": spec,
            "candidates": candidate_vectors,
            "queries": query_vectors,
            "scores": scores.astype(np.float32, copy=False),
        }
        base.log(f"loaded dense spec {name}: {spec.storage_label} -> {spec.transform} k={spec.k}")
    return loaded


def load_dense_specs_from_tensor_dirs(
    tensor_dirs: list[Path],
    specs: dict[str, DenseCellSpec],
) -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    remaining = dict(specs)
    for tensor_dir in tensor_dirs:
        if not remaining:
            break
        vectors_path = tensor_dir / "raw_hidden_vectors.npz"
        if not vectors_path.exists():
            raise FileNotFoundError(f"Missing raw hidden vectors: {vectors_path}")
        with np.load(vectors_path) as arrays:
            available_keys = set(arrays.files)
            available = {
                name: spec
                for name, spec in remaining.items()
                if f"{spec.storage_label}::candidates" in available_keys
                and f"{spec.storage_label}::queries" in available_keys
            }
            if not available:
                continue
            base.log(f"loading {len(available)} dense spec(s) from {tensor_dir}")
            loaded.update(load_dense_specs(arrays, available))
            for name in available:
                remaining.pop(name, None)
    if remaining:
        missing = {
            name: {
                "variant": spec.variant,
                "layer": spec.layer,
                "storage_label": spec.storage_label,
            }
            for name, spec in remaining.items()
        }
        raise KeyError(f"Missing dense tensor arrays for selected specs: {missing}")
    return loaded


def weighted_row_zscore_sum(score_matrices: list[np.ndarray], weights: tuple[float, ...]) -> np.ndarray:
    output = np.zeros_like(score_matrices[0], dtype=np.float32)
    for weight, scores in zip(weights, score_matrices, strict=True):
        output += np.float32(weight) * base.row_zscore(scores)
    return output


def score_zsum(combo_specs: list[dict[str, Any]]) -> np.ndarray:
    output = np.zeros_like(combo_specs[0]["scores"], dtype=np.float32)
    for item in combo_specs:
        output += base.row_zscore(item["scores"])
    return output


def score_vertical_concat(combo_specs: list[dict[str, Any]], *, component_normalize: bool) -> np.ndarray:
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
    candidates = base.normalize_rows(np.concatenate(candidate_parts, axis=1))
    queries = base.normalize_rows(np.concatenate(query_parts, axis=1))
    return queries @ candidates.T


def score_vector_average(combo_specs: list[dict[str, Any]], *, component_normalize: bool) -> np.ndarray:
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
    candidates = base.normalize_rows(np.mean(np.stack(candidate_parts, axis=0), axis=0))
    queries = base.normalize_rows(np.mean(np.stack(query_parts, axis=0), axis=0))
    return queries @ candidates.T


def evaluate_matrix_with_split(
    name: str,
    description: str,
    scores: np.ndarray,
    data: base.BenchmarkData,
    eval_args: argparse.Namespace,
    *,
    split_name: str,
    indices: list[int] | None,
    extra: dict[str, Any],
) -> dict[str, Any]:
    if indices is None:
        split_scores = scores
        split_data = data
    else:
        split_scores = scores[indices]
        split_data = subset_queries(data, indices)
    row = base.evaluate_score_matrix(name, description, split_scores, split_data, eval_args, extra=extra)
    row["split"] = split_name
    return row


def subset_queries(data: base.BenchmarkData, indices: list[int]) -> base.BenchmarkData:
    return base.BenchmarkData(
        task=data.task,
        dataset_id=data.dataset_id,
        items=data.items,
        candidate_ids=data.candidate_ids,
        candidate_texts=data.candidate_texts,
        query_ids=[data.query_ids[index] for index in indices],
        query_texts=[data.query_texts[index] for index in indices],
        gold_ids_by_query=[data.gold_ids_by_query[index] for index in indices],
    )


def oracle_union_row(
    combo_name: str,
    spec_names: tuple[str, ...],
    loaded: dict[str, dict[str, Any]],
    data: base.BenchmarkData,
    indices: list[int],
    split_name: str,
) -> dict[str, Any]:
    any_hits = 0
    all_hits = 0
    component_any_hits = [0 for _ in spec_names]
    jaccards = []
    for query_index in indices:
        gold = set(data.gold_ids_by_query[query_index])
        union_ids: set[str] = set()
        component_sets = []
        for spec_offset, spec_name in enumerate(spec_names):
            order = np.argsort(loaded[spec_name]["scores"][query_index])[::-1][:5]
            ids = {data.candidate_ids[int(index)] for index in order}
            component_sets.append(ids)
            union_ids.update(ids)
            component_any_hits[spec_offset] += int(bool(gold & ids))
        any_hits += int(bool(gold & union_ids))
        all_hits += int(gold.issubset(union_ids))
        for left in range(len(component_sets)):
            for right in range(left + 1, len(component_sets)):
                denom = len(component_sets[left] | component_sets[right])
                jaccards.append(0.0 if denom == 0 else len(component_sets[left] & component_sets[right]) / denom)
    total = max(len(indices), 1)
    return {
        "combo": combo_name,
        "split": split_name,
        "cells": list(spec_names),
        "n_queries": len(indices),
        "oracle_any_hit_at5": any_hits / total,
        "oracle_recall_all_at5": all_hits / total,
        "best_component_any_hit_at5": max(component_any_hits) / total if component_any_hits else 0.0,
        "oracle_any_gain_vs_best_component": (any_hits - max(component_any_hits, default=0)) / total,
        "mean_pairwise_jaccard_at5": float(np.mean(jaccards)) if jaccards else 0.0,
    }


def evaluate_transform_grid(
    variant: str,
    layer: int,
    family: str,
    candidates: np.ndarray,
    queries: np.ndarray,
    data: base.BenchmarkData,
    eval_args: argparse.Namespace,
) -> list[dict[str, Any]]:
    rows = []
    mean, pcs50 = fit_pcs(candidates, max(ANTI_PCA_KS))
    specs: list[tuple[str, str, int | None]] = [
        ("raw_cosine", "raw hidden vectors with L2-normalized cosine", None),
        ("centered_cosine", "candidate mean subtracted from candidates and queries, then L2-normalized cosine", None),
    ]
    specs.extend(("anti_pca_both", "candidate mean and top-k PCs removed from candidates and queries", k) for k in ANTI_PCA_KS)
    specs.extend(("anti_pca_query_only", "candidate raw; query subtracts candidate mean and removes top-k candidate PCs", k) for k in ANTI_PCA_KS)
    specs.append(("anti_pca_candidate_only", "candidate subtracts candidate mean and removes top-10 PCs; query raw", 10))
    for transform, description, k in specs:
        scores = score_transform(candidates, queries, mean, pcs50, transform=transform, k=k)
        suffix = transform if k is None else f"{transform}_k{k}"
        name = f"{variant}_L{layer}_{suffix}"
        rows.append(
            base.evaluate_score_matrix(
                name,
                f"PrefEval Stage 1 anti-PCA calibration: {variant}, L{layer}, {description}",
                scores,
                data,
                eval_args,
                extra={
                    "cell": {"variant": variant, "layer": layer, "family": family},
                    "transform": transform,
                    "k": k,
                    "phase": "anti_pca_calibration",
                },
            )
        )
    return rows


def fit_pcs(candidates: np.ndarray, max_components: int) -> tuple[np.ndarray, np.ndarray]:
    mean = np.mean(candidates, axis=0).astype(np.float32, copy=False)
    centered = candidates - mean
    _u, _s, vt = np.linalg.svd(centered.astype(np.float32, copy=False), full_matrices=False)
    return mean, vt[: min(max_components, vt.shape[0])].astype(np.float32, copy=False)


def score_transform(
    candidates: np.ndarray,
    queries: np.ndarray,
    mean: np.ndarray,
    pcs: np.ndarray,
    *,
    transform: str,
    k: int | None,
) -> np.ndarray:
    candidate_vectors, query_vectors = transform_vectors(candidates, queries, mean, pcs, transform, k)
    return base.normalize_rows(query_vectors) @ base.normalize_rows(candidate_vectors).T


def transform_vectors(
    candidates: np.ndarray,
    queries: np.ndarray,
    mean: np.ndarray,
    pcs: np.ndarray,
    transform: str,
    k: int | None,
) -> tuple[np.ndarray, np.ndarray]:
    if transform == "raw_cosine":
        candidate_vectors = candidates
        query_vectors = queries
    elif transform == "centered_cosine":
        candidate_vectors = candidates - mean
        query_vectors = queries - mean
    elif transform == "anti_pca_both":
        candidate_vectors = remove_pc_projection(candidates - mean, pcs[: int(k)])
        query_vectors = remove_pc_projection(queries - mean, pcs[: int(k)])
    elif transform == "anti_pca_query_only":
        candidate_vectors = candidates
        query_vectors = remove_pc_projection(queries - mean, pcs[: int(k)])
    elif transform == "anti_pca_candidate_only":
        candidate_vectors = remove_pc_projection(candidates - mean, pcs[: int(k)])
        query_vectors = queries
    else:
        raise ValueError(f"Unsupported transform: {transform}")
    return candidate_vectors.astype(np.float32, copy=False), query_vectors.astype(np.float32, copy=False)


def remove_pc_projection(vectors: np.ndarray, pcs: np.ndarray) -> np.ndarray:
    if pcs.size == 0:
        return vectors.astype(np.float32, copy=False)
    return (vectors - (vectors @ pcs.T) @ pcs).astype(np.float32, copy=False)


def ensure_findings_skeleton(path: Path) -> None:
    if path.exists():
        return
    path.write_text(
        "\n".join(
            [
                "# PrefEval n=1000 Stage 1 Findings",
                "",
                "This note tracks offline analysis over the PrefEval implicit_persona n=1000 run.",
                "The benchmark is separate from the LongMemEval Stage 1-3 line, so conclusions",
                "are recorded here instead of in `notes/results_log.md`.",
                "",
                "## Setup",
                "",
                "- Data: `benchmarks/PrefEval/data/implicit_persona_n1000_pruned_hidden_l28_l29_l30_l31_logits256_promptreps128_20260512.jsonl`",
                "- Tensor store: `benchmarks/PrefEval/tensors/hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128/`",
                "- Stored vectors are raw extractor outputs. The original n=1000 prompt-sweep results applied `anti_pca_both_k15` and L2-normalized cosine at scoring time.",
                "",
                "## Anti-PCA Calibration",
                "",
                "_Pending._",
                "",
                "## Dense K3 Fusion",
                "",
                "_Pending._",
                "",
                "## PromptReps Logit Fusion",
                "",
                "_Pending._",
                "",
                "## BM25 Fusion",
                "",
                "_Pending._",
                "",
                "## Split Stability",
                "",
                "_Pending._",
                "",
            ]
        ),
        encoding="utf-8",
    )


def spec_to_json(spec: DenseCellSpec) -> dict[str, Any]:
    return {
        "name": spec.name,
        "variant": spec.variant,
        "layer": spec.layer,
        "transform": spec.transform,
        "k": spec.k,
        "family": spec.family,
        "storage_label": spec.storage_label,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# PrefEval Stage 1 Offline Analysis",
        "",
        f"- Created UTC: `{payload['created_utc']}`",
        f"- Analysis: `{payload['analysis']}`",
        f"- Items: `{payload['task_summary']['items']}`",
        f"- Tensor dir: `{payload['inputs']['tensor_dir']}`",
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
            "| rank | split | config | R@1 | R@3 | R@5 | NDCG@5 | MRR |",
            "|---:|---|---|---:|---:|---:|---:|---:|",
        ]
    )
    for index, row in enumerate(payload["rows"], start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | `{row.get('split', 'all')}` | `{row['name']}` | {summary['recall_all@1']:.3f} | "
            f"{summary['recall_all@3']:.3f} | {summary['recall_all@5']:.3f} | "
            f"{summary['ndcg_any@5']:.3f} | {summary['mrr']:.3f} |"
        )
    diagnostic_rows = payload.get("oracle_union_rows") or payload.get("layer_overlap_rows")
    if diagnostic_rows:
        lines.extend(
            [
                "",
                "## Oracle Union Diagnostics",
                "",
                "| combo | split | any_hit@5 | recall_all@5 | best_component_any@5 | gain | mean_jaccard@5 |",
                "|---|---|---:|---:|---:|---:|---:|",
            ]
        )
        for row in diagnostic_rows:
            lines.append(
                f"| `{row['combo']}` | `{row['split']}` | {row['oracle_any_hit_at5']:.3f} | "
                f"{row['oracle_recall_all_at5']:.3f} | {row['best_component_any_hit_at5']:.3f} | "
                f"{row['oracle_any_gain_vs_best_component']:.3f} | {row['mean_pairwise_jaccard_at5']:.3f} |"
            )
    lines.extend(["", "## Configs", ""])
    for row in payload["rows"]:
        transform = row.get("transform", row.get("scorer", ""))
        k = "" if row.get("k") is None else f", k={row['k']}"
        suffix = f" ({transform}{k})" if transform else ""
        lines.append(f"- `{row['name']}`: {row['description']}{suffix}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
