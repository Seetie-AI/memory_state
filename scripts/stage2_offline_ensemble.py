"""Hidden-only ensemble experiments on the 9B Stage 2 vector dump.

Design decisions agreed in multi-agent planning:
  1. N=100 evaluation only (94 scored). N=30 was retired for confirmation due
     to a 0.24 R@5 swing between 30-subset and 100-subset on the identical 2B
     P0|layer22|last|centered config (0.833 vs 0.596). N=30 can eliminate bad
     directions, but it cannot confirm improvements.
  2. RRF (Reciprocal Rank Fusion, k=60) over rank, not linear-alpha over score.
     This avoids score-scale calibration issues across different anti-PCA k,
     layer, and position configurations.
  3. For multi-vector (ColBERT-style max-sim) experiments, anti-PCA is applied
     per position independently, not jointly. Reason: last/minus2/content_end
     have different hidden distributions; joint PCA would let last-token
     dominant directions contaminate other positions.
  4. Strictly hidden-only: no BM25, no Qwen-Embedding. BM25 fusion stays as an
     ablation in the existing offline pipeline, not in this script.
  5. Statistical significance: 95% bootstrap CI (n=1000 resamples) on every
     R@5 / NDCG@5. Improvements smaller than +0.05 over the hidden-only
     baseline are treated as noise on n=94, not real signal.
  6. Headline hidden-only baseline to beat:
     P0|layer30|last|anti_pca_both_k15 -> R@5 = 0.755, NDCG@5 = 0.779.

The script reads saved compact vectors from tensors/stage2/9b_4bit_100_p0 and
does not run the model or create new tensor stores. It materializes one
(variant, layer, position) slice at a time for rank-fusion experiments; the
only experiment that holds multiple slices concurrently is multi-vector scoring
(five normalized position matrices, roughly 2GB for the 9B 100-subset dump).
"""

from __future__ import annotations

import argparse
import json
import sys
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

from eval.longmemeval_metrics import (  # noqa: E402
    Prediction,
    evaluate,
    ndcg_any_at_k,
    recall_all_at_k,
)
import stage2_offline_analyze as offline  # noqa: E402


DEFAULT_DUMP_DIR = ROOT / "tensors" / "stage2" / "9b_4bit_100_p0"
DEFAULT_DATA = ROOT / "data" / "longmemeval_s_cleaned.json"
DEFAULT_VARIANT = "P0"
DEFAULT_TOP_K = 50
DEFAULT_BOOTSTRAP_SAMPLES = 1000
RRF_K = 60
BASELINE_NAME = "P0|layer30|last|anti_pca_both_k15"
SIGNAL_THRESHOLD = 0.05

K_VALUES = [5, 10, 15, 20]
LAYER_VALUES = [28, 29, 30, 31]
POSITION_VALUES = ["last", "minus2", "minus3", "suffix_start", "content_end"]


