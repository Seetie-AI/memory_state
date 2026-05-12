"""Stage 3 prompt-vector fusion experiments over saved prompt-sweep vectors.

This script tests whether multiple prompt views can improve chatbot memory
retrieval beyond the best single Stage 3 hidden-state retriever. It does not
rerun the model; it reuses the Stage 3 merged prompt-sweep store and the MLX
chunk-batched cell loader from `stage3_offline_analyze.py`.

Design constraints:

- K is limited to 2 and 3. The user wants a product-relevant 20/80 point, and
  K=3 is already enough to test whether different prompt facets complement one
  another. At the storage layer, one 4096-d bf16 vector is 8KB, so K=3 is 24KB
  per memory, comfortably inside the target 10-100KB range. fp8 K=3 would be
  12KB, but fp8/int8 quantization is a future storage-quality experiment.
- Audit comes first. Fusion only helps if prompt views make different mistakes,
  so Phase 1 measures complementarity before spending effort on concat or
  late-interaction scoring.
- Phase 4 is anti-PCA only. `centered_cosine` is not a persistable vector
  transform because its mean is the per-query candidate subset mean; using it
  inside concat would change the experiment definition. Centered cells still
  appear in Phase 1 audit and Phase 3 score fusion, but vector fusion selects
  only anti-PCA/query-only cells.
- Query-only anti-PCA preserves its original asymmetry in vector fusion:
  candidate vectors stay raw while query vectors are transformed. This keeps
  the same retrieval semantics that made query-only useful in Stage 2/3.
- Vertical concat treats K prompt vectors as one thicker vector. The primary
  concat scorer normalizes each 4096-d component first, then normalizes the
  concatenated vector, so the test measures equal-weight "information
  thickening" rather than letting component vector norms become hidden prompt
  weights. A norm-weighted concat variant is kept as a diagnostic.
- Vector average collapses K prompt vectors back to one 4096-d vector before
  scoring. The primary average normalizes each component first so every prompt
  contributes equally; a raw norm-weighted average is kept as a storage-friendly
  diagnostic.
- Side-by-side max-sim keeps K prompt facets separate and lets each query facet
  match the candidate facet it likes best, which is a better chatbot-memory
  intuition: different user queries may care about facts, tags, needs, or
  persona facets.
- Row-aligned matrix scoring treats K prompt vectors as H in R^{D x K}: each
  hidden dimension gets a K-wide prompt-response profile. It compares those row
  profiles between query and memory, then aggregates over dimensions. Because
  this assumes the hidden coordinates share a layer-wise basis, the script tests
  both the selected cells' best layers and a same-layer L30 variant.
- We do not run PCA in the concatenated space. K=7 would create a 28,672-d
  vector whose covariance matrix alone is about 3.3GB fp32 and whose eigensolve
  would violate the 8GB target / 10GB hard limit.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
for path in [SCRIPTS, SRC]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import stage2_offline_analyze as offline
from eval.longmemeval_metrics import Prediction, evaluate
from stage3_offline_analyze import load_cell_vectors_mlx


DEFAULT_DUMP_DIR = ROOT / "tensors" / "stage3" / "prompt_sweep" / "merged_subset0-100_cache2gb_logits256"
DEFAULT_DATA = ROOT / "data" / "longmemeval_s_cleaned.json"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "prompt_fusion"
DEFAULT_OUTPUT_PREFIX = "findings_v2"
DEFAULT_TOP_K = 50
BASELINE_SINGLE_R5 = 0.7659574468085106
BASELINE_SINGLE_NDCG = 0.7837910207130874


@dataclass(frozen=True)
class CellConfig:
    variant: str
    layer: int
    score_mode: str
    family: str

    @property
    def label(self) -> str:
        return f"{self.variant}|layer{self.layer}|last|{self.score_mode}"

    @property
    def is_persistable(self) -> bool:
        return self.score_mode in {"anti_pca_both_k15", "query_only_anti_pca_k2"}


@dataclass(frozen=True)
class ScoredItem:
    question_id: str
    instance_index: int
    candidate_ids: tuple[str, ...]
    scores: tuple[float, ...]
    ranked_ids: tuple[str, ...]
    gold_ids: tuple[str, ...]
    is_abstention: bool
    has_target: bool

    def prediction(self) -> Prediction:
        return Prediction(
            question_id=self.question_id,
            retrieved_ids=list(self.ranked_ids),
            gold_ids=list(self.gold_ids),
            is_abstention=self.is_abstention,
            has_target=self.has_target,
        )


@dataclass
class CellRun:
    cell: CellConfig
    items: list[ScoredItem]
    metrics: dict[str, Any]
    session_metrics: dict[str, float]
    rank_metrics: dict[str, Any]
    summary: dict[str, Any]


@dataclass
class VectorRepr:
    cell: CellConfig
    candidate_vectors: np.ndarray
    query_vectors: np.ndarray
    representation_note: str


BEST_CELLS: list[CellConfig] = [
    CellConfig("2-3-2_mem", 31, "anti_pca_both_k15", "mem-key"),
    CellConfig("2-4-1_user_word", 30, "anti_pca_both_k15", "persona"),
    CellConfig("1-3", 31, "anti_pca_both_k15", "tag"),
    CellConfig("P0", 30, "anti_pca_both_k15", "anchor"),
    CellConfig("1-1_CN", 29, "centered_cosine", "content-summary"),
    CellConfig("2-1", 30, "anti_pca_both_k15", "topic"),
    CellConfig("1-1_CN_ASCII", 29, "query_only_anti_pca_k2", "content-summary"),
    CellConfig("2-3-2_query", 29, "anti_pca_both_k15", "query-key"),
    CellConfig("2-3-1", 30, "anti_pca_both_k15", "mem-key"),
    CellConfig("1-2", 29, "anti_pca_both_k15", "summary"),
    CellConfig("2-5", 29, "query_only_anti_pca_k2", "association"),
    CellConfig("2-4-1", 30, "query_only_anti_pca_k2", "persona"),
    CellConfig("2-6", 30, "anti_pca_both_k15", "impression"),
    CellConfig("1-1_EN", 31, "anti_pca_both_k15", "content-summary"),
    CellConfig("2-4-2", 29, "anti_pca_both_k15", "need"),
    CellConfig("2-7", 31, "anti_pca_both_k15", "style"),
    CellConfig("2-8", 31, "anti_pca_both_k15", "strategy"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--limit-audit-cells", type=int, default=None)
    parser.add_argument(
        "--selected-variants",
        default=None,
        help=(
            "Comma-separated variants to use for phases 2-4 after Phase 1. "
            "Each variant maps to its Stage 3 best cell. When omitted, the "
            "script auto-selects top cells from Phase 1."
        ),
    )
    parser.add_argument(
        "--audit-only",
        action="store_true",
        help="Run Phase 1 audit and write outputs, then skip phases 2-4 for human prompt selection.",
    )
    parser.add_argument(
        "--limit-fusion-K",
        type=int,
        choices=[2, 3],
        default=None,
        help="Smoke-test limiter. Default runs K=2 and K=3.",
    )
    parser.add_argument(
        "--reference-variant",
        default="1-3",
        help="Variant used as the ranking-comparison reference in v2 diagnostics.",
    )
    parser.add_argument(
        "--uniform-vector-layers",
        default="30",
        help="Comma-separated layers for same-config vector fusion, e.g. '30' or '29,30,31'.",
    )
    parser.add_argument(
        "--vector-average-only",
        action="store_true",
        help=(
            "Skip audit/asymmetric/score-fusion phases and run only Phase 4 "
            "vector_average_* methods. Requires --selected-variants."
        ),
    )
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.audit_only and args.vector_average_only:
        raise ValueError("--audit-only and --vector-average-only cannot be combined.")
    started = time.perf_counter()

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

    cells = BEST_CELLS[: args.limit_audit_cells] if args.limit_audit_cells else list(BEST_CELLS)
    k_values = [args.limit_fusion_K] if args.limit_fusion_K else [2, 3]
    uniform_layers = parse_int_list(args.uniform_vector_layers)
    print(
        f"records={len(records)} audit_cells={len(cells)} K={k_values} "
        f"bootstrap={args.bootstrap_samples} uniform_layers={uniform_layers} "
        f"vector_average_only={args.vector_average_only}"
    )

    if args.vector_average_only:
        if not args.selected_variants:
            raise ValueError("--vector-average-only requires --selected-variants.")
        phase1 = {"runs": [], "pairwise": [], "note": "Skipped because --vector-average-only was set."}
        selected = parse_selected_variants(args.selected_variants, list(BEST_CELLS))
        reference_run = None
        print("phase1 skipped for vector-average-only run")
    else:
        phase1 = run_phase1_audit(dump_dir, manifest, records, cells, args.top_k, args.bootstrap_samples)
        if args.selected_variants:
            selected = parse_selected_variants(args.selected_variants, cells)
        else:
            selected = select_top3_for_vector_fusion(phase1["runs"], phase1["pairwise"])
        reference_run = select_reference_run(phase1["runs"], args.reference_variant)
    print("selected top cells:", ", ".join(cell.label for cell in selected))
    if reference_run:
        print(f"reference cell: {reference_run.cell.label}")
    else:
        print(f"reference cell: none found for variant {args.reference_variant!r}")

    if args.audit_only:
        phase2 = {"rows": [], "note": "Skipped because --audit-only was set."}
        phase3 = {"rows": [], "note": "Skipped because --audit-only was set."}
        phase4 = {"rows": [], "note": "Skipped because --audit-only was set."}
    elif args.vector_average_only:
        phase2 = {"rows": [], "note": "Skipped because --vector-average-only was set."}
        phase3 = {"rows": [], "note": "Skipped because --vector-average-only was set."}
        phase4 = run_phase4_vector_fusion(
            dump_dir,
            manifest,
            records,
            buckets,
            selected,
            k_values,
            args.top_k,
            args.bootstrap_samples,
            uniform_layers=uniform_layers,
            reference_run=reference_run,
            vector_methods={"vector_average_component_norm", "vector_average_norm_weighted"},
        )
    else:
        phase2 = run_phase2_asymmetric(
            dump_dir,
            manifest,
            records,
            selected,
            args.top_k,
            args.bootstrap_samples,
        )
        phase3 = run_phase3_score_fusion(
            phase1["runs"],
            selected,
            k_values,
            args.bootstrap_samples,
            reference_run=reference_run,
        )
        phase4 = run_phase4_vector_fusion(
            dump_dir,
            manifest,
            records,
            buckets,
            selected,
            k_values,
            args.top_k,
            args.bootstrap_samples,
            uniform_layers=uniform_layers,
            reference_run=reference_run,
            vector_methods=None,
        )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "stage3_prompt_fusion_v2",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "limit_audit_cells": args.limit_audit_cells,
            "limit_fusion_K": args.limit_fusion_K,
            "selected_variants": args.selected_variants,
            "audit_only": args.audit_only,
            "reference_variant": args.reference_variant,
            "uniform_vector_layers": uniform_layers,
            "vector_average_only": args.vector_average_only,
        },
        "baselines": {
            "best_single_r5": BASELINE_SINGLE_R5,
            "best_single_ndcg": BASELINE_SINGLE_NDCG,
        },
        "selected_cells": [cell_to_json(cell) for cell in selected],
        "phase1_audit": {
            "cell_results": [cell_run_to_json(run) for run in phase1["runs"]],
            "pairwise": phase1["pairwise"],
            "centered_future_work": centered_future_work_notes(phase1["runs"], selected, phase1["pairwise"]),
        },
        "phase2_asymmetric": phase2,
        "phase3_score_fusion": phase3,
        "phase4_vector_fusion": phase4,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(f"elapsed {format_seconds(payload['elapsed_seconds'])}")
    return 0


def run_phase1_audit(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    cells: list[CellConfig],
    top_k: int,
    bootstrap_samples: int,
) -> dict[str, Any]:
    runs = []
    for index, cell in enumerate(cells, start=1):
        print(f"phase1 [{index}/{len(cells)}] {cell.label}")
        runs.append(evaluate_cell_pair(dump_dir, manifest, records, cell, cell, top_k, bootstrap_samples))
    pairwise = pairwise_complementarity(runs)
    return {"runs": runs, "pairwise": pairwise}


def run_phase2_asymmetric(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    selected: list[CellConfig],
    top_k: int,
    bootstrap_samples: int,
) -> dict[str, Any]:
    rows = []
    for candidate_cell in selected:
        for query_cell in selected:
            print(f"phase2 asym {candidate_cell.variant} -> {query_cell.variant}")
            run = evaluate_cell_pair(
                dump_dir,
                manifest,
                records,
                candidate_cell,
                query_cell,
                top_k,
                bootstrap_samples,
            )
            row = cell_run_to_json(run)
            row["candidate_cell"] = cell_to_json(candidate_cell)
            row["query_cell"] = cell_to_json(query_cell)
            row["config"] = f"{candidate_cell.label} -> {query_cell.label}"
            rows.append(row)
    return {"rows": sorted(rows, key=lambda row: metric_sort_key(row["summary"]), reverse=True)}


def run_phase3_score_fusion(
    runs: list[CellRun],
    selected: list[CellConfig],
    k_values: list[int],
    bootstrap_samples: int,
    *,
    reference_run: CellRun | None = None,
) -> dict[str, Any]:
    runs_by_label = {run.cell.label: run for run in runs}
    selected_runs = [runs_by_label[cell.label] for cell in selected if cell.label in runs_by_label]
    rows = []
    for k in k_values:
        if len(selected_runs) < k:
            continue
        for combo in itertools.combinations(selected_runs, k):
            for method in ["rrf", "zsum"]:
                predictions = fuse_score_runs(combo, method)
                metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
                row = {
                    "method": method,
                    "k": k,
                    "cells": [cell_to_json(run.cell) for run in combo],
                    "metrics": metrics,
                    "session_metrics": offline.session_retrieval_metrics(predictions),
                    "rank_metrics": offline.rank_metrics(predictions),
                }
                row["summary"] = summarize_metrics(row["metrics"], row["session_metrics"], row["rank_metrics"])
                add_reference_diagnostics(row, predictions, reference_run)
                rows.append(row)
    return {"rows": sorted(rows, key=lambda row: metric_sort_key(row["summary"]), reverse=True)}


def run_phase4_vector_fusion(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    selected: list[CellConfig],
    k_values: list[int],
    top_k: int,
    bootstrap_samples: int,
    *,
    uniform_layers: list[int],
    reference_run: CellRun | None = None,
    vector_methods: set[str] | None = None,
) -> dict[str, Any]:
    persistable = [cell for cell in selected if cell.is_persistable]
    if len(persistable) < 2:
        return {"rows": [], "note": "Fewer than two persistable anti-PCA cells selected."}

    reprs = build_vector_representations(dump_dir, manifest, records, persistable)
    rows = []
    selected_layer_methods = filter_methods(
        [
            "vector_average_component_norm",
            "vector_average_norm_weighted",
            "vertical_concat_component_norm",
            "vertical_concat_norm_weighted",
            "maxsim_sum",
            "row_aligned_unweighted_selected_layers",
            "row_aligned_weighted_selected_layers",
        ],
        vector_methods,
    )
    for k in k_values:
        if len(persistable) < k:
            continue
        for combo in itertools.combinations(persistable, k):
            combo_reprs = [reprs[cell.label] for cell in combo]
            for method in selected_layer_methods:
                predictions = predictions_from_vector_fusion(
                    records,
                    buckets,
                    combo_reprs,
                    method=method,
                    top_k=top_k,
                )
                metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
                row = {
                    "method": method,
                    "k": k,
                    "cells": [cell_to_json(cell) for cell in combo],
                    "representation_notes": [reprs[cell.label].representation_note for cell in combo],
                    "metrics": metrics,
                    "session_metrics": offline.session_retrieval_metrics(predictions),
                    "rank_metrics": offline.rank_metrics(predictions),
                }
                row["summary"] = summarize_metrics(row["metrics"], row["session_metrics"], row["rank_metrics"])
                add_reference_diagnostics(row, predictions, reference_run)
                rows.append(row)
    same_layer_methods = filter_methods(
        ["row_aligned_unweighted_same_layer30", "row_aligned_weighted_same_layer30"],
        vector_methods,
    )
    if same_layer_methods:
        same_layer_rows = run_same_layer_row_aligned(
            dump_dir,
            manifest,
            records,
            buckets,
            persistable,
            k_values,
            top_k,
            bootstrap_samples,
            layer=30,
            reference_run=reference_run,
            methods=same_layer_methods,
        )
        rows.extend(same_layer_rows)
    uniform_methods = filter_methods(
        [
            "vector_average_component_norm",
            "vector_average_norm_weighted",
            "vertical_concat_component_norm",
            "vertical_concat_norm_weighted",
            "maxsim_sum",
            "row_aligned_unweighted_selected_layers",
            "row_aligned_weighted_selected_layers",
        ],
        vector_methods,
    )
    for layer in uniform_layers:
        uniform_rows = run_uniform_config_vector_fusion(
            dump_dir,
            manifest,
            records,
            buckets,
            persistable,
            k_values,
            top_k,
            bootstrap_samples,
            layer=layer,
            score_mode="anti_pca_both_k15",
            reference_run=reference_run,
            methods=uniform_methods,
        )
        rows.extend(uniform_rows)
    return {"rows": sorted(rows, key=lambda row: metric_sort_key(row["summary"]), reverse=True)}


def run_same_layer_row_aligned(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    selected: list[CellConfig],
    k_values: list[int],
    top_k: int,
    bootstrap_samples: int,
    *,
    layer: int,
    reference_run: CellRun | None = None,
    methods: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Run row-aligned scoring with all selected variants forced to one layer.

    Row alignment assumes dimension `d` has the same coordinate meaning across
    prompt views. That assumption is cleaner when all prompt vectors come from
    the same model layer. We use anti-PCA-both k=15 for these forced-layer cells
    because Phase 4 only uses persistable vector representations.
    """
    variants = []
    seen = set()
    for cell in selected:
        if cell.variant not in seen:
            variants.append(cell)
            seen.add(cell.variant)
    same_layer_cells = [
        CellConfig(cell.variant, layer, "anti_pca_both_k15", cell.family)
        for cell in variants
    ]
    if len(same_layer_cells) < 2:
        return []
    reprs = build_vector_representations(dump_dir, manifest, records, same_layer_cells)
    rows = []
    for k in k_values:
        if len(same_layer_cells) < k:
            continue
        for combo in itertools.combinations(same_layer_cells, k):
            combo_reprs = [reprs[cell.label] for cell in combo]
            for method in methods or ["row_aligned_unweighted_same_layer30", "row_aligned_weighted_same_layer30"]:
                predictions = predictions_from_vector_fusion(
                    records,
                    buckets,
                    combo_reprs,
                    method=method,
                    top_k=top_k,
                )
                metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
                row = {
                    "method": method,
                    "k": k,
                    "cells": [cell_to_json(cell) for cell in combo],
                    "representation_notes": [reprs[cell.label].representation_note for cell in combo],
                    "metrics": metrics,
                    "session_metrics": offline.session_retrieval_metrics(predictions),
                    "rank_metrics": offline.rank_metrics(predictions),
                }
                row["summary"] = summarize_metrics(row["metrics"], row["session_metrics"], row["rank_metrics"])
                add_reference_diagnostics(row, predictions, reference_run)
                rows.append(row)
    return rows


