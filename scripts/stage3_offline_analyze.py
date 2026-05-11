"""Stage 3 offline prompt-sweep leaderboard over the merged vector store.

This script evaluates saved Stage 3 prompt vectors without rerunning the model.
It is intentionally hidden-only: BM25 score fusion is excluded because this
stage is about prompt geometry for chatbot memory, not lexical reranking.

The first-pass experiment is deliberately simple:

- sweep every symmetric `(prompt_variant, layer, last)` cell;
- add the asymmetric memory/query cell where `2-3-2_mem` encodes candidates and
  `2-3-2_query` encodes queries;
- report centered cosine, query-only anti-PCA k=2, and anti-PCA-both k=15.

Multi-vector prompt fusion / late interaction is future work. Stage 3 already
stores the raw 17-variant tensor grid needed for that experiment; this script
keeps the first leaderboard interpretable before combining prompts.

The implementation streams one cell at a time. A full 17x3 load would materialize
many gigabytes of fp32 vectors, while one cell is about 0.38 GiB before PCA
workspace. This respects the 16GB Mac operating budget and allows a quick smoke
run via `--limit-cells 1 --bootstrap-samples 100`.
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


DEFAULT_DUMP_DIR = ROOT / "tensors" / "stage3" / "prompt_sweep" / "merged_subset0-100_cache2gb_logits256"
DEFAULT_DATA = ROOT / "data" / "longmemeval_s_cleaned.json"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "offline_prompt_sweep"
DEFAULT_OUTPUT_PREFIX = "merged_subset0-100_hidden_only"
DEFAULT_LAYERS = "29,30,31"
DEFAULT_POSITION = "last"
ASYM_CANDIDATE_VARIANT = "2-3-2_mem"
ASYM_QUERY_VARIANT = "2-3-2_query"


@dataclass(frozen=True)
class CellSpec:
    candidate_variant: str
    query_variant: str
    layer: int
    position: str
    cell_type: str

    @property
    def label(self) -> str:
        if self.cell_type == "asymmetric":
            return f"{self.candidate_variant}->{self.query_variant}|layer{self.layer}|{self.position}"
        return f"{self.candidate_variant}|layer{self.layer}|{self.position}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--variants", default="all")
    parser.add_argument("--layers", default=DEFAULT_LAYERS)
    parser.add_argument("--position", default=DEFAULT_POSITION)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--limit-cells", type=int, default=None)
    parser.add_argument("--no-asymmetric", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()

    dump_dir = Path(args.dump_dir)
    manifest = offline.load_manifest(dump_dir)
    offline.validate_manifest(manifest)
    records = offline.load_records(dump_dir, manifest, Path(args.data))

    variants = parse_variants(args.variants, manifest["prompt_variants"])
    layers = parse_layers(args.layers, manifest["layers"])
    cells = build_cells(
        variants=variants,
        layers=layers,
        position=args.position,
        manifest_variants=manifest["prompt_variants"],
        include_asymmetric=not args.no_asymmetric,
    )
    if args.limit_cells is not None:
        cells = cells[: args.limit_cells]
    if not cells:
        raise ValueError("No Stage 3 cells selected.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in [json_path, md_path] if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    print(f"records={len(records)} cells={len(cells)} bootstrap={args.bootstrap_samples}")
    cell_results: list[dict[str, Any]] = []
    for index, cell in enumerate(cells, start=1):
        cell_start = time.perf_counter()
        print(f"[{index}/{len(cells)}] {cell.label}")
        try:
            cell_results.extend(
                evaluate_cell(
                    dump_dir=dump_dir,
                    manifest=manifest,
                    records=records,
                    cell=cell,
                    top_k=args.top_k,
                    bootstrap_samples=args.bootstrap_samples,
                )
            )
        except ValueError as exc:
            if "No predictions left after official LongMemEval filtering" in str(exc):
                raise ValueError(
                    f"{cell.label}: no scored predictions after LongMemEval filtering. "
                    "Check the data subset, manifest rows, and abstention/no-target filtering."
                ) from exc
            raise
        elapsed = time.perf_counter() - cell_start
        print(f"  done in {format_seconds(elapsed)}")
        gc.collect()

    top_configs = sorted(
        [summarize_result(result) for result in cell_results],
        key=lambda row: (
            row["recall_all@5"],
            row["ndcg_any@5"],
            row["session_hit@5"],
        ),
        reverse=True,
    )
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "stage3_offline_prompt_sweep_hidden_only",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "variants": variants,
            "layers": layers,
            "position": args.position,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "limit_cells": args.limit_cells,
        },
        "design_notes": [
            "Hidden-only first pass; BM25 fusion is intentionally excluded.",
            "Asymmetric 2-3-2_mem -> 2-3-2_query tests store-vs-retrieve prompt semantics.",
            "Prompt-vector fusion and late interaction are future experiments over the same raw store.",
            "Cells are streamed one at a time to stay within the 16GB Mac memory budget.",
        ],
        "cell_results": cell_results,
        "top_configs": top_configs,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(f"elapsed {format_seconds(payload['elapsed_seconds'])}")
    return 0


def parse_variants(value: str, manifest_variants: list[str]) -> list[str]:
    if value == "all":
        return list(manifest_variants)
    variants = [item.strip() for item in value.split(",") if item.strip()]
    missing = [variant for variant in variants if variant not in manifest_variants]
    if missing:
        raise ValueError(f"Unknown variants {missing}; manifest has {manifest_variants}")
    return variants


def parse_layers(value: str, manifest_layers: list[int]) -> list[int]:
    if value == "all":
        return [int(layer) for layer in manifest_layers]
    layers = [int(item.strip()) for item in value.split(",") if item.strip()]
    missing = [layer for layer in layers if layer not in manifest_layers]
    if missing:
        raise ValueError(f"Unknown layers {missing}; manifest has {manifest_layers}")
    return layers


def build_cells(
    *,
    variants: list[str],
    layers: list[int],
    position: str,
    manifest_variants: list[str],
    include_asymmetric: bool,
) -> list[CellSpec]:
    cells = [
        CellSpec(
            candidate_variant=variant,
            query_variant=variant,
            layer=layer,
            position=position,
            cell_type="symmetric",
        )
        for variant in variants
        for layer in layers
    ]
    if include_asymmetric:
        for variant in [ASYM_CANDIDATE_VARIANT, ASYM_QUERY_VARIANT]:
            if variant not in manifest_variants:
                raise ValueError(f"Asymmetric variant {variant!r} missing from manifest.")
        cells.extend(
            CellSpec(
                candidate_variant=ASYM_CANDIDATE_VARIANT,
                query_variant=ASYM_QUERY_VARIANT,
                layer=layer,
                position=position,
                cell_type="asymmetric",
            )
            for layer in layers
        )
    return cells


def load_cell_vectors_mlx(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    *,
    variant: str,
    layer: int,
    position: str,
) -> np.ndarray:
    """Load one `(variant, layer, position)` cell with chunk-batched MLX reads.

    The legacy Stage 2 helper slices one safetensors row at a time. On the Stage
    3 merged store that means 24,796 Python/safetensors calls per cell, which
    the smoke timing showed as 180s of load time and about 5GB peak memory.

    This loader follows the Stage 1 analyzer pattern instead: `mx.load` one
    chunk, take `states[:, variant, layer, position, :]` once, evaluate the MLX
    slice, convert that compact slice to fp32 NumPy, and batch-assign all rows
    for the chunk. The transient full chunk is about 100MB, while the persistent
    output matrix is about 406MB for 24,796 x 4096 fp32 rows. With PCA and
    NumPy workspace, expected single-cell peak after this change is roughly
    2-3GB, below the 8GB target and 10GB hard limit, provided embedding eval is
    not running.

    We intentionally do not reuse the PCA-centered matrix for centered cosine:
    centered cosine uses a per-query candidate-subset mean, while anti-PCA uses
    the global candidate-corpus mean. Reusing one for the other would change the
    experiment definition and make the smoke metrics incomparable.
    """
    import mlx.core as mx

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

        tensors = mx.load(str(path))
        states = tensors["states"]
        cell_tensor = states[:, variant_index, layer_index, position_index, :].astype(mx.float32)
        mx.eval(cell_tensor)
        cell_vectors = np.array(cell_tensor).astype(np.float32, copy=False)

        output_rows = np.fromiter((row_index for row_index, _record in rows), dtype=np.int64)
        chunk_rows = np.fromiter((record.chunk_index for _row_index, record in rows), dtype=np.int64)
        output[output_rows] = cell_vectors[chunk_rows]

        del tensors, states, cell_tensor, cell_vectors, output_rows, chunk_rows
        clear_mlx_cache(mx)

    if not np.all(np.isfinite(output)):
        raise ValueError(f"Non-finite vector in {variant}|layer{layer}|{position}.")
    return output


def clear_mlx_cache(mx_module: Any) -> None:
    """Best-effort MLX cache release after each chunk.

    Chunk-batched loading is fast, but we still avoid retaining the MLX reusable
    allocation cache across 100 chunks because this repo targets a 16GB Mac.
    MLX has used both `mx.clear_cache()` and `mx.metal.clear_cache()` across
    versions, so this helper supports either without making cache release fatal.
    """
    clear_cache = getattr(mx_module, "clear_cache", None)
    if callable(clear_cache):
        clear_cache()
        return
    metal = getattr(mx_module, "metal", None)
    clear_cache = getattr(metal, "clear_cache", None)
    if callable(clear_cache):
        clear_cache()


def evaluate_cell(
    *,
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    cell: CellSpec,
    top_k: int,
    bootstrap_samples: int,
) -> list[dict[str, Any]]:
    # Measure before optimizing: the first smoke run was slow, but phase
    # timings tell us whether to batch vector loading, GPU-accelerate math, or
    # trim bootstrap. Keep this local to Stage 3 so Stage 2 paths stay stable.
    cell_started = time.perf_counter()
    timings: dict[str, float] = {}

    phase_started = time.perf_counter()
    candidate_vectors = load_cell_vectors_mlx(
        dump_dir,
        manifest,
        records,
        variant=cell.candidate_variant,
        layer=cell.layer,
        position=cell.position,
    )
    timings["load_candidate_vectors"] = time.perf_counter() - phase_started

    if cell.query_variant == cell.candidate_variant:
        query_vectors = candidate_vectors
        timings["load_query_vectors"] = 0.0
    else:
        phase_started = time.perf_counter()
        query_vectors = load_cell_vectors_mlx(
            dump_dir,
            manifest,
            records,
            variant=cell.query_variant,
            layer=cell.layer,
            position=cell.position,
        )
        timings["load_query_vectors"] = time.perf_counter() - phase_started

    phase_started = time.perf_counter()
    mean, pcs = offline.global_anti_pca(records, candidate_vectors, max_components=15)
    timings["pca_fit"] = time.perf_counter() - phase_started

    score_modes: list[tuple[str, Callable[[np.ndarray, np.ndarray], np.ndarray]]] = [
        ("centered_cosine", offline.centered_cosine_scores),
        (
            "query_only_anti_pca_k2",
            lambda query, candidates: offline.anti_pca_scores(
                query,
                candidates,
                mean=mean,
                pcs=pcs[:2],
                mode="query_only",
            ),
        ),
        (
            "anti_pca_both_k15",
            lambda query, candidates: offline.anti_pca_scores(
                query,
                candidates,
                mean=mean,
                pcs=pcs[:15],
                mode="both",
            ),
        ),
    ]

    short_names = {
        "centered_cosine": "centered",
        "query_only_anti_pca_k2": "qpca",
        "anti_pca_both_k15": "apca",
    }
    results = []
    for score_mode, score_fn in score_modes:
        short_name = short_names[score_mode]
        phase_started = time.perf_counter()
        predictions = predictions_from_pair_vectors(
            records,
            candidate_vectors=candidate_vectors,
            query_vectors=query_vectors,
            top_k=top_k,
            score_fn=score_fn,
        )
        timings[f"score_{short_name}"] = time.perf_counter() - phase_started

        phase_started = time.perf_counter()
        turn_metrics = evaluate(
            predictions,
            skip_abstention=True,
            bootstrap_samples=bootstrap_samples,
            ks=(1, 3, 5, 10, 20, 30, 50),
        )
        session_metrics = offline.session_retrieval_metrics(predictions)
        rank_metrics = offline.rank_metrics(predictions)
        timings[f"eval_{short_name}"] = time.perf_counter() - phase_started
        results.append(
            {
                "cell": cell_to_dict(cell),
                "config": f"{cell.label}|{score_mode}",
                "score_mode": score_mode,
                "turn_metrics": turn_metrics,
                "session_metrics": session_metrics,
                "rank_metrics": rank_metrics,
            }
        )
    timings["total"] = time.perf_counter() - cell_started
    for result in results:
        result["phase_timings_s"] = dict(timings)
    print(
        f"timing {cell.label}: "
        f"load={timings['load_candidate_vectors'] + timings['load_query_vectors']:.1f}s "
        f"pca={timings['pca_fit']:.1f}s "
        f"score_centered={timings['score_centered']:.1f}s "
        f"eval_centered={timings['eval_centered']:.1f}s "
        f"score_qpca={timings['score_qpca']:.1f}s "
        f"eval_qpca={timings['eval_qpca']:.1f}s "
        f"score_apca={timings['score_apca']:.1f}s "
        f"eval_apca={timings['eval_apca']:.1f}s "
        f"total={timings['total']:.1f}s"
    )
    return results


def predictions_from_pair_vectors(
    records: list[offline.Stage2Record],
    *,
    candidate_vectors: np.ndarray,
    query_vectors: np.ndarray,
    top_k: int,
    score_fn: Callable[[np.ndarray, np.ndarray], np.ndarray],
) -> list[Prediction]:
    buckets = offline.group_by_instance(records)
    output = []
    for bucket in buckets.values():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query_record = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        if len(candidate_ids) != len(candidate_records):
            raise ValueError(f"Missing candidate_id in instance {query_record.instance_index}.")
        scores = np.asarray(
            score_fn(
                query_vectors[bucket.query_index],
                candidate_vectors[bucket.candidate_indices],
            ),
            dtype=np.float64,
        )
        if scores.shape != (len(candidate_records),):
            raise ValueError(f"score_fn returned {scores.shape}, expected {(len(candidate_records),)}")
        order = np.argsort(scores)[::-1][:top_k]
        output.append(
            Prediction(
                question_id=query_record.question_id,
                retrieved_ids=[candidate_ids[int(index)] for index in order],
                gold_ids=bucket.gold_ids,
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
            )
        )
    return output


def summarize_result(result: dict[str, Any]) -> dict[str, Any]:
    metrics = result["turn_metrics"]["metrics"]
    recall5 = metrics["recall_all@5"]
    ndcg5 = metrics["ndcg_any@5"]
    session = result["session_metrics"]
    cell = result["cell"]
    return {
        "config": result["config"],
        "cell_type": cell["cell_type"],
        "candidate_variant": cell["candidate_variant"],
        "query_variant": cell["query_variant"],
        "layer": cell["layer"],
        "position": cell["position"],
        "score_mode": result["score_mode"],
        "recall_all@5": recall5["mean"],
        "recall_all@5_ci95": recall5["ci95"],
        "ndcg_any@5": ndcg5["mean"],
        "ndcg_any@5_ci95": ndcg5["ci95"],
        "session_hit@5": session["session_hit@5"],
        "session_recall_all@5": session["session_recall_all@5"],
        "mrr": result["rank_metrics"]["mrr"],
        "n_scored": result["turn_metrics"]["n_scored"],
    }


def cell_to_dict(cell: CellSpec) -> dict[str, Any]:
    return {
        "candidate_variant": cell.candidate_variant,
        "query_variant": cell.query_variant,
        "layer": cell.layer,
        "position": cell.position,
        "cell_type": cell.cell_type,
        "label": cell.label,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    rows = payload["top_configs"]
    lines = [
        "# Stage 3 offline prompt sweep: hidden-only",
        "",
        "This analysis reads the merged Stage 3 prompt-sweep vectors and does not rerun the model.",
        "",
        "LongMemEval is evidence-retrieval biased. In a chatbot-memory product, persona, preference, style, or strategy prompts may still be useful even when this leaderboard ranks them below fact/topic prompts.",
        "",
        "BM25 score fusion is intentionally excluded here; prompt-vector fusion and late interaction are future experiments over the same stored vectors.",
        "",
        "## Top Configs",
        "",
        "| rank | config | R@5 | NDCG@5 | session_hit@5 | MRR | n |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(rows[:25], start=1):
        lines.append(
            f"| {rank} | `{row['config']}` | {row['recall_all@5']:.3f} "
            f"| {row['ndcg_any@5']:.3f} | {row['session_hit@5']:.3f} "
            f"| {row['mrr']:.3f} | {row['n_scored']} |"
        )
    lines.extend(["", "## Query-Only Anti-PCA k=2", "", *render_mode_table(rows, "query_only_anti_pca_k2")])
    lines.extend(["", "## Anti-PCA Both k=15", "", *render_mode_table(rows, "anti_pca_both_k15")])
    lines.extend(
        [
            "",
            "## Asymmetric Memory/Query Cell",
            "",
            "Anti-PCA for the asymmetric cell fits the mean and PCs on `2-3-2_mem` candidate rows, then applies that candidate-side geometry to `2-3-2_query` query rows. If this cell is weak, inspect that cross-prompt centering mismatch before treating the prompt idea as failed.",
            "",
            *render_asymmetric_table(rows),
        ]
    )
    lines.extend(["", f"Elapsed: {format_seconds(payload['elapsed_seconds'])}", ""])
    return "\n".join(lines)


def render_mode_table(rows: list[dict[str, Any]], score_mode: str) -> list[str]:
    selected = [row for row in rows if row["score_mode"] == score_mode]
    lines = [
        "| rank | candidate prompt | query prompt | layer | R@5 | NDCG@5 | session_hit@5 |",
        "|---:|---|---|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(selected[:15], start=1):
        lines.append(
            f"| {rank} | `{row['candidate_variant']}` | `{row['query_variant']}` | "
            f"{row['layer']} | {row['recall_all@5']:.3f} | {row['ndcg_any@5']:.3f} "
            f"| {row['session_hit@5']:.3f} |"
        )
    return lines


def render_asymmetric_table(rows: list[dict[str, Any]]) -> list[str]:
    selected = [row for row in rows if row["cell_type"] == "asymmetric"]
    lines = [
        "| score | layer | R@5 | NDCG@5 | session_hit@5 |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in selected:
        lines.append(
            f"| `{row['score_mode']}` | {row['layer']} | {row['recall_all@5']:.3f} "
            f"| {row['ndcg_any@5']:.3f} | {row['session_hit@5']:.3f} |"
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