@dataclass(frozen=True)
class Ranking:
    question_id: str
    instance_index: int
    ranked_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--variant", default=DEFAULT_VARIANT)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--bootstrap-samples", type=int, default=DEFAULT_BOOTSTRAP_SAMPLES)
    parser.add_argument("--rrf-k", type=int, default=RRF_K)
    parser.add_argument(
        "--experiments",
        default="all",
        help=(
            "Comma-separated list from k_rrf,layer_rrf,position_rrf,k_layer_rrf,"
            "k_position_rrf,multivector,multivector_antipca, or all."
        ),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output-prefix", default="offline_hidden_ensemble")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected = parse_experiments(args.experiments)
    dump_dir = Path(args.dump_dir)
    manifest = offline.load_manifest(dump_dir)
    offline.validate_manifest(manifest)
    validate_manifest_values(manifest, args.variant)

    if args.dry_run:
        print_plan(manifest, selected, dump_dir)
        return 0

    records = offline.load_records(dump_dir, manifest, Path(args.data))
    baseline = anti_pca_rankings(
        dump_dir,
        manifest,
        records,
        variant=args.variant,
        layer=30,
        position="last",
        components=[15],
    )[15]
    baseline_predictions = predictions_from_rankings(baseline, args.top_k)
    baseline_metrics = evaluate(
        baseline_predictions,
        skip_abstention=True,
        bootstrap_samples=args.bootstrap_samples,
    )

    configs: dict[str, dict[str, Any]] = {
        BASELINE_NAME: {
            "kind": "baseline",
            "judges": [BASELINE_NAME],
            "metrics": baseline_metrics,
            "paired_delta_vs_baseline": paired_delta(
                baseline_predictions,
                baseline_predictions,
                bootstrap_samples=args.bootstrap_samples,
            ),
            "interpretation": "baseline",
        }
    }

    if "k_rrf" in selected:
        rankings_by_k = anti_pca_rankings(
            dump_dir,
            manifest,
            records,
            variant=args.variant,
            layer=30,
            position="last",
            components=K_VALUES,
        )
        add_rrf_config(
            configs,
            "hidden_only_rrf_k_5_10_15_20_layer30_last",
            [f"{args.variant}|layer30|last|anti_pca_both_k{k}" for k in K_VALUES],
            [rankings_by_k[k] for k in K_VALUES],
            baseline_predictions,
            args,
        )

    if "layer_rrf" in selected:
        layer_rankings = []
        layer_names = []
        for layer in LAYER_VALUES:
            rankings = anti_pca_rankings(
                dump_dir,
                manifest,
                records,
                variant=args.variant,
                layer=layer,
                position="last",
                components=[15],
            )[15]
            layer_rankings.append(rankings)
            layer_names.append(f"{args.variant}|layer{layer}|last|anti_pca_both_k15")
        add_rrf_config(
            configs,
            "hidden_only_rrf_layers_28_29_30_31_k15_last",
            layer_names,
            layer_rankings,
            baseline_predictions,
            args,
        )

    if "position_rrf" in selected:
        position_rankings = []
        position_names = []
        for position in POSITION_VALUES:
            rankings = anti_pca_rankings(
                dump_dir,
                manifest,
                records,
                variant=args.variant,
                layer=30,
                position=position,
                components=[15],
            )[15]
            position_rankings.append(rankings)
            position_names.append(f"{args.variant}|layer30|{position}|anti_pca_both_k15")
        add_rrf_config(
            configs,
            "hidden_only_rrf_positions_layer30_k15",
            position_names,
            position_rankings,
            baseline_predictions,
            args,
        )

    if "k_layer_rrf" in selected:
        rankings_list = []
        names = []
        for layer in LAYER_VALUES:
            by_k = anti_pca_rankings(
                dump_dir,
                manifest,
                records,
                variant=args.variant,
                layer=layer,
                position="last",
                components=K_VALUES,
            )
            for k in K_VALUES:
                rankings_list.append(by_k[k])
                names.append(f"{args.variant}|layer{layer}|last|anti_pca_both_k{k}")
        add_rrf_config(
            configs,
            "hidden_only_rrf_layers_28_31_x_k_5_20_last",
            names,
            rankings_list,
            baseline_predictions,
            args,
        )

    if "k_position_rrf" in selected:
        rankings_list = []
        names = []
        for position in POSITION_VALUES:
            by_k = anti_pca_rankings(
                dump_dir,
                manifest,
                records,
                variant=args.variant,
                layer=30,
                position=position,
                components=K_VALUES,
            )
            for k in K_VALUES:
                rankings_list.append(by_k[k])
                names.append(f"{args.variant}|layer30|{position}|anti_pca_both_k{k}")
        add_rrf_config(
            configs,
            "hidden_only_rrf_positions_x_k_layer30",
            names,
            rankings_list,
            baseline_predictions,
            args,
        )

    if "multivector" in selected:
        rankings = multivector_rankings(
            dump_dir,
            manifest,
            records,
            variant=args.variant,
            layer=30,
            positions=POSITION_VALUES,
            anti_pca_components=None,
        )
        add_single_config(
            configs,
            "hidden_only_multivector_layer30_positions_raw",
            [f"{args.variant}|layer30|{position}|raw" for position in POSITION_VALUES],
            rankings,
            baseline_predictions,
            args,
        )

    if "multivector_antipca" in selected:
        rankings = multivector_rankings(
            dump_dir,
            manifest,
            records,
            variant=args.variant,
            layer=30,
            positions=POSITION_VALUES,
            anti_pca_components=15,
        )
        add_single_config(
            configs,
            "hidden_only_multivector_layer30_positions_per_position_antipca_k15",
            [f"{args.variant}|layer30|{position}|anti_pca_both_k15" for position in POSITION_VALUES],
            rankings,
            baseline_predictions,
            args,
        )

    result = {
        "analysis": "offline_hidden_ensemble",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "dump_dir": str(dump_dir),
        "data": str(Path(args.data)),
        "design_decisions": design_decisions(),
        "experiments_requested": selected,
        "baseline_config": BASELINE_NAME,
        "signal_threshold_r5": SIGNAL_THRESHOLD,
        "configs": configs,
        "top_configs": top_metric_rows(configs),
    }
    write_outputs(result, args.output_prefix)
    return 0


def parse_experiments(spec: str) -> list[str]:
    all_names = [
        "k_rrf",
        "layer_rrf",
        "position_rrf",
        "k_layer_rrf",
        "k_position_rrf",
        "multivector",
        "multivector_antipca",
    ]
    if spec.strip() == "all":
        return all_names
    selected = [part.strip() for part in spec.split(",") if part.strip()]
    invalid = [name for name in selected if name not in all_names]
    if invalid:
        raise ValueError(f"Unknown experiments {invalid}; choose from {all_names}")
    return selected


def validate_manifest_values(manifest: dict[str, Any], variant: str) -> None:
    missing_layers = [layer for layer in LAYER_VALUES + [30] if layer not in manifest["layers"]]
    missing_positions = [position for position in POSITION_VALUES if position not in manifest["positions"]]
    if variant not in manifest["prompt_variants"]:
        raise ValueError(f"Variant {variant!r} not present in manifest: {manifest['prompt_variants']}")
    if missing_layers:
        raise ValueError(f"Missing required layers in manifest: {missing_layers}")
    if missing_positions:
        raise ValueError(f"Missing required positions in manifest: {missing_positions}")


def print_plan(manifest: dict[str, Any], selected: list[str], dump_dir: Path) -> None:
    rows = int(sum(int(chunk["row_count"]) for chunk in manifest["chunks"]))
    hidden_dim = int(manifest["hidden_dim"])
    slice_gb = rows * hidden_dim * 4 / 1024**3
    print("offline hidden-only ensemble dry run")
    print(f"dump_dir: {dump_dir}")
    print(f"rows: {rows}")
    print(f"layers available: {manifest['layers']}")
    print(f"positions available: {manifest['positions']}")
    print(f"variants available: {manifest['prompt_variants']}")
    print(f"one fp32 slice estimate: {slice_gb:.2f} GiB")
    print(f"selected experiments: {', '.join(selected)}")
    print("no model execution; output is results/offline_hidden_ensemble_<timestamp>.json/.md")


def design_decisions() -> list[str]:
    return [
        "N=100 evaluation only; N=30 is for elimination, not confirmation.",
        "RRF over rank with k=60; no score-linear fusion.",
        "Multi-vector anti-PCA is per-position independent.",
        "Strict hidden-only: no BM25 and no external embedding model.",
        "Bootstrap 95% CI is reported; R@5 deltas below +0.05 are treated as noise.",
    ]


def anti_pca_rankings(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    *,
    variant: str,
    layer: int,
    position: str,
    components: list[int],
) -> dict[int, list[Ranking]]:
    print(f"loading {variant}|layer{layer}|{position} for anti-PCA k={components}")
    vectors = load_vector_matrix(
        dump_dir,
        manifest,
        records,
        variant=variant,
        layer=layer,
        position=position,
    )
    max_components = max(components)
    mean, pcs = offline.global_anti_pca(records, vectors, max_components=max_components)
    output = {}
    for k in components:
        name = f"{variant}|layer{layer}|{position}|anti_pca_both_k{k}"
        print(f"ranking {name}")
        output[k] = rankings_from_vectors(
            records,
            vectors,
            score_fn=lambda query, candidates, k=k: offline.anti_pca_scores(
                query,
                candidates,
                mean=mean,
                pcs=pcs[:k],
                mode="both",
            ),
        )
    return output


def rankings_from_vectors(
    records: list[offline.Stage2Record],
    vectors: np.ndarray,
    *,
    score_fn: Any,
) -> list[Ranking]:
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
            score_fn(vectors[bucket.query_index], vectors[bucket.candidate_indices]),
            dtype=np.float64,
        )
        order = np.argsort(scores)[::-1]
        output.append(
            Ranking(
                question_id=query_record.question_id,
                instance_index=instance_index,
                ranked_ids=[candidate_ids[int(index)] for index in order],
                gold_ids=bucket.gold_ids,
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
            )
        )
    return output