def run_uniform_config_vector_fusion(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    selected: list[CellConfig],
    k_values: list[int],
    top_k: int,
    bootstrap_samples: int,
    *,
    layer: int,
    score_mode: str,
    reference_run: CellRun | None = None,
    methods: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Run vector fusion after forcing all variants to one layer and score mode."""
    variants = []
    seen = set()
    for cell in selected:
        if cell.variant not in seen:
            variants.append(cell)
            seen.add(cell.variant)
    uniform_cells = [CellConfig(cell.variant, layer, score_mode, cell.family) for cell in variants]
    if len(uniform_cells) < 2:
        return []

    reprs = build_vector_representations(dump_dir, manifest, records, uniform_cells)
    rows = []
    suffix = f"uniform_l{layer}_{score_mode.replace('anti_pca_', '').replace('_k', 'k')}"
    for k in k_values:
        if len(uniform_cells) < k:
            continue
        for combo in itertools.combinations(uniform_cells, k):
            combo_reprs = [reprs[cell.label] for cell in combo]
            for base_method in methods or [
                "vector_average_component_norm",
                "vector_average_norm_weighted",
                "vertical_concat_component_norm",
                "vertical_concat_norm_weighted",
                "maxsim_sum",
                "row_aligned_unweighted_selected_layers",
                "row_aligned_weighted_selected_layers",
            ]:
                predictions = predictions_from_vector_fusion(
                    records,
                    buckets,
                    combo_reprs,
                    method=base_method,
                    top_k=top_k,
                )
                metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
                row = {
                    "method": f"{base_method}_{suffix}",
                    "k": k,
                    "cells": [cell_to_json(cell) for cell in combo],
                    "representation_notes": [reprs[cell.label].representation_note for cell in combo],
                    "metrics": metrics,
                    "session_metrics": offline.session_retrieval_metrics(predictions),
                    "rank_metrics": offline.rank_metrics(predictions),
                }
                row["summary"] = summarize_metrics(row["metrics"], row["session_metrics"], row["rank_metrics"])
                add_reference_diagnostics(row, predictions, reference_run)
                rows.append(row)
    return rows


def parse_selected_variants(value: str, available_cells: list[CellConfig]) -> list[CellConfig]:
    by_variant = {cell.variant: cell for cell in available_cells}
    variants = [item.strip() for item in value.split(",") if item.strip()]
    if not variants:
        raise ValueError("--selected-variants was provided but no variants were parsed.")
    missing = [variant for variant in variants if variant not in by_variant]
    if missing:
        raise ValueError(f"Selected variants not present in current audit cells: {missing}")
    selected = [by_variant[variant] for variant in variants]
    if len(selected) < 2:
        raise ValueError("Select at least two variants for phases 2-4.")
    return selected


def filter_methods(methods: list[str], allowed: set[str] | None) -> list[str]:
    if allowed is None:
        return methods
    return [method for method in methods if method in allowed]


def parse_int_list(value: str) -> list[int]:
    output = []
    for item in value.split(","):
        item = item.strip()
        if item:
            output.append(int(item))
    return sorted(set(output))


def select_reference_run(runs: list[CellRun], variant: str) -> CellRun | None:
    matches = [run for run in runs if run.cell.variant == variant]
    if not matches:
        return None
    return sorted(matches, key=lambda run: metric_sort_key(run.summary), reverse=True)[0]


def add_reference_diagnostics(
    row: dict[str, Any],
    predictions: list[Prediction],
    reference_run: CellRun | None,
) -> None:
    if reference_run is None:
        return
    reference_predictions = [item.prediction() for item in reference_run.items]
    row["ranking_vs_reference"] = ranking_comparison(predictions, reference_predictions, reference_run.cell)


def ranking_comparison(
    predictions: list[Prediction],
    reference_predictions: list[Prediction],
    reference_cell: CellConfig,
) -> dict[str, Any]:
    ref_by_qid = {prediction.question_id: prediction for prediction in reference_predictions}
    top1_same = []
    top3_exact = []
    top5_exact = []
    top3_jaccard = []
    top5_jaccard = []
    ref_hit5 = []
    pred_hit5 = []
    pred_only5 = []
    ref_only5 = []
    both5 = []
    neither5 = []
    for prediction in predictions:
        reference = ref_by_qid.get(prediction.question_id)
        if reference is None or not is_prediction_scored(prediction):
            continue
        pred_top3 = set(prediction.retrieved_ids[:3])
        ref_top3 = set(reference.retrieved_ids[:3])
        pred_top5 = set(prediction.retrieved_ids[:5])
        ref_top5 = set(reference.retrieved_ids[:5])
        pred_hit = prediction_hit_all(prediction, 5)
        ref_hit = prediction_hit_all(reference, 5)
        top1_same.append(float(bool(prediction.retrieved_ids and reference.retrieved_ids and prediction.retrieved_ids[0] == reference.retrieved_ids[0])))
        top3_exact.append(float(tuple(prediction.retrieved_ids[:3]) == tuple(reference.retrieved_ids[:3])))
        top5_exact.append(float(tuple(prediction.retrieved_ids[:5]) == tuple(reference.retrieved_ids[:5])))
        top3_jaccard.append(jaccard(pred_top3, ref_top3))
        top5_jaccard.append(jaccard(pred_top5, ref_top5))
        ref_hit5.append(float(ref_hit))
        pred_hit5.append(float(pred_hit))
        pred_only5.append(float(pred_hit and not ref_hit))
        ref_only5.append(float(ref_hit and not pred_hit))
        both5.append(float(pred_hit and ref_hit))
        neither5.append(float(not pred_hit and not ref_hit))
    return {
        "reference_cell": cell_to_json(reference_cell),
        "top1_same": safe_mean(top1_same),
        "top3_exact_same": safe_mean(top3_exact),
        "top5_exact_same": safe_mean(top5_exact),
        "avg_top3_jaccard": safe_mean(top3_jaccard),
        "avg_top5_jaccard": safe_mean(top5_jaccard),
        "reference_hit@5": safe_mean(ref_hit5),
        "prediction_hit@5": safe_mean(pred_hit5),
        "prediction_only_hit@5": safe_mean(pred_only5),
        "reference_only_hit@5": safe_mean(ref_only5),
        "both_hit@5": safe_mean(both5),
        "neither_hit@5": safe_mean(neither5),
        "n_scored": len(top5_jaccard),
    }


def is_prediction_scored(prediction: Prediction) -> bool:
    return (not prediction.is_abstention) and prediction.has_target and bool(prediction.gold_ids)


def prediction_hit_all(prediction: Prediction, k: int) -> bool:
    return set(prediction.gold_ids).issubset(set(prediction.retrieved_ids[:k])) if prediction.gold_ids else False


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def evaluate_cell_pair(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    candidate_cell: CellConfig,
    query_cell: CellConfig,
    top_k: int,
    bootstrap_samples: int,
) -> CellRun:
    candidate_vectors = load_cell_vectors_mlx(
        dump_dir,
        manifest,
        records,
        variant=candidate_cell.variant,
        layer=candidate_cell.layer,
        position="last",
    )
    if candidate_cell.variant == query_cell.variant and candidate_cell.layer == query_cell.layer:
        query_vectors = candidate_vectors
    else:
        query_vectors = load_cell_vectors_mlx(
            dump_dir,
            manifest,
            records,
            variant=query_cell.variant,
            layer=query_cell.layer,
            position="last",
        )
    score_fn = make_score_fn(candidate_cell.score_mode, records, candidate_vectors)
    items = scored_items_from_pair_vectors(records, candidate_vectors, query_vectors, score_fn)
    predictions = [item.prediction() for item in items]
    metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
    session = offline.session_retrieval_metrics(predictions)
    rank = offline.rank_metrics(predictions)
    return CellRun(
        cell=candidate_cell,
        items=items,
        metrics=metrics,
        session_metrics=session,
        rank_metrics=rank,
        summary=summarize_metrics(metrics, session, rank),
    )


def make_score_fn(
    score_mode: str,
    records: list[offline.Stage2Record],
    candidate_vectors: np.ndarray,
) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
    if score_mode == "centered_cosine":
        return offline.centered_cosine_scores
    if score_mode == "query_only_anti_pca_k2":
        mean, pcs = offline.global_anti_pca(records, candidate_vectors, max_components=2)
        return lambda query, candidates: offline.anti_pca_scores(
            query,
            candidates,
            mean=mean,
            pcs=pcs[:2],
            mode="query_only",
        )
    if score_mode == "anti_pca_both_k15":
        mean, pcs = offline.global_anti_pca(records, candidate_vectors, max_components=15)
        return lambda query, candidates: offline.anti_pca_scores(
            query,
            candidates,
            mean=mean,
            pcs=pcs[:15],
            mode="both",
        )
    raise ValueError(f"Unsupported score mode: {score_mode}")


def scored_items_from_pair_vectors(
    records: list[offline.Stage2Record],
    candidate_vectors: np.ndarray,
    query_vectors: np.ndarray,
    score_fn: Callable[[np.ndarray, np.ndarray], np.ndarray],
) -> list[ScoredItem]:
    buckets = offline.group_by_instance(records)
    output = []
    for instance_index, bucket in sorted(buckets.items()):
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query_record = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        if len(candidate_ids) != len(candidate_records):
            raise ValueError(f"Missing candidate_id in instance {instance_index}.")
        scores = np.asarray(
            score_fn(query_vectors[bucket.query_index], candidate_vectors[bucket.candidate_indices]),
            dtype=np.float64,
        )
        order = np.argsort(scores)[::-1]
        output.append(
            ScoredItem(
                question_id=query_record.question_id,
                instance_index=instance_index,
                candidate_ids=tuple(candidate_ids),
                scores=tuple(float(value) for value in scores),
                ranked_ids=tuple(candidate_ids[int(index)] for index in order),
                gold_ids=tuple(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
            )
        )
    return output


def pairwise_complementarity(runs: list[CellRun]) -> list[dict[str, Any]]:
    rows = []
    for left, right in itertools.combinations(runs, 2):
        left_by_qid = {item.question_id: item for item in left.items}
        right_by_qid = {item.question_id: item for item in right.items}
        jaccards = []
        only_left = []
        only_right = []
        both = []
        neither = []
        for qid, left_item in left_by_qid.items():
            right_item = right_by_qid[qid]
            if not is_scored(left_item):
                continue
            left_top = set(left_item.ranked_ids[:5])
            right_top = set(right_item.ranked_ids[:5])
            union = left_top | right_top
            jaccards.append(len(left_top & right_top) / len(union) if union else 0.0)
            left_hit = hit_all(left_item.ranked_ids, left_item.gold_ids, 5)
            right_hit = hit_all(right_item.ranked_ids, right_item.gold_ids, 5)
            only_left.append(float(left_hit and not right_hit))
            only_right.append(float(right_hit and not left_hit))
            both.append(float(left_hit and right_hit))
            neither.append(float(not left_hit and not right_hit))
        rows.append(
            {
                "left": left.cell.label,
                "right": right.cell.label,
                "left_family": left.cell.family,
                "right_family": right.cell.family,
                "avg_top5_jaccard": safe_mean(jaccards),
                "only_left_hit@5": safe_mean(only_left),
                "only_right_hit@5": safe_mean(only_right),
                "both_hit@5": safe_mean(both),
                "neither_hit@5": safe_mean(neither),
                "n_scored": len(jaccards),
            }
        )
    return rows


def select_top3_for_vector_fusion(runs: list[CellRun], pairwise: list[dict[str, Any]]) -> list[CellConfig]:
    eligible = [run for run in runs if run.cell.is_persistable]
    eligible = sorted(eligible, key=lambda run: metric_sort_key(run.summary), reverse=True)
    if not eligible:
        return []
    selected = [eligible[0]]
    while len(selected) < 3 and len(selected) < len(eligible):
        candidates = []
        selected_labels = {run.cell.label for run in selected}
        selected_families = {run.cell.family for run in selected}
        for run in eligible:
            if run.cell.label in selected_labels or run.cell.family in selected_families:
                continue
            avg_jaccard = safe_mean(pair_jaccard(run, selected_run, pairwise) for selected_run in selected)
            if avg_jaccard <= 0.80:
                candidates.append(run)
        if candidates:
            selected.append(candidates[0])
            continue
        for run in eligible:
            if run.cell.label not in selected_labels:
                selected.append(run)
                break
    return [run.cell for run in selected]


def pair_jaccard(left: CellRun, right: CellRun, pairwise: list[dict[str, Any]]) -> float:
    labels = {left.cell.label, right.cell.label}
    for row in pairwise:
        if {row["left"], row["right"]} == labels:
            return float(row["avg_top5_jaccard"])
    return 1.0


def fuse_score_runs(combo: tuple[CellRun, ...], method: str) -> list[Prediction]:
    by_qid = [{item.question_id: item for item in run.items} for run in combo]
    output = []
    for qid, base in by_qid[0].items():
        items = [mapping[qid] for mapping in by_qid]
        if method == "rrf":
            ranked = rrf_fuse([item.ranked_ids for item in items])
        elif method == "zsum":
            ranked = zsum_fuse(items)
        else:
            raise ValueError(f"Unsupported score fusion method: {method}")
        output.append(
            Prediction(
                question_id=base.question_id,
                retrieved_ids=ranked,
                gold_ids=list(base.gold_ids),
                is_abstention=base.is_abstention,
                has_target=base.has_target,
            )
        )
    return output


def rrf_fuse(rankings: list[tuple[str, ...]], k: int = 60) -> list[str]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, candidate_id in enumerate(ranking, start=1):
            scores[candidate_id] = scores.get(candidate_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)


def zsum_fuse(items: list[ScoredItem]) -> list[str]:
    fused = {candidate_id: 0.0 for candidate_id in items[0].candidate_ids}
    for item in items:
        scores = np.asarray(item.scores, dtype=np.float64)
        std = float(np.std(scores))
        zscores = np.zeros_like(scores) if std <= 1e-12 else (scores - float(np.mean(scores))) / std
        for candidate_id, score in zip(item.candidate_ids, zscores, strict=True):
            fused[candidate_id] += float(score)
    return sorted(fused, key=fused.get, reverse=True)


def build_vector_representations(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    cells: list[CellConfig],
) -> dict[str, VectorRepr]:
    output = {}
    for cell in cells:
        print(f"phase4 repr {cell.label}")
        vectors = load_cell_vectors_mlx(
            dump_dir,
            manifest,
            records,
            variant=cell.variant,
            layer=cell.layer,
            position="last",
        )
        output[cell.label] = build_persistable_repr(cell, vectors, records)
    return output


def build_persistable_repr(
    cell: CellConfig,
    vectors: np.ndarray,
    records: list[offline.Stage2Record],
) -> VectorRepr:
    if cell.score_mode == "anti_pca_both_k15":
        mean, pcs = offline.global_anti_pca(records, vectors, max_components=15)
        transformed = offline.remove_pc_projection(vectors - mean, pcs[:15])
        return VectorRepr(cell, transformed, transformed, "anti_pca_both_k15 on both candidate and query")
    if cell.score_mode == "query_only_anti_pca_k2":
        mean, pcs = offline.global_anti_pca(records, vectors, max_components=2)
        query_vectors = offline.remove_pc_projection(vectors - mean, pcs[:2])
        return VectorRepr(cell, vectors, query_vectors, "candidate raw, query anti_pca_k2")
    raise ValueError(f"{cell.label} is not persistable for Phase 4 vector fusion.")


def predictions_from_vector_fusion(
    records: list[offline.Stage2Record],
    buckets: dict[int, offline.InstanceBucket],
    reprs: list[VectorRepr],
    *,
    method: str,
    top_k: int,
) -> list[Prediction]:
    predictions = []
    for bucket in buckets.values():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query_record = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        if len(candidate_ids) != len(candidate_records):
            raise ValueError(f"Missing candidate_id in instance {query_record.instance_index}.")
        if method == "vector_average_component_norm":
            scores = score_vector_average(bucket, reprs, component_normalize=True)
        elif method == "vector_average_norm_weighted":
            scores = score_vector_average(bucket, reprs, component_normalize=False)
        elif method == "vertical_concat_component_norm":
            scores = score_vertical_concat(bucket, reprs, component_normalize=True)
        elif method == "vertical_concat_norm_weighted":
            scores = score_vertical_concat(bucket, reprs, component_normalize=False)
        elif method == "maxsim_sum":
            scores = score_maxsim(bucket, reprs, reduce="sum")
        elif method in {"row_aligned_unweighted_selected_layers", "row_aligned_unweighted_same_layer30"}:
            scores = score_row_aligned(bucket, reprs, weighted=False)
        elif method in {"row_aligned_weighted_selected_layers", "row_aligned_weighted_same_layer30"}:
            scores = score_row_aligned(bucket, reprs, weighted=True)
        else:
            raise ValueError(f"Unsupported vector fusion method: {method}")
        order = np.argsort(scores)[::-1]
        predictions.append(
            Prediction(
                question_id=query_record.question_id,
                retrieved_ids=[candidate_ids[int(index)] for index in order[:top_k]],
                gold_ids=list(bucket.gold_ids),
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
            )
        )
    return predictions


def score_vector_average(
    bucket: offline.InstanceBucket,
    reprs: list[VectorRepr],
    *,
    component_normalize: bool,
) -> np.ndarray:
    """Average K prompt vectors back into one D-dimensional vector, then cosine.

    This is the storage-friendly counterpart to concat: each memory can persist
    one averaged vector instead of K separate prompt vectors. Component
    normalization makes it an equal-weight prompt average; leaving raw norms in
    place is a diagnostic for implicit norm weighting.
    """
    query_parts = []
    candidate_parts = []
    for repr_ in reprs:
        query_part = repr_.query_vectors[bucket.query_index]
        candidate_part = repr_.candidate_vectors[bucket.candidate_indices]
        if component_normalize:
            query_part = offline.normalize(query_part)
            candidate_part = offline.normalize(candidate_part)
        query_parts.append(query_part)
        candidate_parts.append(candidate_part)
    query = np.mean(np.stack(query_parts, axis=0), axis=0)
    candidates = np.mean(np.stack(candidate_parts, axis=0), axis=0)
    return offline.normalize(candidates) @ offline.normalize(query)


def score_vertical_concat(
    bucket: offline.InstanceBucket,
    reprs: list[VectorRepr],
    *,
    component_normalize: bool,
) -> np.ndarray:
    query_parts = []
    candidate_parts = []
    for repr_ in reprs:
        query_part = repr_.query_vectors[bucket.query_index]
        candidate_part = repr_.candidate_vectors[bucket.candidate_indices]
        if component_normalize:
            query_part = offline.normalize(query_part)
            candidate_part = offline.normalize(candidate_part)
        query_parts.append(query_part)
        candidate_parts.append(candidate_part)
    query = np.concatenate(query_parts, axis=0)
    candidates = np.concatenate(
        candidate_parts,
        axis=1,
    )
    return offline.normalize(candidates) @ offline.normalize(query)


def score_maxsim(bucket: offline.InstanceBucket, reprs: list[VectorRepr], *, reduce: str) -> np.ndarray:
    per_query_prompt_scores = []
    for query_repr in reprs:
        query = offline.normalize(query_repr.query_vectors[bucket.query_index])
        per_candidate_prompt = []
        for candidate_repr in reprs:
            candidates = offline.normalize(candidate_repr.candidate_vectors[bucket.candidate_indices])
            per_candidate_prompt.append(candidates @ query)
        per_query_prompt_scores.append(np.max(np.stack(per_candidate_prompt, axis=0), axis=0))
    stacked = np.stack(per_query_prompt_scores, axis=0)
    if reduce == "sum":
        return np.sum(stacked, axis=0)
    if reduce == "mean":
        return np.mean(stacked, axis=0)
    raise ValueError(f"Unsupported maxsim reduce: {reduce}")


def score_row_aligned(bucket: offline.InstanceBucket, reprs: list[VectorRepr], *, weighted: bool) -> np.ndarray:
    """Compare D x K row profiles across prompt views.

    For each memory/query item, K prompt vectors form H in R^{D x K}. We compare
    the K-wide row profile for each hidden dimension and aggregate over D. The
    unweighted version gives every hidden dimension equal vote after row-wise
    normalization. The weighted version weights row similarity by query/candidate
    row norm product, preserving some activation-strength information.
    """
    query_profiles = np.stack(
        [repr_.query_vectors[bucket.query_index] for repr_ in reprs],
        axis=1,
    )
    candidate_profiles = np.stack(
        [repr_.candidate_vectors[bucket.candidate_indices] for repr_ in reprs],
        axis=2,
    )
    query_norms = np.linalg.norm(query_profiles, axis=1)
    candidate_norms = np.linalg.norm(candidate_profiles, axis=2)
    norm_products = candidate_norms * query_norms[None, :]
    row_dots = np.sum(candidate_profiles * query_profiles[None, :, :], axis=2)
    row_sims = row_dots / np.maximum(norm_products, 1e-12)
    if weighted:
        weights = norm_products
        return np.sum(row_sims * weights, axis=1) / np.maximum(np.sum(weights, axis=1), 1e-12)
    valid = norm_products > 1e-12
    return np.sum(np.where(valid, row_sims, 0.0), axis=1) / np.maximum(np.sum(valid, axis=1), 1)


def hit_all(ranked_ids: tuple[str, ...], gold_ids: tuple[str, ...], k: int) -> bool:
    return set(gold_ids).issubset(set(ranked_ids[:k])) if gold_ids else False


def is_scored(item: ScoredItem) -> bool:
    return (not item.is_abstention) and item.has_target and bool(item.gold_ids)


def safe_mean(values: Any) -> float:
    vals = list(values)
    return float(np.mean(vals)) if vals else float("nan")


def summarize_metrics(metrics: dict[str, Any], session: dict[str, float], rank: dict[str, Any]) -> dict[str, Any]:
    metric_values = metrics["metrics"]
    return {
        "recall_all@3": metric_values["recall_all@3"]["mean"],
        "recall_all@3_ci95": metric_values["recall_all@3"]["ci95"],
        "ndcg_any@3": metric_values["ndcg_any@3"]["mean"],
        "ndcg_any@3_ci95": metric_values["ndcg_any@3"]["ci95"],
        "recall_all@5": metric_values["recall_all@5"]["mean"],
        "recall_all@5_ci95": metric_values["recall_all@5"]["ci95"],
        "ndcg_any@5": metric_values["ndcg_any@5"]["mean"],
        "ndcg_any@5_ci95": metric_values["ndcg_any@5"]["ci95"],
        "session_hit@5": session["session_hit@5"],
        "session_recall_all@5": session["session_recall_all@5"],
        "mrr": rank["mrr"],
        "n_scored": metrics["n_scored"],
    }


def metric_sort_key(summary: dict[str, Any]) -> tuple[float, float, float]:
    return (
        float(summary["recall_all@5"]),
        float(summary["ndcg_any@5"]),
        float(summary["session_hit@5"]),
    )


def cell_to_json(cell: CellConfig) -> dict[str, Any]:
    return {
        "variant": cell.variant,
        "layer": cell.layer,
        "score_mode": cell.score_mode,
        "family": cell.family,
        "label": cell.label,
        "is_persistable": cell.is_persistable,
    }


def cell_run_to_json(run: CellRun) -> dict[str, Any]:
    return {
        "cell": cell_to_json(run.cell),
        "metrics": run.metrics,
        "session_metrics": run.session_metrics,
        "rank_metrics": run.rank_metrics,
        "summary": run.summary,
    }


def centered_future_work_notes(
    runs: list[CellRun],
    selected: list[CellConfig],
    pairwise: list[dict[str, Any]],
) -> list[str]:
    notes = []
    selected_labels = {cell.label for cell in selected}
    for run in runs:
        if run.cell.score_mode != "centered_cosine":
            continue
        jaccards = [
            row["avg_top5_jaccard"]
            for row in pairwise
            if run.cell.label in {row["left"], row["right"]}
            and ({row["left"], row["right"]} - {run.cell.label}).pop() in selected_labels
        ]
        if jaccards and min(jaccards) < 0.50:
            notes.append(
                f"{run.cell.label} shows complementarity but is excluded from Phase 4 because "
                "centered cosine's per-query candidate mean is not a persistable vector transform."
            )
    return notes


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Stage 3 prompt fusion findings",
        "",
        "This run reuses Stage 3 hidden vectors and does not rerun the model.",
        "",
        "Storage budget: one bf16 prompt vector is 8KB; K=3 is 24KB per memory, inside the 10-100KB product target.",
        "",
        f"Single-vector baselines: best R@5={payload['baselines']['best_single_r5']:.3f}; best NDCG@5={payload['baselines']['best_single_ndcg']:.3f}.",
        "",
        "## Selected Cells",
        "",
        "| rank | cell | family |",
        "|---:|---|---|",
    ]
    for index, cell in enumerate(payload["selected_cells"], start=1):
        lines.append(f"| {index} | `{cell['label']}` | {cell['family']} |")
    lines.extend(["", "## Phase 1 Audit", ""])
    lines.extend(render_summary_table([row for row in payload["phase1_audit"]["cell_results"]], key="cell"))
    lines.extend(["", "## Phase 1 Pairwise Complementarity", ""])
    lines.extend(render_pairwise_table(payload["phase1_audit"]["pairwise"]))
    if payload["phase1_audit"]["centered_future_work"]:
        lines.extend(["", "### Centered Future Work", ""])
        for note in payload["phase1_audit"]["centered_future_work"]:
            lines.append(f"- {note}")
    lines.extend(["", "## Phase 2 Asymmetric", ""])
    lines.extend(render_summary_table(payload["phase2_asymmetric"]["rows"], key="config"))
    lines.extend(["", "## Phase 3 Score Fusion", ""])
    lines.extend(render_summary_table(payload["phase3_score_fusion"]["rows"], key="method"))
    lines.extend(["", "## Phase 4 Vector Fusion", ""])
    lines.extend(render_summary_table(payload["phase4_vector_fusion"]["rows"], key="method"))
    lines.extend(["", f"Elapsed: {format_seconds(payload['elapsed_seconds'])}", ""])
    return "\n".join(lines)


def render_summary_table(rows: list[dict[str, Any]], *, key: str, limit: int = 20) -> list[str]:
    lines = [
        "| rank | config | R@3 | NDCG@3 | R@5 | NDCG@5 | session_hit@5 | MRR | ref_top5_j | pred_only@5 | ref_only@5 | n |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    sorted_rows = sorted(rows, key=lambda row: metric_sort_key(row["summary"]), reverse=True)
    for index, row in enumerate(sorted_rows[:limit], start=1):
        summary = row["summary"]
        if key == "cell":
            label = row["cell"]["label"]
        elif key == "method":
            cells = "+".join(cell["variant"] for cell in row.get("cells", []))
            label = f"{row['method']} K={row.get('k', '?')} {cells}"
        else:
            label = row.get(key, row.get("config", ""))
        ref = row.get("ranking_vs_reference", {})
        lines.append(
            f"| {index} | `{label}` | {summary['recall_all@3']:.3f} | "
            f"{summary['ndcg_any@3']:.3f} | {summary['recall_all@5']:.3f} | "
            f"{summary['ndcg_any@5']:.3f} | {summary['session_hit@5']:.3f} | "
            f"{summary['mrr']:.3f} | {format_optional_float(ref.get('avg_top5_jaccard'))} | "
            f"{format_optional_float(ref.get('prediction_only_hit@5'))} | "
            f"{format_optional_float(ref.get('reference_only_hit@5'))} | {summary['n_scored']} |"
        )
    return lines


def format_optional_float(value: Any) -> str:
    if value is None:
        return "-"
    try:
        if np.isnan(float(value)):
            return "-"
    except TypeError:
        return "-"
    return f"{float(value):.3f}"


def render_pairwise_table(rows: list[dict[str, Any]], limit: int = 30) -> list[str]:
    lines = [
        "| pair | top5_jaccard | only_left_hit@5 | only_right_hit@5 | both_hit@5 |",
        "|---|---:|---:|---:|---:|",
    ]
    sorted_rows = sorted(rows, key=lambda row: (row["avg_top5_jaccard"], -row["both_hit@5"]))
    for row in sorted_rows[:limit]:
        pair = f"{row['left']} vs {row['right']}"
        lines.append(
            f"| `{pair}` | {row['avg_top5_jaccard']:.3f} | "
            f"{row['only_left_hit@5']:.3f} | {row['only_right_hit@5']:.3f} | {row['both_hit@5']:.3f} |"
        )
    return lines


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