def load_vector_matrix(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    *,
    variant: str,
    layer: int,
    position: str,
) -> np.ndarray:
    """Load one vector slice with a CPU-safe bf16 fallback.

    The older offline analyzer falls back to MLX when safetensors' NumPy path
    cannot expose bf16 rows. This sandbox has no Metal device, so this script
    keeps the fallback local and uses safetensors' PyTorch CPU path instead.
    It still loads one row slice at a time and never materializes unrelated
    layers/positions from the vector store.
    """
    variant_index = index_of(manifest["prompt_variants"], variant, "variant")
    layer_index = index_of(manifest["layers"], layer, "layer")
    position_index = index_of(manifest["positions"], position, "position")
    hidden_dim = int(manifest["hidden_dim"])
    output = np.empty((len(records), hidden_dim), dtype=np.float32)

    records_by_chunk: dict[str, list[tuple[int, offline.Stage2Record]]] = {}
    for row_index, record in enumerate(records):
        records_by_chunk.setdefault(record.chunk_file, []).append((row_index, record))

    for chunk_file, rows in sorted(records_by_chunk.items()):
        path = dump_dir / chunk_file
        try:
            from safetensors import safe_open

            with safe_open(str(path), framework="np") as handle:
                tensor_slice = handle.get_slice("states")
                for row_index, record in rows:
                    output[row_index] = np.asarray(
                        tensor_slice[
                            record.chunk_index,
                            variant_index,
                            layer_index,
                            position_index,
                            :,
                        ],
                        dtype=np.float32,
                    )
        except (TypeError, ValueError):
            import torch
            from safetensors import safe_open

            with safe_open(str(path), framework="pt", device="cpu") as handle:
                tensor_slice = handle.get_slice("states")
                for row_index, record in rows:
                    output[row_index] = (
                        tensor_slice[
                            record.chunk_index,
                            variant_index,
                            layer_index,
                            position_index,
                            :,
                        ]
                        .to(dtype=torch.float32)
                        .numpy()
                    )
        except Exception as exc:
            raise RuntimeError(f"Failed to load vector slice from {path}") from exc
    if not np.all(np.isfinite(output)):
        raise ValueError(f"Non-finite vector in {variant}|layer{layer}|{position}.")
    return output


def index_of(values: list[Any], target: Any, name: str) -> int:
    if target not in values:
        raise ValueError(f"{name} {target!r} not present in manifest values {values!r}")
    return int(values.index(target))


def multivector_rankings(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[offline.Stage2Record],
    *,
    variant: str,
    layer: int,
    positions: list[str],
    anti_pca_components: int | None,
) -> list[Ranking]:
    matrices = []
    for position in positions:
        print(
            f"loading {variant}|layer{layer}|{position} "
            f"for multivector anti_pca={anti_pca_components}"
        )
        matrix = load_vector_matrix(
            dump_dir,
            manifest,
            records,
            variant=variant,
            layer=layer,
            position=position,
        )
        if anti_pca_components is not None:
            mean, pcs = offline.global_anti_pca(records, matrix, max_components=anti_pca_components)
            matrix = offline.remove_pc_projection(matrix - mean, pcs[:anti_pca_components])
        matrices.append(normalize_matrix(matrix))

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
        scores = np.zeros(len(candidate_ids), dtype=np.float64)
        for query_matrix in matrices:
            query_vector = query_matrix[bucket.query_index]
            position_scores = []
            for candidate_matrix in matrices:
                position_scores.append(candidate_matrix[bucket.candidate_indices] @ query_vector)
            scores += np.max(np.stack(position_scores, axis=0), axis=0)
        order = np.argsort(scores)[::-1]
        output.append(
            Ranking(
                question_id=query_record.question_id,
                instance_index=instance_index,
                ranked_ids=[candidate_ids[int(index)] for index in order],
                gold_ids=bucket.gold_ids,
                is_abstention=query_record.is_abstention,
                has_target=query_record.has_target,
            )
        )
    return output


def normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    arr = np.asarray(matrix, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-12)


def add_rrf_config(
    configs: dict[str, dict[str, Any]],
    name: str,
    judge_names: list[str],
    rankings_list: list[list[Ranking]],
    baseline_predictions: list[Prediction],
    args: argparse.Namespace,
) -> None:
    rankings = rrf_rankings(rankings_list, rrf_k=args.rrf_k)
    add_single_config(configs, name, judge_names, rankings, baseline_predictions, args)


def add_single_config(
    configs: dict[str, dict[str, Any]],
    name: str,
    judge_names: list[str],
    rankings: list[Ranking],
    baseline_predictions: list[Prediction],
    args: argparse.Namespace,
) -> None:
    predictions = predictions_from_rankings(rankings, args.top_k)
    metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=args.bootstrap_samples)
    delta = paired_delta(
        predictions,
        baseline_predictions,
        bootstrap_samples=args.bootstrap_samples,
    )
    configs[name] = {
        "kind": "rrf" if len(judge_names) > 1 else "single",
        "judges": judge_names,
        "metrics": metrics,
        "paired_delta_vs_baseline": delta,
        "interpretation": interpret_delta(delta),
    }


def rrf_rankings(rankings_list: list[list[Ranking]], *, rrf_k: int) -> list[Ranking]:
    if not rankings_list:
        raise ValueError("No rankings provided for RRF.")
    base = rankings_list[0]
    for rankings in rankings_list[1:]:
        if [item.question_id for item in rankings] != [item.question_id for item in base]:
            raise ValueError("RRF rankings have mismatched question order.")

    fused = []
    for index, base_item in enumerate(base):
        scores: dict[str, float] = {}
        for rankings in rankings_list:
            item = rankings[index]
            for rank, candidate_id in enumerate(item.ranked_ids, start=1):
                scores[candidate_id] = scores.get(candidate_id, 0.0) + 1.0 / (rrf_k + rank)
        ranked = [candidate_id for candidate_id, _score in sorted(scores.items(), key=lambda kv: kv[1], reverse=True)]
        fused.append(
            Ranking(
                question_id=base_item.question_id,
                instance_index=base_item.instance_index,
                ranked_ids=ranked,
                gold_ids=base_item.gold_ids,
                is_abstention=base_item.is_abstention,
                has_target=base_item.has_target,
            )
        )
    return fused


def predictions_from_rankings(rankings: list[Ranking], top_k: int) -> list[Prediction]:
    return [
        Prediction(
            question_id=item.question_id,
            retrieved_ids=item.ranked_ids[:top_k],
            gold_ids=item.gold_ids,
            is_abstention=item.is_abstention,
            has_target=item.has_target,
        )
        for item in rankings
    ]


def paired_delta(
    predictions: list[Prediction],
    baseline_predictions: list[Prediction],
    *,
    bootstrap_samples: int,
) -> dict[str, Any]:
    by_qid = {prediction.question_id: prediction for prediction in predictions}
    base_by_qid = {prediction.question_id: prediction for prediction in baseline_predictions}
    common = [
        qid
        for qid in by_qid
        if qid in base_by_qid
        and not by_qid[qid].is_abstention
        and by_qid[qid].has_target
        and by_qid[qid].gold_ids
    ]
    if not common:
        raise ValueError("No common scored predictions for paired delta.")

    deltas: dict[str, list[float]] = {
        "recall_all@5": [],
        "ndcg_any@5": [],
        "recall_all@10": [],
        "recall_all@50": [],
    }
    for qid in common:
        pred = by_qid[qid]
        base = base_by_qid[qid]
        deltas["recall_all@5"].append(
            recall_all_at_k(pred.retrieved_ids, pred.gold_ids, 5)
            - recall_all_at_k(base.retrieved_ids, base.gold_ids, 5)
        )
        deltas["ndcg_any@5"].append(
            ndcg_any_at_k(pred.retrieved_ids, pred.gold_ids, 5)
            - ndcg_any_at_k(base.retrieved_ids, base.gold_ids, 5)
        )
        deltas["recall_all@10"].append(
            recall_all_at_k(pred.retrieved_ids, pred.gold_ids, 10)
            - recall_all_at_k(base.retrieved_ids, base.gold_ids, 10)
        )
        deltas["recall_all@50"].append(
            recall_all_at_k(pred.retrieved_ids, pred.gold_ids, 50)
            - recall_all_at_k(base.retrieved_ids, base.gold_ids, 50)
        )

    return {
        "n_scored": len(common),
        "metrics": {
            name: {
                "mean": float(np.mean(values)),
                "ci95": bootstrap_ci(values, bootstrap_samples=bootstrap_samples, seed=17),
            }
            for name, values in deltas.items()
        },
    }


def bootstrap_ci(values: list[float], *, bootstrap_samples: int, seed: int) -> dict[str, float]:
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 1 or bootstrap_samples <= 0:
        mean = float(np.mean(arr))
        return {"low": mean, "high": mean}
    rng = np.random.default_rng(seed)
    sample_means = []
    for _ in range(bootstrap_samples):
        sample = rng.choice(arr, size=arr.size, replace=True)
        sample_means.append(float(np.mean(sample)))
    low, high = np.percentile(sample_means, [2.5, 97.5])
    return {"low": float(low), "high": float(high)}


def interpret_delta(delta: dict[str, Any]) -> str:
    r5_delta = float(delta["metrics"]["recall_all@5"]["mean"])
    if r5_delta >= SIGNAL_THRESHOLD:
        return "candidate_signal"
    if r5_delta <= -SIGNAL_THRESHOLD:
        return "clear_regression"
    return "noise_range"


def top_metric_rows(configs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for name, payload in configs.items():
        metrics = payload["metrics"]
        r5 = metrics["metrics"]["recall_all@5"]
        ndcg5 = metrics["metrics"]["ndcg_any@5"]
        delta = payload["paired_delta_vs_baseline"]["metrics"]["recall_all@5"]
        rows.append(
            {
                "config": name,
                "kind": payload["kind"],
                "recall_all@5": r5["mean"],
                "recall_all@5_ci95": r5["ci95"],
                "ndcg_any@5": ndcg5["mean"],
                "ndcg_any@5_ci95": ndcg5["ci95"],
                "delta_recall_all@5_vs_baseline": delta["mean"],
                "delta_recall_all@5_vs_baseline_ci95": delta["ci95"],
                "interpretation": payload["interpretation"],
                "n_scored": metrics["n_scored"],
            }
        )
    return sorted(rows, key=lambda row: (row["recall_all@5"], row["ndcg_any@5"]), reverse=True)


def write_outputs(result: dict[str, Any], prefix: str) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results_dir = ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    json_path = results_dir / f"{prefix}_{timestamp}.json"
    md_path = results_dir / f"{prefix}_{timestamp}.md"
    json_path.write_text(json.dumps(to_jsonable(result), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(result), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        "# Offline Hidden-Only Ensemble",
        "",
        "This run reads saved 9B Stage 2 vectors and does not run the model.",
        "",
        "## Design Decisions",
        "",
    ]
    for decision in result["design_decisions"]:
        lines.append(f"- {decision}")
    lines.extend(
        [
            "",
            "## Top Configs",
            "",
            "| config | R@5 | R@5 95% CI | NDCG@5 | delta R@5 vs baseline | interpretation | n |",
            "|---|---:|---:|---:|---:|---|---:|",
        ]
    )
    for row in result["top_configs"]:
        ci = row["recall_all@5_ci95"]
        dci = row["delta_recall_all@5_vs_baseline_ci95"]
        lines.append(
            f"| `{row['config']}` | {row['recall_all@5']:.3f} | "
            f"[{ci['low']:.3f}, {ci['high']:.3f}] | {row['ndcg_any@5']:.3f} | "
            f"{row['delta_recall_all@5_vs_baseline']:+.3f} "
            f"[{dci['low']:+.3f}, {dci['high']:+.3f}] | "
            f"{row['interpretation']} | {row['n_scored']} |"
        )
    lines.append("")
    return "\n".join(lines)


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [to_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    return value


if __name__ == "__main__":
    raise SystemExit(main())
