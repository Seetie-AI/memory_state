"""Analyze hidden-state dumps without rerunning the LLM.

This script consumes tensors produced by `dump_hidden_states.py`. It supports
the reusable analysis loop requested after the Phase 2 negative result:
compare layer choices, score normalization, prompt-vector collapse, vector
transforms, layer ensembles, and selected Tier B position slices.

Why this exists: MVP_Plan.md defines the v0 method as a single prompt-final
hidden vector. The later deep-dive showed that the vector geometry matters as
much as the layer. These offline analyses let us test geometry hypotheses on
the existing Tier A/Tier B dumps without spending more model-forward time.
"""

from __future__ import annotations

import argparse
import gc
import json
import sys
import warnings
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import mlx.core as mx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from eval.longmemeval_metrics import Prediction, evaluate
from longmemeval.data import load_instances
from method.hidden_state import SUMMARY_PROMPT_SUFFIX


ROUND1_ANALYSES = [
    "z_score_sweep",
    "centering_comparison",
    "anti_pca_sweep",
    "layer_concat_sweep",
    "residual_delta_sweep",
    "multilayer_rrf",
    "question_type_breakdown",
    "score_diagnostics",
    "suffix_position_scan",
]

ROUND2_ANALYSES = [
    "anti_pca_extended_sweep",
    "whitening_sweep",
    "multi_gold_breakdown",
    "transform_ablation",
    "rank_and_error_diagnostics",
]

ROUND3_ANALYSES = [
    "query_only_anti_pca_stability",
    "corpus_stat_sampling",
    "session_hit_diagnostics",
    "same_session_rerank_baseline",
]

ROUND4_ANALYSES = [
    "apples_to_apples_baselines",
    "statistical_robustness",
    "session_reframing_table",
    "score_fusion_alpha_sweep",
    "oracle_ceiling_overlap",
]

TIER_B_EXTRA_ANALYSES = [
    "content_end_position_scan",
    "position_debiased_retrieval",
    "layer_scan_at_content_end",
]


@dataclass(frozen=True)
class VectorSpec:
    """A reusable definition of which Tier A vector geometry to evaluate."""

    name: str
    kind: str
    layers: tuple[int, ...] = ()
    left: int | None = None
    right: int | None = None


@dataclass(frozen=True)
class ScoredPrediction:
    """Prediction plus per-candidate scores for diagnostics."""

    prediction: Prediction
    query_record: dict[str, Any]
    candidate_records: list[dict[str, Any]]
    candidate_ids: list[str]
    scores: np.ndarray
    gold_mask: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(ROOT / "tensors" / "dump_v1"))
    parser.add_argument("--data", default=str(ROOT / "data" / "longmemeval_s_cleaned.json"))
    parser.add_argument(
        "--analysis",
        choices=[
            "layer_scan_retrieval",
            "pairwise_cosine_per_layer",
            "score_mode_comparison",
            "position_scan_within_layer",
            "diagonal_slice",
            "pool_combinations",
            *ROUND1_ANALYSES,
            *ROUND2_ANALYSES,
            *ROUND3_ANALYSES,
            *ROUND4_ANALYSES,
            *TIER_B_EXTRA_ANALYSES,
        ],
        required=True,
    )
    parser.add_argument("--layer", type=int, default=22)
    parser.add_argument("--score-mode", choices=["cosine", "dot", "centered_cosine"], default="cosine")
    parser.add_argument("--sample-prompts", type=int, default=256)
    parser.add_argument("--rrf-k", type=float, default=60.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dump_dir = Path(args.dump_dir)
    manifest = json.loads((dump_dir / "manifest.json").read_text(encoding="utf-8"))

    if args.analysis == "layer_scan_retrieval":
        result = layer_scan_retrieval(dump_dir, manifest, score_mode=args.score_mode)
    elif args.analysis == "pairwise_cosine_per_layer":
        result = pairwise_cosine_per_layer(dump_dir, manifest, sample_prompts=args.sample_prompts)
    elif args.analysis == "score_mode_comparison":
        result = score_mode_comparison(dump_dir, manifest)
    elif args.analysis == "position_scan_within_layer":
        result = position_scan_within_layer(dump_dir, manifest, layer=args.layer, score_mode=args.score_mode)
    elif args.analysis == "diagonal_slice":
        result = diagonal_slice(dump_dir, manifest, score_mode=args.score_mode)
    elif args.analysis == "pool_combinations":
        result = pool_combinations(dump_dir, manifest, layer=args.layer, score_mode=args.score_mode)
    elif args.analysis == "z_score_sweep":
        result = z_score_sweep(dump_dir, manifest)
    elif args.analysis == "centering_comparison":
        result = centering_comparison(dump_dir, manifest)
    elif args.analysis == "anti_pca_sweep":
        result = anti_pca_sweep(dump_dir, manifest)
    elif args.analysis == "layer_concat_sweep":
        result = layer_concat_sweep(dump_dir, manifest)
    elif args.analysis == "residual_delta_sweep":
        result = residual_delta_sweep(dump_dir, manifest)
    elif args.analysis == "multilayer_rrf":
        result = multilayer_rrf(dump_dir, manifest, rrf_k=args.rrf_k)
    elif args.analysis == "question_type_breakdown":
        result = question_type_breakdown(dump_dir, manifest, data_path=Path(args.data))
    elif args.analysis == "score_diagnostics":
        result = score_diagnostics(dump_dir, manifest)
    elif args.analysis == "suffix_position_scan":
        result = suffix_position_scan(dump_dir, manifest, layer=args.layer, score_mode=args.score_mode)
    elif args.analysis == "anti_pca_extended_sweep":
        result = anti_pca_extended_sweep(dump_dir, manifest)
    elif args.analysis == "whitening_sweep":
        result = whitening_sweep(dump_dir, manifest)
    elif args.analysis == "multi_gold_breakdown":
        result = multi_gold_breakdown(dump_dir, manifest)
    elif args.analysis == "transform_ablation":
        result = transform_ablation(dump_dir, manifest)
    elif args.analysis == "rank_and_error_diagnostics":
        result = rank_and_error_diagnostics(dump_dir, manifest, data_path=Path(args.data))
    elif args.analysis == "query_only_anti_pca_stability":
        result = query_only_anti_pca_stability(dump_dir, manifest)
    elif args.analysis == "corpus_stat_sampling":
        result = corpus_stat_sampling(dump_dir, manifest)
    elif args.analysis == "session_hit_diagnostics":
        result = session_hit_diagnostics(dump_dir, manifest)
    elif args.analysis == "same_session_rerank_baseline":
        result = same_session_rerank_baseline(dump_dir, manifest)
    elif args.analysis == "apples_to_apples_baselines":
        result = apples_to_apples_baselines(dump_dir, manifest)
    elif args.analysis == "statistical_robustness":
        result = statistical_robustness(dump_dir, manifest)
    elif args.analysis == "session_reframing_table":
        result = session_reframing_table(dump_dir, manifest)
    elif args.analysis == "score_fusion_alpha_sweep":
        result = score_fusion_alpha_sweep(dump_dir, manifest)
    elif args.analysis == "oracle_ceiling_overlap":
        result = oracle_ceiling_overlap(dump_dir, manifest)
    elif args.analysis == "content_end_position_scan":
        result = content_end_position_scan(dump_dir, manifest)
    elif args.analysis == "position_debiased_retrieval":
        result = position_debiased_retrieval(dump_dir, manifest)
    elif args.analysis == "layer_scan_at_content_end":
        result = layer_scan_at_content_end(dump_dir, manifest)
    else:
        raise ValueError(f"Unsupported analysis: {args.analysis}")

    write_analysis_result(args.analysis, result)
    return 0


def layer_scan_retrieval(
    dump_dir: Path,
    manifest: dict[str, Any],
    score_mode: str,
) -> dict[str, Any]:
    """Evaluate retrieval for each Tier A layer and final post-norm vector."""
    records, tensors = load_tier_a(dump_dir, manifest)
    output: dict[str, Any] = {"score_mode": score_mode, "layers": {}}
    layer_count = tensors["last_by_layer"].shape[1]
    for layer in range(layer_count):
        vectors = tensors["last_by_layer"][:, layer, :]
        output["layers"][str(layer)] = evaluate_vectors(records, vectors, score_mode)
    output["final_post_norm"] = evaluate_vectors(records, tensors["final_post_norm"], score_mode)
    return output


def pairwise_cosine_per_layer(
    dump_dir: Path,
    manifest: dict[str, Any],
    sample_prompts: int,
) -> dict[str, Any]:
    """Measure prompt-vector collapse by pairwise cosine distribution per layer."""
    _records, tensors = load_tier_a(dump_dir, manifest)
    vectors = tensors["last_by_layer"][:sample_prompts].astype(np.float32)
    result: dict[str, Any] = {"sample_prompts": int(vectors.shape[0]), "layers": {}}
    for layer in range(vectors.shape[1]):
        cosines = pairwise_cosines(vectors[:, layer, :])
        result["layers"][str(layer)] = summarize_array(cosines)
    result["final_post_norm"] = summarize_array(pairwise_cosines(tensors["final_post_norm"][:sample_prompts]))
    return result


def score_mode_comparison(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Compare raw dot, cosine, and centered cosine for each layer."""
    return {
        mode: layer_scan_retrieval(dump_dir, manifest, score_mode=mode)
        for mode in ["dot", "cosine", "centered_cosine"]
    }


def z_score_sweep(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 1: compare per-dimension z-score transforms.

    Why: centered cosine helped because prompt-final states share a large common
    direction. Z-scoring tests whether some dimensions also dominate ranking by
    scale rather than by memory-specific information.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    configs: dict[str, Any] = {}
    for layer in [18, 19, 20, 21, 22, 23]:
        vectors = vectors_for_spec(tensors, VectorSpec(name=f"layer{layer}", kind="layer", layers=(layer,)))
        configs[f"layer{layer}_zscore_instance"] = evaluate_transformed(
            records, vectors, transform="zscore_instance"
        )
        configs[f"layer{layer}_zscore_global"] = evaluate_transformed(
            records, vectors, transform="zscore_global", global_stats=global_zscore_stats(records, vectors)
        )
    configs["final_zscore_instance"] = evaluate_transformed(
        records, tensors["final_post_norm"], transform="zscore_instance"
    )
    configs["final_zscore_global"] = evaluate_transformed(
        records,
        tensors["final_post_norm"],
        transform="zscore_global",
        global_stats=global_zscore_stats(records, tensors["final_post_norm"]),
    )
    return {"configs": configs, "top_configs": top_metric_rows(configs)}


def centering_comparison(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 1: compare per-instance vs global centering.

    Why: current best results use per-instance candidate centering. This checks
    whether the gain comes from local candidate-set de-biasing or from removing
    one global prompt-suffix direction.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    configs: dict[str, Any] = {}
    for layer in [18, 19, 20, 21, 22, 23]:
        vectors = vectors_for_spec(tensors, VectorSpec(name=f"layer{layer}", kind="layer", layers=(layer,)))
        configs[f"layer{layer}_cosine"] = evaluate_vectors(records, vectors, "cosine")
        configs[f"layer{layer}_center_instance"] = evaluate_transformed(
            records, vectors, transform="center_instance"
        )
        configs[f"layer{layer}_center_global"] = evaluate_transformed(
            records, vectors, transform="center_global", global_stats=global_center_stats(records, vectors)
        )
    configs["final_center_instance"] = evaluate_transformed(
        records, tensors["final_post_norm"], transform="center_instance"
    )
    configs["final_center_global"] = evaluate_transformed(
        records,
        tensors["final_post_norm"],
        transform="center_global",
        global_stats=global_center_stats(records, tensors["final_post_norm"]),
    )
    return {"configs": configs, "top_configs": top_metric_rows(configs)}


def anti_pca_sweep(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 1: project away top candidate principal components.

    Why: layer-15 collapse and centered-cosine gains suggest a few shared
    directions may swamp memory-specific signal. Anti-PCA directly removes
    those directions before cosine scoring.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    vectors = vectors_for_spec(tensors, VectorSpec(name="layer22", kind="layer", layers=(22,)))
    global_stats = global_anti_pca_stats(records, vectors, max_components=10)
    configs: dict[str, Any] = {}
    for components in [1, 2, 5, 10]:
        configs[f"layer22_anti_pca_instance_k{components}"] = evaluate_transformed(
            records,
            vectors,
            transform="anti_pca_instance",
            transform_kwargs={"components": components},
        )
        configs[f"layer22_anti_pca_global_k{components}"] = evaluate_transformed(
            records,
            vectors,
            transform="anti_pca_global",
            transform_kwargs={"components": components},
            global_stats=global_stats,
        )
    return {"configs": configs, "top_configs": top_metric_rows(configs)}


def layer_concat_sweep(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 1: concatenate neighboring deep-layer vectors.

    Why: layer 22 is best alone, but layers 21/23 may carry complementary
    errors. Concatenation preserves layer-specific coordinates before centered
    cosine scoring.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    layer_sets = [(21, 22), (21, 22, 23), (20, 21, 22, 23)]
    configs: dict[str, Any] = {}
    for layers in layer_sets:
        name = "concat_" + "_".join(str(layer) for layer in layers)
        vectors = vectors_for_spec(tensors, VectorSpec(name=name, kind="concat", layers=layers))
        configs[f"{name}_center_instance"] = evaluate_transformed(
            records, vectors, transform="center_instance"
        )
    return {"configs": configs, "top_configs": top_metric_rows(configs)}


def residual_delta_sweep(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 1: evaluate residual deltas between layers.

    Why: subtracting an earlier layer may remove the prompt-suffix/base
    residual stream while preserving the semantic update added by deeper
    transformer blocks.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    pairs = [(22, 21), (23, 22), (22, 18)]
    configs: dict[str, Any] = {}
    for left, right in pairs:
        name = f"delta_{left}_minus_{right}"
        vectors = vectors_for_spec(
            tensors,
            VectorSpec(name=name, kind="delta", left=left, right=right),
        )
        configs[f"{name}_center_instance"] = evaluate_transformed(
            records, vectors, transform="center_instance"
        )
    return {"configs": configs, "top_configs": top_metric_rows(configs)}


def multilayer_rrf(dump_dir: Path, manifest: dict[str, Any], rrf_k: float) -> dict[str, Any]:
    """Round 1: reciprocal-rank fusion over several strong layers.

    Why: RRF uses ranking agreement instead of assuming hidden dimensions from
    different layers are geometrically aligned. This is a robust ensemble path
    if layers 21/22/23 make complementary mistakes.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    vector_sets = {
        "layer21": tensors["last_by_layer"][:, 21, :],
        "layer22": tensors["last_by_layer"][:, 22, :],
        "layer23": tensors["last_by_layer"][:, 23, :],
        "final": tensors["final_post_norm"],
    }
    predictions = build_rrf_predictions(records, vector_sets, rrf_k=rrf_k)
    return {
        "rrf_k": rrf_k,
        "configs": {
            "rrf_layer21_22_23_final_center_instance": evaluate(
                predictions,
                skip_abstention=True,
                bootstrap_samples=200,
            )
        },
    }


def question_type_breakdown(
    dump_dir: Path,
    manifest: dict[str, Any],
    data_path: Path,
) -> dict[str, Any]:
    """Round 1: break promising configs down by LongMemEval question type.

    Why: a single Recall@5 can hide structure. The hidden-state method may be
    useful for some memory skills and weak for others, which determines the
    next optimization direction.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    question_types = load_question_types(data_path)
    configs = tier_a_reference_configs(records, tensors)
    output: dict[str, Any] = {}
    for name, predictions in configs.items():
        output[name] = evaluate_predictions_by_question_type(predictions, question_types)
    return output


def score_diagnostics(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 1: inspect gold/non-gold score separation for key configs.

    Why: retrieval metrics tell whether gold appears in top-k, but diagnostics
    show whether failures come from weak score separation, hard negatives, or a
    few pathological questions.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    layer22 = tensors["last_by_layer"][:, 22, :]
    scored = {
        "final_cosine": scored_predictions_from_vectors(records, tensors["final_post_norm"], "cosine"),
        "layer22_center_instance": scored_predictions_from_vectors(
            records,
            layer22,
            transform="center_instance",
        ),
    }
    return {name: summarize_scored_predictions(items) for name, items in scored.items()}


def suffix_position_scan(
    dump_dir: Path,
    manifest: dict[str, Any],
    layer: int,
    score_mode: str,
) -> dict[str, Any]:
    """Round 1: test suffix-local positions on Tier B.

    Why: Tier B already showed full-sequence mean/max pooling collapses. This
    narrower scan tests whether the final token is uniquely useful or whether a
    short suffix window around the prompt end is better.
    """
    pools = ["last", "minus2", "minus3", "mean_last3", "mean_last5"]
    predictions_by_pool: dict[str, list[Prediction]] = {name: [] for name in pools}
    for _instance_index, entries in iter_tier_b_by_instance(dump_dir, manifest):
        records = []
        vectors_by_pool: dict[str, list[np.ndarray]] = {name: [] for name in pools}
        for record, tensor in entries:
            layer_tensor = tensor[layer]
            records.append(record)
            for name in pools:
                vectors_by_pool[name].append(suffix_vector(layer_tensor, name))
        for name, vectors in vectors_by_pool.items():
            prediction = build_prediction_for_instance(records, np.stack(vectors, axis=0), score_mode)
            if prediction is not None:
                predictions_by_pool[name].append(prediction)
    return {
        name: evaluate(predictions, skip_abstention=True, bootstrap_samples=200)
        for name, predictions in predictions_by_pool.items()
        if predictions
    }


def anti_pca_extended_sweep(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 2: deepen the winning anti-PCA direction.

    Why: Round 1 found global anti-PCA on layer 22 is the best current geometry
    fix. This is the same family as All-but-the-top style embedding
    post-processing: remove dominant corpus-wide principal directions before
    nearest-neighbor retrieval.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    layer22 = vectors_for_spec(tensors, VectorSpec(name="layer22", kind="layer", layers=(22,)))
    configs: dict[str, Any] = {}

    layer22_stats = global_anti_pca_stats(records, layer22, max_components=200)
    for components in [15, 20, 30, 50, 80, 100, 200]:
        configs[f"layer22_anti_pca_global_k{components}"] = evaluate_transformed(
            records,
            layer22,
            transform="anti_pca_global",
            transform_kwargs={"components": components},
            global_stats=layer22_stats,
        )

    layer_specs = {
        "layer21": VectorSpec(name="layer21", kind="layer", layers=(21,)),
        "layer22": VectorSpec(name="layer22", kind="layer", layers=(22,)),
        "layer23": VectorSpec(name="layer23", kind="layer", layers=(23,)),
        "final": VectorSpec(name="final", kind="final"),
    }
    for name, spec in layer_specs.items():
        vectors = vectors_for_spec(tensors, spec)
        stats = global_anti_pca_stats(records, vectors, max_components=10)
        configs[f"{name}_anti_pca_global_k10"] = evaluate_transformed(
            records,
            vectors,
            transform="anti_pca_global",
            transform_kwargs={"components": 10},
            global_stats=stats,
        )

    return {"configs": configs, "top_configs": top_metric_rows(configs)}


def whitening_sweep(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 2: test global whitening variants on layer 22.

    Why: WhiteningBERT and related embedding-isotropy work show that whitening
    can improve unsupervised sentence retrieval. Anti-PCA only removes a few
    directions; whitening re-scales the full covariance spectrum after mean
    removal. We use global whitening only because per-instance covariance is
    rank-deficient for about 240 candidates in a 2048-dimensional space.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    vectors = vectors_for_spec(tensors, VectorSpec(name="layer22", kind="layer", layers=(22,)))
    configs: dict[str, Any] = {}
    for shrinkage in [0.01, 0.1]:
        stats = global_whitening_stats(records, vectors, shrinkage=shrinkage)
        for keep_dims in [128, 256, 512, 1024, 2048]:
            configs[f"layer22_whitening_global_lambda{shrinkage}_dim{keep_dims}"] = evaluate_transformed(
                records,
                vectors,
                transform="whitening_global",
                transform_kwargs={"keep_dims": keep_dims},
                global_stats=stats,
            )
    return {"configs": configs, "top_configs": top_metric_rows(configs)}


def multi_gold_breakdown(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 2: isolate the strict multi-gold recall bottleneck.

    Why: Round 1 showed high pairwise gold/non-gold separation but weak
    multi-session Recall@5. This analysis separates single-gold and multi-gold
    questions and adds MRR / first-hit-position diagnostics to distinguish
    ranking weakness from the strict `all gold in top-k` metric.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    layer22 = tensors["last_by_layer"][:, 22, :]
    anti_stats = global_anti_pca_stats(records, layer22, max_components=10)
    configs = {
        "layer22_center_instance": predictions_from_vectors(
            records,
            layer22,
            "transformed_cosine",
            transform="center_instance",
        ),
        "layer22_anti_pca_global_k10": predictions_from_vectors(
            records,
            layer22,
            "transformed_cosine",
            transform="anti_pca_global",
            transform_kwargs={"components": 10},
            global_stats=anti_stats,
        ),
    }
    return {name: evaluate_by_gold_count(predictions) for name, predictions in configs.items()}


def transform_ablation(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 2: ablate whether transforms apply to candidates, query, or both.

    Why: centered cosine currently subtracts candidate-set mean from both
    candidates and query. That is a reasonable retrieval transform, but not a
    given. This checks whether the gain is from de-biasing candidates, moving
    the query into the candidate-centered frame, or both.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    vectors = tensors["last_by_layer"][:, 22, :]
    anti_stats = global_anti_pca_stats(records, vectors, max_components=10)
    configs = {
        "layer22_raw_cosine": evaluate_vectors(records, vectors, "cosine"),
        "layer22_center_both": evaluate_transformed(records, vectors, transform="center_instance"),
        "layer22_center_candidates_only": evaluate_transformed(
            records, vectors, transform="center_candidates_only"
        ),
        "layer22_center_query_only": evaluate_transformed(records, vectors, transform="center_query_only"),
        "layer22_anti_pca_both_k10": evaluate_transformed(
            records,
            vectors,
            transform="anti_pca_global",
            transform_kwargs={"components": 10},
            global_stats=anti_stats,
        ),
        "layer22_anti_pca_candidates_only_k10": evaluate_transformed(
            records,
            vectors,
            transform="anti_pca_global_candidates_only",
            transform_kwargs={"components": 10},
            global_stats=anti_stats,
        ),
        "layer22_anti_pca_query_only_k10": evaluate_transformed(
            records,
            vectors,
            transform="anti_pca_global_query_only",
            transform_kwargs={"components": 10},
            global_stats=anti_stats,
        ),
    }
    return {"configs": configs, "top_configs": top_metric_rows(configs)}


def rank_and_error_diagnostics(
    dump_dir: Path,
    manifest: dict[str, Any],
    data_path: Path,
) -> dict[str, Any]:
    """Round 2: inspect false positives, margins, and rank confounds.

    Why: after All-but-the-top / anti-PCA improvements, the next bottleneck is
    not whether hidden states contain signal, but why top-ranked errors outrank
    gold turns. Human-readable false positives and same-session/date rates tell
    whether errors are plausible memory confusions or geometry artifacts.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    contexts = round_candidate_contexts(data_path)
    layer22 = tensors["last_by_layer"][:, 22, :]
    anti_stats = global_anti_pca_stats(records, layer22, max_components=10)
    scored = {
        "layer22_center_instance": scored_predictions_from_vectors(
            records,
            layer22,
            transform="center_instance",
        ),
        "layer22_anti_pca_global_k10": scored_predictions_from_vectors(
            records,
            layer22,
            transform="anti_pca_global",
            transform_kwargs={"components": 10},
            global_stats=anti_stats,
        ),
    }
    return {name: detailed_error_summary(items, contexts) for name, items in scored.items()}


def query_only_anti_pca_stability(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 3: test whether query-only anti-PCA is stable across layers/k.

    Why: Round 2 found query-only anti-PCA nearly matches the previous
    both-sided anti-PCA score, while candidates-only is catastrophic. This
    isolates that finding with one variable changed per cell: source layer or
    number of removed global PCs.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    configs: dict[str, Any] = {}
    for layer in [21, 22, 23]:
        vectors = tensors["last_by_layer"][:, layer, :]
        stats = global_anti_pca_stats(records, vectors, max_components=15)
        for components in [2, 5, 10, 15]:
            configs[f"layer{layer}_query_only_anti_pca_k{components}"] = evaluate_transformed(
                records,
                vectors,
                transform="anti_pca_global_query_only",
                transform_kwargs={"components": components},
                global_stats=stats,
            )
    return {"configs": configs, "top_configs": top_metric_rows(configs)}


def corpus_stat_sampling(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 3: estimate how much corpus is needed for query-only anti-PCA.

    Why: Round 2 suggests the production-friendly path is transforming only the
    query by corpus-level PCs. This analysis checks whether those PCs require
    the full corpus or can be estimated from a smaller sample without a large
    retrieval drop.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    vectors = tensors["last_by_layer"][:, 22, :]
    fractions = [1.0, 0.5, 0.25, 0.1, 0.05]
    seeds = [0, 1, 2, 3, 4]
    output: dict[str, Any] = {"layer": 22, "k": 10, "fractions": {}}
    for fraction in fractions:
        runs = []
        for seed in seeds:
            stats = sampled_global_anti_pca_stats(records, vectors, max_components=10, fraction=fraction, seed=seed)
            result = evaluate_transformed(
                records,
                vectors,
                transform="anti_pca_global_query_only",
                transform_kwargs={"components": 10},
                global_stats=stats,
            )
            runs.append(result)
        output["fractions"][str(fraction)] = summarize_metric_runs(runs)
    return output


def session_hit_diagnostics(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 3: compare turn-level recall with session-level routing success.

    Why: Round 2 found 62% of top-1 false positives come from a gold session.
    This measures whether the hidden-state retriever is already a good
    session/topic router while failing at within-session turn disambiguation.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    vectors = tensors["last_by_layer"][:, 22, :]
    stats = global_anti_pca_stats(records, vectors, max_components=10)
    predictions = predictions_from_vectors(
        records,
        vectors,
        "transformed_cosine",
        transform="anti_pca_global",
        transform_kwargs={"components": 10},
        global_stats=stats,
    )
    return {
        "config": "layer22_anti_pca_global_k10",
        "groups": session_metrics_by_gold_count(predictions),
    }


def same_session_rerank_baseline(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 3: rerank top hidden-state turns with lexical evidence.

    Why: Round 2 showed the method often finds the right session but the wrong
    turn. This keeps the same hidden-state candidate generator and changes one
    second-stage variable: BM25-style lexical reranking inside its top-50
    candidates.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    vectors = tensors["last_by_layer"][:, 22, :]
    stats = global_anti_pca_stats(records, vectors, max_components=10)
    hidden_scored = scored_predictions_from_vectors(
        records,
        vectors,
        "transformed_cosine",
        transform="anti_pca_global",
        transform_kwargs={"components": 10},
        global_stats=stats,
    )
    reranked = [rerank_prediction_by_top50_bm25(item) for item in hidden_scored]
    return {
        "baseline_hidden_state": evaluate(
            [item.prediction for item in hidden_scored],
            skip_abstention=True,
            bootstrap_samples=200,
        ),
        "top50_bm25_rerank": evaluate(reranked, skip_abstention=True, bootstrap_samples=200),
        "by_gold_count": evaluate_by_gold_count(reranked),
    }


def apples_to_apples_baselines(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 4: restrict baselines to the exact 94 scored dump questions.

    Why: this is not another attempt to find a higher score. It is a guardrail
    for the paper-style summary: every baseline and hidden-state method should
    be compared on the same question IDs and with both turn-level and
    session-level metrics.
    """
    reference_qids = reference_scored_question_ids(dump_dir, manifest)
    methods = load_available_baseline_predictions(reference_qids)
    return {
        name: compact_method_metrics(predictions, bootstrap_samples=1000)
        for name, predictions in methods.items()
    }


def statistical_robustness(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 4: bootstrap and split-check the top hidden-state configs.

    Why: after several exploratory rounds, the risk is p-hacking on 100
    instances. This analysis asks whether the top configurations are stable
    under resampling and a fixed 50/50 split, not whether we can tune another
    point of Recall@5.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    configs = hidden_state_core_predictions(records, tensors)
    bootstrap = {
        name: evaluate(predictions, skip_abstention=True, bootstrap_samples=1000)
        for name, predictions in configs.items()
    }
    split = split_stability(configs, seed=0)
    return {"bootstrap_1000": bootstrap, "split_50_50": split}


def session_reframing_table(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 4: present the method as both turn retriever and session router.

    Why: Round 3 showed session_hit@5 is much stronger than turn Recall@5. This
    table prevents the summary from cherry-picking: it reports the same
    session-level metrics for baselines and hidden-state configs.
    """
    reference_qids = reference_scored_question_ids(dump_dir, manifest)
    records, tensors = load_tier_a(dump_dir, manifest)
    methods = load_available_baseline_predictions(reference_qids)
    methods.update(hidden_state_core_predictions(records, tensors))
    return {
        name: compact_method_metrics(filter_predictions_to_qids(predictions, reference_qids), bootstrap_samples=1000)
        for name, predictions in methods.items()
    }


def score_fusion_alpha_sweep(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 4: report the full hidden/BM25 top-50 fusion curve.

    Why: BM25 replacement hurt in Round 3. Fusion is a controlled combination,
    but the anti-p-hacking rule is to report every alpha value, not only the
    best one.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    layer22 = tensors["last_by_layer"][:, 22, :]
    stats = global_anti_pca_stats(records, layer22, max_components=10)
    hidden_scored = scored_predictions_from_vectors(
        records,
        layer22,
        "transformed_cosine",
        transform="anti_pca_global_query_only",
        transform_kwargs={"components": 10},
        global_stats=stats,
    )
    output: dict[str, Any] = {"score_normalization": "zscore within hidden top-50", "alphas": {}}
    for alpha in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]:
        predictions = [fuse_top50_hidden_bm25(item, alpha=alpha) for item in hidden_scored]
        output["alphas"][str(alpha)] = compact_method_metrics(predictions, bootstrap_samples=1000)
    return output


def oracle_ceiling_overlap(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Round 4: estimate diagnostic ensemble ceiling and rank overlap.

    Why: this is explicitly not a deployable method. It tells the paper-style
    summary whether top configs fail on the same questions or have complementary
    errors, which determines whether future ensemble work is worth doing.
    """
    records, tensors = load_tier_a(dump_dir, manifest)
    configs = hidden_state_core_predictions(records, tensors)
    return {
        "warning": "Oracle ceiling is diagnostic only, not a real method.",
        "oracle": oracle_prediction_metrics(configs),
        "jaccard_at5": rank_overlap_jaccard(configs, k=5),
    }


def content_end_position_scan(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Tier B extra: compare content-end / suffix-start / late positions.

    Why: Stage 1 showed the position axis is underexplored. Anti-PCA removes
    corpus-wide directions; content-end and suffix-start positions test a more
    local hypothesis: whether the fixed summary suffix itself is the source of
    useful or harmful shared signal. Tier B has only 20 instances, so this is a
    direction-finding experiment, not a final claim.
    """
    suffix_len = suffix_token_count()
    positions = ["content_end", "suffix_start", "minus2", "last"]
    valid_prompt_ids = valid_tier_b_prompt_ids(manifest, positions, suffix_len)
    output: dict[str, Any] = {
        "disclaimer": tier_b_disclaimer(),
        "memory_plan": tier_b_memory_plan(),
        "layer": 22,
        "suffix_token_count": suffix_len,
        "valid_prompt_count": len(valid_prompt_ids),
        "baseline": tier_b_baseline_metrics(
            dump_dir,
            manifest,
            suffix_len=suffix_len,
            valid_prompt_ids=valid_prompt_ids,
        ),
        "positions": {},
    }
    records, vectors_by_position, skipped = collect_tier_b_positions_at_layer(
        dump_dir,
        manifest,
        layer=22,
        positions=positions,
        suffix_len=suffix_len,
        valid_prompt_ids=valid_prompt_ids,
    )
    for position in positions:
        vectors = vectors_by_position[position]
        stats = global_anti_pca_stats(records, vectors, max_components=10)
        output["positions"][position] = {
            "skipped_prompt_count": skipped,
            "metrics": evaluate_transformed(
                records,
                vectors,
                transform="anti_pca_global",
                transform_kwargs={"components": 10},
                global_stats=stats,
            ),
        }
        del stats
        clear_mlx_memory()
    del records, vectors_by_position
    clear_mlx_memory()
    return output


def position_debiased_retrieval(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Tier B extra: subtract position-specific means before retrieval.

    Why: anti-PCA is a corpus-wide de-biasing method. Position de-biasing is a
    more precise variant inspired by the finding that the ignored position axis
    may encode template/suffix artifacts. It changes only the de-biasing axis:
    role-pooled mean or role-separated mean at the same layer/position.
    """
    suffix_len = suffix_token_count()
    positions = ["content_end", "minus2", "last"]
    valid_prompt_ids = valid_tier_b_prompt_ids(manifest, positions, suffix_len)
    output: dict[str, Any] = {
        "disclaimer": tier_b_disclaimer(),
        "memory_plan": tier_b_memory_plan(),
        "layer": 22,
        "suffix_token_count": suffix_len,
        "valid_prompt_count": len(valid_prompt_ids),
        "baseline": tier_b_baseline_metrics(
            dump_dir,
            manifest,
            suffix_len=suffix_len,
            valid_prompt_ids=valid_prompt_ids,
        ),
        "positions": {},
    }
    records, vectors_by_position, skipped = collect_tier_b_positions_at_layer(
        dump_dir,
        manifest,
        layer=22,
        positions=positions,
        suffix_len=suffix_len,
        valid_prompt_ids=valid_prompt_ids,
    )
    for position in positions:
        vectors = vectors_by_position[position]
        output["positions"][position] = {
            "skipped_prompt_count": skipped,
            "role_pooled_mean": evaluate_vectors(
                records,
                debias_by_position_mean(records, vectors, role_separated=False),
                "cosine",
            ),
            "role_separated_mean": evaluate_vectors(
                records,
                debias_by_position_mean(records, vectors, role_separated=True),
                "cosine",
            ),
        }
        clear_mlx_memory()
    del records, vectors_by_position
    clear_mlx_memory()
    return output


def layer_scan_at_content_end(dump_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Tier B extra: scan layers at the content-end position.

    Why: layer 22 is best at the prompt-final position, but changing the
    position may move the sweet spot. This keeps the scoring method fixed
    (anti-PCA k=10) and changes only the layer at content-end.
    """
    suffix_len = suffix_token_count()
    valid_prompt_ids = valid_tier_b_prompt_ids(manifest, ["content_end"], suffix_len)
    output: dict[str, Any] = {
        "disclaimer": tier_b_disclaimer(),
        "memory_plan": tier_b_memory_plan(),
        "position": "content_end",
        "suffix_token_count": suffix_len,
        "valid_prompt_count": len(valid_prompt_ids),
        "baseline": tier_b_baseline_metrics(
            dump_dir,
            manifest,
            suffix_len=suffix_len,
            valid_prompt_ids=valid_prompt_ids,
        ),
        "layers": {},
    }
    layers = list(range(16, 24))
    records, vectors_by_layer, skipped = collect_tier_b_layers_at_position(
        dump_dir,
        manifest,
        layers=layers,
        position="content_end",
        suffix_len=suffix_len,
        valid_prompt_ids=valid_prompt_ids,
    )
    for layer in layers:
        vectors = vectors_by_layer[layer]
        stats = global_anti_pca_stats(records, vectors, max_components=10)
        output["layers"][str(layer)] = {
            "skipped_prompt_count": skipped,
            "metrics": evaluate_transformed(
                records,
                vectors,
                transform="anti_pca_global",
                transform_kwargs={"components": 10},
                global_stats=stats,
            ),
        }
        del stats
        clear_mlx_memory()
    del records, vectors_by_layer
    clear_mlx_memory()
    return output


def position_scan_within_layer(
    dump_dir: Path,
    manifest: dict[str, Any],
    layer: int,
    score_mode: str,
) -> dict[str, Any]:
    """Run retrieval on Tier B fixed positions for one layer."""
    positions = [0, 1, 2, 4, 8, 16, 32, 64, 128, 256, -1]
    output: dict[str, Any] = {"layer": layer, "score_mode": score_mode, "positions": {}}
    predictions_by_position: dict[str, list[Prediction]] = {str(position): [] for position in positions}

    for _instance_index, entries in iter_tier_b_by_instance(dump_dir, manifest):
        for position in positions:
            records = []
            vectors = []
            for record, tensor in entries:
                seq_len = tensor.shape[1]
                resolved = position if position >= 0 else seq_len + position
                if 0 <= resolved < seq_len:
                    records.append(record)
                    vectors.append(tensor[layer, resolved, :])
            if vectors:
                prediction = build_prediction_for_instance(
                    records,
                    np.stack(vectors, axis=0),
                    score_mode,
                )
                if prediction is not None:
                    predictions_by_position[str(position)].append(prediction)

    for position in positions:
        predictions = predictions_by_position[str(position)]
        if predictions:
            output["positions"][str(position)] = evaluate(
                predictions,
                skip_abstention=True,
                bootstrap_samples=200,
            )
    return output


def diagonal_slice(dump_dir: Path, manifest: dict[str, Any], score_mode: str) -> dict[str, Any]:
    """Evaluate vectors from layer i, token i for Tier B prompts."""
    predictions = []
    for _instance_index, entries in iter_tier_b_by_instance(dump_dir, manifest):
        records = []
        vectors = []
        for record, tensor in entries:
            max_diag = min(tensor.shape[0], tensor.shape[1])
            diag_vectors = [tensor[index, index, :] for index in range(max_diag)]
            records.append(record)
            vectors.append(np.mean(np.stack(diag_vectors, axis=0), axis=0))
        prediction = build_prediction_for_instance(records, np.stack(vectors, axis=0), score_mode)
        if prediction is not None:
            predictions.append(prediction)
    return evaluate(predictions, skip_abstention=True, bootstrap_samples=200)


def pool_combinations(
    dump_dir: Path,
    manifest: dict[str, Any],
    layer: int,
    score_mode: str,
) -> dict[str, Any]:
    """Evaluate simple Tier B mean/max/last pooling combinations for one layer."""
    predictions_by_pool: dict[str, list[Prediction]] = {"last": [], "mean": [], "max": []}
    for _instance_index, entries in iter_tier_b_by_instance(dump_dir, manifest):
        records = []
        pools: dict[str, list[np.ndarray]] = {"last": [], "mean": [], "max": []}
        for record, tensor in entries:
            layer_tensor = tensor[layer]
            records.append(record)
            pools["last"].append(layer_tensor[-1])
            pools["mean"].append(np.mean(layer_tensor, axis=0))
            pools["max"].append(np.max(layer_tensor, axis=0))
        for name, vectors in pools.items():
            prediction = build_prediction_for_instance(records, np.stack(vectors, axis=0), score_mode)
            if prediction is not None:
                predictions_by_pool[name].append(prediction)

    return {
        name: evaluate(predictions, skip_abstention=True, bootstrap_samples=200)
        for name, predictions in predictions_by_pool.items()
        if predictions
    }


def load_tier_a(dump_dir: Path, manifest: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, np.ndarray]]:
    records = []
    last_chunks = []
    final_chunks = []
    prompt_records = manifest["prompts"]
    for chunk in manifest["tier_a_chunks"]:
        arrays = mx.load(str(dump_dir / chunk["file"]))
        last = np.asarray(arrays["last_by_layer"].astype(mx.float32))
        final = np.asarray(arrays["final_post_norm"].astype(mx.float32))
        last_chunks.append(last)
        final_chunks.append(final)
        records.extend(prompt_records[prompt_id] for prompt_id in chunk["prompt_ids"])
    return records, {
        "last_by_layer": np.concatenate(last_chunks, axis=0),
        "final_post_norm": np.concatenate(final_chunks, axis=0),
    }


def iter_tier_b_by_instance(
    dump_dir: Path,
    manifest: dict[str, Any],
) -> "Iterable[tuple[int, list[tuple[dict[str, Any], np.ndarray]]]]":
    """Yield one instance worth of Tier B tensors at a time.

    Tier B may contain thousands of prompts. Loading all bf16 tensors and
    casting to fp32 can exceed 16GB memory. Streaming by instance keeps only one
    query+candidates set in memory long enough to build a Prediction.

    Deprecated for new Tier B analyses: even one LongMemEval instance can hold
    hundreds of full tensors. Use `iter_tier_b_lean` for single layer/position
    slices so only 2048 fp32 values are materialized per prompt.
    """
    warnings.warn(
        "iter_tier_b_by_instance materializes full Tier B tensors and can exceed "
        "16GB memory; use iter_tier_b_lean for new analyses.",
        RuntimeWarning,
        stacklevel=2,
    )
    grouped: dict[int, list[dict[str, Any]]] = {}
    for record in manifest["prompts"].values():
        if "tier_b_file" in record:
            grouped.setdefault(int(record["instance_index"]), []).append(record)

    if not grouped:
        raise ValueError("No Tier B tensors found in manifest.")

    for instance_index in sorted(grouped):
        entries = []
        for record in grouped[instance_index]:
            arrays = mx.load(str(dump_dir / record["tier_b_file"]))
            tensor = np.asarray(arrays["all_by_layer"].astype(mx.float32))
            entries.append((record, tensor))
        yield instance_index, entries


def clear_mlx_memory() -> None:
    """Release Python objects and MLX's metal cache between Tier B slices.

    The Tier B files are large enough that relying on process teardown alone is
    unsafe on a 16GB Mac. MLX exposes `mx.metal.clear_cache()` in recent builds;
    if it is unavailable, normal Python GC still runs and the analysis proceeds.
    """
    gc.collect()
    try:
        if hasattr(mx, "metal") and hasattr(mx.metal, "clear_cache"):
            mx.metal.clear_cache()
    except Exception:
        pass


def tier_b_memory_plan() -> str:
    return (
        "Lean per-prompt slice loading: each safetensors file is opened, one "
        "small set of (layer, position, 2048) vectors is materialized as fp32, "
        "then the file object and MLX cache are released. Target peak memory "
        "for TB extra analyses is below the 8GB budget."
    )


def tier_b_records(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Return Tier B prompt records in manifest order."""
    return [record for record in manifest["prompts"].values() if "tier_b_file" in record]


def record_sequence_length(record: dict[str, Any]) -> int:
    """Infer the tensor sequence length stored for a Tier B prompt."""
    truncated = record.get("truncated_to")
    if truncated is not None:
        return int(truncated)
    return int(record["token_count"])


def valid_tier_b_prompt_ids(
    manifest: dict[str, Any],
    positions: list[str],
    suffix_len: int,
) -> set[str]:
    """Find prompt IDs valid for every compared position.

    This keeps apples-to-apples comparisons exact: if one position is invalid
    for a short prompt, all position variants drop that same prompt.
    """
    valid = set()
    for record in tier_b_records(manifest):
        seq_len = record_sequence_length(record)
        if all(resolve_tier_b_position(seq_len, position, suffix_len) is not None for position in positions):
            valid.add(str(record["prompt_id"]))
    return valid


def iter_tier_b_lean(
    dump_dir: Path,
    manifest: dict[str, Any],
    layer: int,
    position_resolver: Callable[[dict[str, Any]], int | None],
    valid_prompt_ids: set[str] | None = None,
    clear_every: int = 50,
) -> "Iterable[tuple[dict[str, Any], np.ndarray]]":
    """Yield one fp32 vector slice per Tier B prompt.

    New Tier B explorations should use this helper instead of
    `iter_tier_b_by_instance`. It changes the memory unit from "one full
    instance worth of 24 x seq_len x dim tensors" to "one 2048-dimensional
    vector", which is the difference between multi-GB peaks and a few MB.
    """
    yielded = 0
    for record in tier_b_records(manifest):
        if valid_prompt_ids is not None and str(record["prompt_id"]) not in valid_prompt_ids:
            continue
        position = position_resolver(record)
        if position is None:
            continue
        try:
            vector = load_tier_b_vector_slice(dump_dir, record, layer, position)
        except IndexError:
            # Manifest token counts should match tensor lengths, but if a dump
            # was truncated differently, skip that prompt instead of crashing a
            # long memory-sensitive run.
            continue
        yield record, vector
        yielded += 1
        if yielded % clear_every == 0:
            clear_mlx_memory()
    clear_mlx_memory()


def load_tier_b_vector_slice(
    dump_dir: Path,
    record: dict[str, Any],
    layer: int,
    position: int,
) -> np.ndarray:
    """Load one Tier B vector slice, preferring safetensors slicing.

    `safe_open(...).get_slice()` avoids materializing the full tensor. Some
    safetensors/numpy combinations do not expose MLX bf16 cleanly, so the
    fallback uses `mx.load` but immediately indexes one vector before casting to
    fp32.
    """
    path = dump_dir / record["tier_b_file"]
    try:
        from safetensors import safe_open

        with safe_open(str(path), framework="np") as handle:
            vector = np.asarray(handle.get_slice("all_by_layer")[layer, position, :])
        if vector.dtype != np.float32:
            vector = vector.astype(np.float32)
        return np.asarray(vector, dtype=np.float32)
    except Exception:
        arrays = mx.load(str(path))
        vector_mx = arrays["all_by_layer"][layer, position, :].astype(mx.float32)
        mx.eval(vector_mx)
        vector = np.array(vector_mx, dtype=np.float32)
        del arrays, vector_mx
        clear_mlx_memory()
        return vector


def load_tier_b_multi_slice(
    dump_dir: Path,
    record: dict[str, Any],
    layer_position_pairs: list[tuple[int, int]],
) -> dict[tuple[int, int], np.ndarray]:
    """Load several Tier B vector slices from one prompt file open.

    This is the 8GB-budget variant of `load_tier_b_vector_slice`: it still
    avoids full-tensor accumulation across prompts, but amortizes file IO for
    analyses that need several layers or positions from the same prompt.
    """
    unique_pairs = list(dict.fromkeys(layer_position_pairs))
    path = dump_dir / record["tier_b_file"]
    try:
        from safetensors import safe_open

        output = {}
        with safe_open(str(path), framework="np") as handle:
            tensor_slice = handle.get_slice("all_by_layer")
            for pair in unique_pairs:
                layer, position = pair
                vector = np.asarray(tensor_slice[layer, position, :])
                if vector.dtype != np.float32:
                    vector = vector.astype(np.float32)
                output[pair] = np.asarray(vector, dtype=np.float32)
        return output
    except Exception:
        arrays = mx.load(str(path))
        tensor = arrays["all_by_layer"]
        output = {}
        for layer, position in unique_pairs:
            vector_mx = tensor[layer, position, :].astype(mx.float32)
            mx.eval(vector_mx)
            output[(layer, position)] = np.array(vector_mx, dtype=np.float32)
            del vector_mx
        del arrays, tensor
        clear_mlx_memory()
        return output


def load_tier_b_layers_at_position(
    dump_dir: Path,
    record: dict[str, Any],
    position: int,
    layers: list[int],
) -> dict[int, np.ndarray]:
    """Load several layer slices at one position from one prompt file."""
    slices = load_tier_b_multi_slice(dump_dir, record, [(layer, position) for layer in layers])
    return {layer: slices[(layer, position)] for layer in layers}


def load_tier_b_positions_at_layer(
    dump_dir: Path,
    record: dict[str, Any],
    layer: int,
    positions: dict[str, int],
) -> dict[str, np.ndarray]:
    """Load several position slices at one layer from one prompt file."""
    slices = load_tier_b_multi_slice(dump_dir, record, [(layer, position) for position in positions.values()])
    return {name: slices[(layer, position)] for name, position in positions.items()}


def suffix_token_count() -> int:
    """Tokenize the shared suffix locally so content-end positions are exact."""
    from transformers import AutoTokenizer

    tokenizer_path = ROOT / "models" / "Qwen3.5-2B-hf"
    if not tokenizer_path.exists():
        tokenizer_path = ROOT / "models" / "Qwen3.5-2B-bf16"
    tokenizer = AutoTokenizer.from_pretrained(str(tokenizer_path), trust_remote_code=True)
    return len(tokenizer.encode(SUMMARY_PROMPT_SUFFIX, add_special_tokens=False))


def tier_b_disclaimer() -> str:
    return (
        "Tier B contains only 20 LongMemEval-S/round instances. Treat these "
        "results as direction-finding diagnostics, not final performance claims."
    )


def tier_b_baseline_metrics(
    dump_dir: Path,
    manifest: dict[str, Any],
    suffix_len: int,
    valid_prompt_ids: set[str] | None = None,
) -> dict[str, Any]:
    records, vectors, skipped = collect_tier_b_position_vectors(
        dump_dir,
        manifest,
        layer=22,
        position="last",
        suffix_len=suffix_len,
        valid_prompt_ids=valid_prompt_ids,
    )
    stats = global_anti_pca_stats(records, vectors, max_components=10)
    metrics = evaluate_transformed(
        records,
        vectors,
        transform="anti_pca_global",
        transform_kwargs={"components": 10},
        global_stats=stats,
    )
    valid_count = len(records)
    del records, vectors, stats
    clear_mlx_memory()
    return {
        "config": "layer22_last_anti_pca_global_k10",
        "valid_prompt_count": valid_count,
        "skipped_prompt_count": skipped,
        "metrics": metrics,
    }


def collect_tier_b_position_vectors(
    dump_dir: Path,
    manifest: dict[str, Any],
    layer: int,
    position: str,
    suffix_len: int,
    valid_prompt_ids: set[str] | None = None,
) -> tuple[list[dict[str, Any]], np.ndarray, int]:
    """Collect one Tier B layer/position matrix with <1GB peak memory.

    This deliberately does not use `iter_tier_b_by_instance`: the latter
    materializes full tensors for hundreds of prompts. Here each prompt loads
    only one 2048-dimensional vector slice, then releases its file/cache before
    the next prompt.
    """
    records = []
    vectors = []
    eligible_records = [
        record
        for record in tier_b_records(manifest)
        if valid_prompt_ids is None or str(record["prompt_id"]) in valid_prompt_ids
    ]

    def resolve_for_record(record: dict[str, Any]) -> int | None:
        return resolve_tier_b_position(record_sequence_length(record), position, suffix_len)

    for record, vector in iter_tier_b_lean(
        dump_dir,
        manifest,
        layer=layer,
        position_resolver=resolve_for_record,
        valid_prompt_ids=valid_prompt_ids,
    ):
        records.append(record)
        vectors.append(vector)
    if not vectors:
        raise ValueError(f"No Tier B vectors collected for layer={layer} position={position}.")
    skipped = len(eligible_records) - len(records)
    matrix = np.stack(vectors, axis=0).astype(np.float32, copy=False)
    del vectors
    clear_mlx_memory()
    return records, matrix, skipped


def collect_tier_b_positions_at_layer(
    dump_dir: Path,
    manifest: dict[str, Any],
    layer: int,
    positions: list[str],
    suffix_len: int,
    valid_prompt_ids: set[str] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, np.ndarray], int]:
    """Collect several position matrices with one file open per prompt.

    Used by position-debias analyses. It changes only IO scheduling relative
    to `collect_tier_b_position_vectors`; the vector definitions and valid
    prompt filtering remain identical.
    """
    records = []
    vectors_by_position: dict[str, list[np.ndarray]] = {position: [] for position in positions}
    eligible_records = [
        record
        for record in tier_b_records(manifest)
        if valid_prompt_ids is None or str(record["prompt_id"]) in valid_prompt_ids
    ]
    loaded = 0
    for record in eligible_records:
        resolved = {
            position: resolve_tier_b_position(record_sequence_length(record), position, suffix_len)
            for position in positions
        }
        if any(value is None for value in resolved.values()):
            continue
        try:
            slices = load_tier_b_positions_at_layer(
                dump_dir,
                record,
                layer=layer,
                positions={name: int(value) for name, value in resolved.items() if value is not None},
            )
        except IndexError:
            continue
        records.append(record)
        for position in positions:
            vectors_by_position[position].append(slices[position])
        loaded += 1
        if loaded % 50 == 0:
            clear_mlx_memory()
    if not records:
        raise ValueError(f"No Tier B vectors collected for layer={layer} positions={positions}.")
    matrices = {
        position: np.stack(vectors, axis=0).astype(np.float32, copy=False)
        for position, vectors in vectors_by_position.items()
    }
    skipped = len(eligible_records) - len(records)
    del vectors_by_position
    clear_mlx_memory()
    return records, matrices, skipped


def collect_tier_b_layers_at_position(
    dump_dir: Path,
    manifest: dict[str, Any],
    layers: list[int],
    position: str,
    suffix_len: int,
    valid_prompt_ids: set[str] | None = None,
) -> tuple[list[dict[str, Any]], dict[int, np.ndarray], int]:
    """Collect several layer matrices with one file open per prompt.

    Used by content-end layer scans. Holding eight 5043 x 2048 fp32 matrices is
    roughly a few hundred MB, comfortably below the requested 8GB ceiling while
    avoiding the previous 8x repeated file-open pattern.
    """
    records = []
    vectors_by_layer: dict[int, list[np.ndarray]] = {layer: [] for layer in layers}
    eligible_records = [
        record
        for record in tier_b_records(manifest)
        if valid_prompt_ids is None or str(record["prompt_id"]) in valid_prompt_ids
    ]
    loaded = 0
    for record in eligible_records:
        resolved = resolve_tier_b_position(record_sequence_length(record), position, suffix_len)
        if resolved is None:
            continue
        try:
            slices = load_tier_b_layers_at_position(dump_dir, record, int(resolved), layers)
        except IndexError:
            continue
        records.append(record)
        for layer in layers:
            vectors_by_layer[layer].append(slices[layer])
        loaded += 1
        if loaded % 50 == 0:
            clear_mlx_memory()
    if not records:
        raise ValueError(f"No Tier B vectors collected for layers={layers} position={position}.")
    matrices = {
        layer: np.stack(vectors, axis=0).astype(np.float32, copy=False)
        for layer, vectors in vectors_by_layer.items()
    }
    skipped = len(eligible_records) - len(records)
    del vectors_by_layer
    clear_mlx_memory()
    return records, matrices, skipped


def resolve_tier_b_position(seq_len: int, position: str, suffix_len: int) -> int | None:
    if position == "last":
        return seq_len - 1
    if position == "minus2":
        return seq_len - 2 if seq_len >= 2 else None
    suffix_start = seq_len - suffix_len
    if position == "suffix_start":
        return suffix_start if 0 <= suffix_start < seq_len else None
    if position == "content_end":
        content_end = suffix_start - 1
        return content_end if 0 <= content_end < seq_len else None
    raise ValueError(f"Unsupported Tier B position: {position}")


def debias_by_position_mean(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    role_separated: bool,
) -> np.ndarray:
    if not role_separated:
        return vectors - np.mean(vectors, axis=0, keepdims=True)
    output = vectors.copy()
    for role in ["query", "candidate"]:
        indices = [
            index
            for index, record in enumerate(records)
            if (record["role"] == "query") == (role == "query")
        ]
        if not indices:
            continue
        output[indices] = output[indices] - np.mean(output[indices], axis=0, keepdims=True)
    return output


def vectors_for_spec(tensors: dict[str, np.ndarray], spec: VectorSpec) -> np.ndarray:
    if spec.kind == "layer":
        return tensors["last_by_layer"][:, spec.layers[0], :]
    if spec.kind == "final":
        return tensors["final_post_norm"]
    if spec.kind == "concat":
        return np.concatenate([tensors["last_by_layer"][:, layer, :] for layer in spec.layers], axis=-1)
    if spec.kind == "delta":
        if spec.left is None or spec.right is None:
            raise ValueError("delta VectorSpec requires left and right layers.")
        return tensors["last_by_layer"][:, spec.left, :] - tensors["last_by_layer"][:, spec.right, :]
    raise ValueError(f"Unsupported vector spec kind: {spec.kind}")


def evaluate_vectors(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    score_mode: str,
) -> dict[str, Any]:
    predictions = predictions_from_vectors(records, vectors, score_mode=score_mode)
    return evaluate(predictions, skip_abstention=True, bootstrap_samples=200)


def evaluate_transformed(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    transform: str,
    transform_kwargs: dict[str, Any] | None = None,
    global_stats: dict[str, np.ndarray] | None = None,
) -> dict[str, Any]:
    predictions = predictions_from_vectors(
        records,
        vectors,
        score_mode="transformed_cosine",
        transform=transform,
        transform_kwargs=transform_kwargs,
        global_stats=global_stats,
    )
    return evaluate(predictions, skip_abstention=True, bootstrap_samples=200)


def predictions_from_vectors(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    score_mode: str,
    transform: str | None = None,
    transform_kwargs: dict[str, Any] | None = None,
    global_stats: dict[str, np.ndarray] | None = None,
) -> list[Prediction]:
    scored = scored_predictions_from_vectors(
        records,
        vectors,
        score_mode=score_mode,
        transform=transform,
        transform_kwargs=transform_kwargs,
        global_stats=global_stats,
    )
    return [item.prediction for item in scored]


def scored_predictions_from_vectors(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    score_mode: str = "transformed_cosine",
    transform: str | None = None,
    transform_kwargs: dict[str, Any] | None = None,
    global_stats: dict[str, np.ndarray] | None = None,
) -> list[ScoredPrediction]:
    by_instance = group_indices_by_instance(records)
    output = []
    for bucket in by_instance.values():
        query_index = bucket["query"]
        candidate_indices = bucket["candidates"]
        if query_index is None or not candidate_indices:
            continue

        query = vectors[query_index]
        candidates = vectors[candidate_indices]
        candidate_records = [records[index] for index in candidate_indices]
        scores = score_candidates(
            query,
            candidates,
            score_mode=score_mode,
            transform=transform,
            transform_kwargs=transform_kwargs,
            global_stats=global_stats,
        )
        output.append(scored_prediction_from_scores(records[query_index], candidate_records, scores))
    return output


def build_prediction_for_instance(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    score_mode: str,
) -> Prediction | None:
    scored = scored_prediction_for_instance(records, vectors, score_mode)
    return scored.prediction if scored is not None else None


def scored_prediction_for_instance(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    score_mode: str,
) -> ScoredPrediction | None:
    query_record = None
    query_vector = None
    candidate_records = []
    candidate_vectors = []

    for record, vector in zip(records, vectors, strict=True):
        if record["role"] == "query":
            query_record = record
            query_vector = vector
        else:
            candidate_records.append(record)
            candidate_vectors.append(vector)

    if query_record is None or query_vector is None or not candidate_records:
        return None

    scores = score_vectors(query_vector, np.stack(candidate_vectors, axis=0), score_mode)
    return scored_prediction_from_scores(query_record, candidate_records, scores)


def scored_prediction_from_scores(
    query_record: dict[str, Any],
    candidate_records: list[dict[str, Any]],
    scores: np.ndarray,
) -> ScoredPrediction:
    order = np.argsort(scores)[::-1][:50]
    retrieved = [candidate_records[index]["candidate_id"] for index in order]
    gold_mask = np.asarray([bool(record["is_gold"]) for record in candidate_records], dtype=bool)
    gold = [record["candidate_id"] for record in candidate_records if record["is_gold"]]
    prediction = Prediction(
        question_id=query_record["question_id"],
        retrieved_ids=retrieved,
        gold_ids=gold,
        is_abstention="_abs" in query_record["question_id"],
        has_target=bool(gold),
    )
    return ScoredPrediction(
        prediction=prediction,
        query_record=query_record,
        candidate_records=candidate_records,
        candidate_ids=[record["candidate_id"] for record in candidate_records],
        scores=np.asarray(scores, dtype=np.float64),
        gold_mask=gold_mask,
    )


def group_indices_by_instance(records: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    by_instance: dict[int, dict[str, Any]] = {}
    for index, record in enumerate(records):
        bucket = by_instance.setdefault(int(record["instance_index"]), {"query": None, "candidates": []})
        if record["role"] == "query":
            bucket["query"] = index
        else:
            bucket["candidates"].append(index)
    return by_instance


def score_vectors(query: np.ndarray, candidates: np.ndarray, mode: str) -> np.ndarray:
    if mode == "dot":
        return candidates @ query
    if mode == "cosine":
        return normalize(candidates) @ normalize(query)
    if mode == "centered_cosine":
        centered_candidates = candidates - np.mean(candidates, axis=0, keepdims=True)
        centered_query = query - np.mean(candidates, axis=0)
        return normalize(centered_candidates) @ normalize(centered_query)
    raise ValueError(f"Unsupported score mode: {mode}")


def score_candidates(
    query: np.ndarray,
    candidates: np.ndarray,
    score_mode: str,
    transform: str | None,
    transform_kwargs: dict[str, Any] | None,
    global_stats: dict[str, np.ndarray] | None,
) -> np.ndarray:
    if score_mode != "transformed_cosine":
        return score_vectors(query, candidates, score_mode)
    transformed_candidates, transformed_query = apply_transform(
        candidates,
        query,
        transform=transform or "identity",
        transform_kwargs=transform_kwargs or {},
        global_stats=global_stats,
    )
    return normalize(transformed_candidates) @ normalize(transformed_query)


def apply_transform(
    candidates: np.ndarray,
    query: np.ndarray,
    transform: str,
    transform_kwargs: dict[str, Any],
    global_stats: dict[str, np.ndarray] | None,
) -> tuple[np.ndarray, np.ndarray]:
    if transform == "identity":
        return candidates, query
    if transform == "center_instance":
        center = np.mean(candidates, axis=0)
        return candidates - center, query - center
    if transform == "center_candidates_only":
        center = np.mean(candidates, axis=0)
        return candidates - center, query
    if transform == "center_query_only":
        center = np.mean(candidates, axis=0)
        return candidates, query - center
    if transform == "center_global":
        center = require_stats(global_stats, "mean")
        return candidates - center, query - center
    if transform == "zscore_instance":
        mean = np.mean(candidates, axis=0)
        std = np.maximum(np.std(candidates, axis=0), 1e-6)
        return (candidates - mean) / std, (query - mean) / std
    if transform == "zscore_global":
        mean = require_stats(global_stats, "mean")
        std = require_stats(global_stats, "std")
        return (candidates - mean) / std, (query - mean) / std
    if transform == "anti_pca_instance":
        components = int(transform_kwargs["components"])
        center = np.mean(candidates, axis=0)
        centered_candidates = candidates - center
        centered_query = query - center
        pcs = top_pcs_svd(centered_candidates, components)
        return remove_pc_projection(centered_candidates, pcs), remove_pc_projection(centered_query, pcs)
    if transform == "anti_pca_global":
        components = int(transform_kwargs["components"])
        center = require_stats(global_stats, "mean")
        pcs = require_stats(global_stats, "pcs")[:components]
        centered_candidates = candidates - center
        centered_query = query - center
        return remove_pc_projection(centered_candidates, pcs), remove_pc_projection(centered_query, pcs)
    if transform == "anti_pca_global_candidates_only":
        components = int(transform_kwargs["components"])
        center = require_stats(global_stats, "mean")
        pcs = require_stats(global_stats, "pcs")[:components]
        centered_candidates = candidates - center
        return remove_pc_projection(centered_candidates, pcs), query
    if transform == "anti_pca_global_query_only":
        components = int(transform_kwargs["components"])
        center = require_stats(global_stats, "mean")
        pcs = require_stats(global_stats, "pcs")[:components]
        centered_query = query - center
        return candidates, remove_pc_projection(centered_query, pcs)
    if transform == "whitening_global":
        center = require_stats(global_stats, "mean")
        eigvecs = require_stats(global_stats, "eigvecs")
        scales = require_stats(global_stats, "scales")
        keep_dims = int(transform_kwargs["keep_dims"])
        return (
            whiten_vectors(candidates - center, eigvecs, scales, keep_dims),
            whiten_vectors(query - center, eigvecs, scales, keep_dims),
        )
    raise ValueError(f"Unsupported transform: {transform}")


def global_center_stats(records: list[dict[str, Any]], vectors: np.ndarray) -> dict[str, np.ndarray]:
    candidates = candidate_vectors(records, vectors)
    return {"mean": np.mean(candidates, axis=0)}


def global_zscore_stats(records: list[dict[str, Any]], vectors: np.ndarray) -> dict[str, np.ndarray]:
    candidates = candidate_vectors(records, vectors)
    return {
        "mean": np.mean(candidates, axis=0),
        "std": np.maximum(np.std(candidates, axis=0), 1e-6),
    }


def global_anti_pca_stats(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    max_components: int,
) -> dict[str, np.ndarray]:
    candidates = candidate_vectors(records, vectors)
    mean = np.mean(candidates, axis=0)
    pcs = top_pcs_cov(candidates - mean, max_components)
    return {"mean": mean, "pcs": pcs}


def sampled_global_anti_pca_stats(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    max_components: int,
    fraction: float,
    seed: int,
) -> dict[str, np.ndarray]:
    candidates = candidate_vectors(records, vectors)
    if not (0.0 < fraction <= 1.0):
        raise ValueError(f"fraction must be in (0, 1], got {fraction}")
    if fraction < 1.0:
        rng = np.random.default_rng(seed)
        sample_size = max(max_components + 1, int(round(candidates.shape[0] * fraction)))
        sample_size = min(sample_size, candidates.shape[0])
        indices = rng.choice(candidates.shape[0], size=sample_size, replace=False)
        candidates = candidates[indices]
    mean = np.mean(candidates, axis=0)
    pcs = top_pcs_cov(candidates - mean, max_components)
    return {"mean": mean, "pcs": pcs}


def global_whitening_stats(
    records: list[dict[str, Any]],
    vectors: np.ndarray,
    shrinkage: float,
) -> dict[str, np.ndarray]:
    candidates = candidate_vectors(records, vectors)
    mean = np.mean(candidates, axis=0)
    centered = candidates - mean
    covariance = (centered.T @ centered) / max(centered.shape[0] - 1, 1)
    values, eigvecs = np.linalg.eigh(covariance)
    order = np.argsort(values)[::-1]
    values = values[order]
    eigvecs = eigvecs[:, order]
    target = float(np.mean(values))
    shrunk = (1.0 - shrinkage) * values + shrinkage * target
    scales = 1.0 / np.sqrt(np.maximum(shrunk, 1e-6))
    return {
        "mean": mean.astype(np.float32, copy=False),
        "eigvecs": eigvecs.astype(np.float32, copy=False),
        "scales": scales.astype(np.float32, copy=False),
    }


def whiten_vectors(
    vectors: np.ndarray,
    eigvecs: np.ndarray,
    scales: np.ndarray,
    keep_dims: int,
) -> np.ndarray:
    dims = min(keep_dims, eigvecs.shape[1])
    projected = vectors @ eigvecs[:, :dims]
    return projected * scales[:dims]


def candidate_vectors(records: list[dict[str, Any]], vectors: np.ndarray) -> np.ndarray:
    indices = [index for index, record in enumerate(records) if record["role"] != "query"]
    return vectors[indices]


def require_stats(stats: dict[str, np.ndarray] | None, key: str) -> np.ndarray:
    if stats is None or key not in stats:
        raise ValueError(f"Transform requires global_stats[{key!r}].")
    return stats[key]


def top_pcs_svd(centered: np.ndarray, components: int) -> np.ndarray:
    if components <= 0:
        return np.zeros((0, centered.shape[1]), dtype=np.float32)
    _u, _s, vh = np.linalg.svd(centered, full_matrices=False)
    return vh[: min(components, vh.shape[0])].astype(np.float32, copy=False)


def top_pcs_cov(centered: np.ndarray, components: int) -> np.ndarray:
    if components <= 0:
        return np.zeros((0, centered.shape[1]), dtype=np.float32)
    covariance = (centered.T @ centered) / max(centered.shape[0] - 1, 1)
    values, vectors = np.linalg.eigh(covariance)
    order = np.argsort(values)[::-1][:components]
    return vectors[:, order].T.astype(np.float32, copy=False)


def remove_pc_projection(vectors: np.ndarray, pcs: np.ndarray) -> np.ndarray:
    if pcs.size == 0:
        return vectors
    return vectors - (vectors @ pcs.T) @ pcs


def build_rrf_predictions(
    records: list[dict[str, Any]],
    vector_sets: dict[str, np.ndarray],
    rrf_k: float,
) -> list[Prediction]:
    by_instance = group_indices_by_instance(records)
    predictions = []
    for bucket in by_instance.values():
        query_index = bucket["query"]
        candidate_indices = bucket["candidates"]
        if query_index is None or not candidate_indices:
            continue
        candidate_records = [records[index] for index in candidate_indices]
        fused = np.zeros(len(candidate_indices), dtype=np.float64)
        for vectors in vector_sets.values():
            scores = score_candidates(
                vectors[query_index],
                vectors[candidate_indices],
                score_mode="transformed_cosine",
                transform="center_instance",
                transform_kwargs={},
                global_stats=None,
            )
            order = np.argsort(scores)[::-1]
            ranks = np.empty_like(order)
            ranks[order] = np.arange(1, len(order) + 1)
            fused += 1.0 / (rrf_k + ranks)
        predictions.append(scored_prediction_from_scores(records[query_index], candidate_records, fused).prediction)
    return predictions


def tier_a_reference_configs(
    records: list[dict[str, Any]],
    tensors: dict[str, np.ndarray],
) -> dict[str, list[Prediction]]:
    """Build a small stable set of configs for breakdown diagnostics."""
    layer22 = tensors["last_by_layer"][:, 22, :]
    concat = vectors_for_spec(tensors, VectorSpec(name="concat_21_22_23", kind="concat", layers=(21, 22, 23)))
    delta = vectors_for_spec(tensors, VectorSpec(name="delta_22_minus_21", kind="delta", left=22, right=21))
    anti_stats = global_anti_pca_stats(records, layer22, max_components=5)
    return {
        "final_cosine": predictions_from_vectors(records, tensors["final_post_norm"], "cosine"),
        "layer22_center_instance": predictions_from_vectors(
            records, layer22, "transformed_cosine", transform="center_instance"
        ),
        "layer22_zscore_instance": predictions_from_vectors(
            records, layer22, "transformed_cosine", transform="zscore_instance"
        ),
        "layer22_anti_pca_global_k5": predictions_from_vectors(
            records,
            layer22,
            "transformed_cosine",
            transform="anti_pca_global",
            transform_kwargs={"components": 5},
            global_stats=anti_stats,
        ),
        "concat_21_22_23_center_instance": predictions_from_vectors(
            records, concat, "transformed_cosine", transform="center_instance"
        ),
        "delta_22_minus_21_center_instance": predictions_from_vectors(
            records, delta, "transformed_cosine", transform="center_instance"
        ),
    }


def evaluate_predictions_by_question_type(
    predictions: list[Prediction],
    question_types: dict[str, str],
) -> dict[str, Any]:
    grouped: dict[str, list[Prediction]] = {}
    for prediction in predictions:
        grouped.setdefault(question_types.get(prediction.question_id, "unknown"), []).append(prediction)
    output = {}
    for question_type, items in sorted(grouped.items()):
        try:
            output[question_type] = evaluate(items, skip_abstention=True, bootstrap_samples=200)
        except ValueError:
            output[question_type] = {"error": "No scored predictions after filtering."}
    return output


def load_question_types(data_path: Path) -> dict[str, str]:
    return {instance.question_id: instance.question_type for instance in load_instances(data_path)}


def evaluate_by_gold_count(predictions: list[Prediction]) -> dict[str, Any]:
    grouped: dict[str, list[Prediction]] = {"1_gold": [], "2_gold": [], "3plus_gold": []}
    for prediction in predictions:
        count = len(prediction.gold_ids)
        if count <= 0:
            continue
        if count == 1:
            grouped["1_gold"].append(prediction)
        elif count == 2:
            grouped["2_gold"].append(prediction)
        else:
            grouped["3plus_gold"].append(prediction)

    output = {}
    for name, items in grouped.items():
        if not items:
            output[name] = {"n_total": 0}
            continue
        output[name] = {
            "official_metrics": evaluate(
                items,
                skip_abstention=True,
                bootstrap_samples=200,
                ks=(1, 3, 5, 10, 20, 30, 50),
            ),
            "rank_metrics": rank_metrics(items),
        }
    output["all"] = {
        "official_metrics": evaluate(
            predictions,
            skip_abstention=True,
            bootstrap_samples=200,
            ks=(1, 3, 5, 10, 20, 30, 50),
        ),
        "rank_metrics": rank_metrics(predictions),
    }
    return output


def summarize_metric_runs(runs: list[dict[str, Any]]) -> dict[str, Any]:
    recalls = np.asarray([metric_mean(run, "recall_all@5") for run in runs], dtype=np.float64)
    ndcgs = np.asarray([metric_mean(run, "ndcg_any@5") for run in runs], dtype=np.float64)
    return {
        "n_runs": len(runs),
        "recall_all@5_mean": float(np.mean(recalls)),
        "recall_all@5_std": float(np.std(recalls)),
        "ndcg_any@5_mean": float(np.mean(ndcgs)),
        "ndcg_any@5_std": float(np.std(ndcgs)),
        "runs": runs,
    }


def session_metrics_by_gold_count(predictions: list[Prediction]) -> dict[str, Any]:
    grouped: dict[str, list[Prediction]] = {"1_gold": [], "2_gold": [], "3plus_gold": [], "all": []}
    for prediction in predictions:
        count = len(prediction.gold_ids)
        if count <= 0:
            continue
        if count == 1:
            grouped["1_gold"].append(prediction)
        elif count == 2:
            grouped["2_gold"].append(prediction)
        else:
            grouped["3plus_gold"].append(prediction)
        grouped["all"].append(prediction)

    output = {}
    for name, items in grouped.items():
        if not items:
            output[name] = {"n": 0}
            continue
        output[name] = {
            "n": len(items),
            "turn_metrics": evaluate(
                items,
                skip_abstention=True,
                bootstrap_samples=200,
                ks=(1, 3, 5, 10, 20, 30, 50),
            ),
            "session_metrics": session_retrieval_metrics(items),
        }
    return output


def session_retrieval_metrics(predictions: list[Prediction]) -> dict[str, Any]:
    scored = [item for item in predictions if not item.is_abstention and item.has_target and item.gold_ids]
    metrics = {}
    for k in [1, 3, 5, 10, 20, 30, 50]:
        hit_values = []
        recall_all_values = []
        for prediction in scored:
            gold_sessions = {normalize_session_key(gold_id) for gold_id in prediction.gold_ids}
            retrieved_sessions = {
                normalize_session_key(candidate_id)
                for candidate_id in prediction.retrieved_ids[:k]
            }
            hit_values.append(float(bool(gold_sessions & retrieved_sessions)))
            recall_all_values.append(float(gold_sessions.issubset(retrieved_sessions)))
        metrics[f"session_hit@{k}"] = float(np.mean(hit_values)) if hit_values else float("nan")
        metrics[f"session_recall_all@{k}"] = (
            float(np.mean(recall_all_values)) if recall_all_values else float("nan")
        )
    return metrics


def rank_metrics(predictions: list[Prediction]) -> dict[str, Any]:
    scored = [item for item in predictions if not item.is_abstention and item.has_target and item.gold_ids]
    first_hits = []
    reciprocal_ranks = []
    for prediction in scored:
        gold = set(prediction.gold_ids)
        first_position = None
        for index, candidate_id in enumerate(prediction.retrieved_ids, start=1):
            if candidate_id in gold:
                first_position = index
                break
        if first_position is None:
            first_hits.append(">50")
            reciprocal_ranks.append(0.0)
        else:
            first_hits.append(str(first_position))
            reciprocal_ranks.append(1.0 / first_position)

    histogram: dict[str, int] = {}
    for value in first_hits:
        histogram[value] = histogram.get(value, 0) + 1
    return {
        "mrr": float(np.mean(reciprocal_ranks)) if reciprocal_ranks else float("nan"),
        "first_hit_position_histogram": dict(sorted(histogram.items(), key=first_hit_sort_key)),
    }


def first_hit_sort_key(item: tuple[str, int]) -> tuple[int, str]:
    key, _value = item
    if key == ">50":
        return (10_000, key)
    return (int(key), key)


def round_candidate_contexts(data_path: Path) -> dict[str, dict[str, dict[str, Any]]]:
    """Return question_id -> candidate_id -> readable context metadata."""
    contexts: dict[str, dict[str, dict[str, Any]]] = {}
    for instance in load_instances(data_path):
        per_question: dict[str, dict[str, Any]] = {}
        for session_id, session, date in zip(
            instance.haystack_session_ids,
            instance.haystack_sessions,
            instance.haystack_dates,
            strict=True,
        ):
            for turn_index, turn in enumerate(session):
                if turn.get("role") != "user":
                    continue
                candidate_id = f"{session_id}_{turn_index + 1}"
                if "answer" in session_id and not bool(turn.get("has_answer", False)):
                    candidate_id = candidate_id.replace("answer", "noans")
                per_question[candidate_id] = {
                    "text": str(turn.get("content", "")),
                    "date": str(date),
                    "session_key": normalize_session_key(candidate_id),
                }
        contexts[instance.question_id] = per_question
    return contexts


def detailed_error_summary(
    items: list[ScoredPrediction],
    contexts: dict[str, dict[str, dict[str, Any]]],
) -> dict[str, Any]:
    false_positives = []
    same_session_flags = []
    same_day_flags = []
    margins = []
    token_counts = []
    ranks = []
    for item in items:
        prediction = item.prediction
        if prediction.is_abstention or not prediction.has_target:
            continue
        gold_scores = item.scores[item.gold_mask]
        non_gold_scores = item.scores[~item.gold_mask]
        if gold_scores.size == 0 or non_gold_scores.size == 0:
            continue
        margins.append(float(np.max(gold_scores) - np.max(non_gold_scores)))

        order = np.argsort(item.scores)[::-1]
        rank_by_candidate_index = np.empty_like(order)
        rank_by_candidate_index[order] = np.arange(1, len(order) + 1)
        for candidate_index, record in enumerate(item.candidate_records):
            token_counts.append(float(record.get("token_count", 0)))
            ranks.append(float(rank_by_candidate_index[candidate_index]))

        top_index = int(order[0])
        if item.gold_mask[top_index]:
            continue

        q_contexts = contexts.get(prediction.question_id, {})
        top_id = item.candidate_ids[top_index]
        gold_ids = prediction.gold_ids
        top_context = q_contexts.get(top_id, {})
        gold_contexts = [q_contexts.get(gold_id, {}) for gold_id in gold_ids]
        same_session = any(
            top_context.get("session_key") == gold_context.get("session_key")
            for gold_context in gold_contexts
        )
        same_day = any(top_context.get("date") == gold_context.get("date") for gold_context in gold_contexts)
        same_session_flags.append(float(same_session))
        same_day_flags.append(float(same_day))
        false_positives.append(
            {
                "question_id": prediction.question_id,
                "top_candidate_id": top_id,
                "top_candidate_text": str(top_context.get("text", ""))[:100],
                "top_score": float(item.scores[top_index]),
                "gold_candidate_ids": gold_ids,
                "gold_texts": [str(gold_context.get("text", ""))[:100] for gold_context in gold_contexts],
                "best_gold_score": float(np.max(gold_scores)),
                "same_session_as_any_gold": bool(same_session),
                "same_day_as_any_gold": bool(same_day),
            }
        )

    return {
        "gold_margin_best_gold_minus_best_non_gold": summarize_array(np.asarray(margins, dtype=np.float64)),
        "same_session_top1_false_positive_rate": float(np.mean(same_session_flags)) if same_session_flags else float("nan"),
        "same_day_top1_false_positive_rate": float(np.mean(same_day_flags)) if same_day_flags else float("nan"),
        "token_count_vs_rank_spearman": spearman(np.asarray(token_counts), np.asarray(ranks)),
        "top_false_positive_examples": false_positives[:30],
    }


def rerank_prediction_by_top50_bm25(item: ScoredPrediction) -> Prediction:
    top_indices = np.argsort(item.scores)[::-1][:50]
    top_records = [item.candidate_records[index] for index in top_indices]
    query_text = str(item.query_record.get("text", ""))
    query_tokens = simple_tokens(query_text)
    scores = bm25_scores(query_tokens, [str(record.get("text", "")) for record in top_records])
    order = np.argsort(scores)[::-1]
    retrieved = [top_records[index]["candidate_id"] for index in order]
    # Preserve hidden-state order after top-50 rerank candidates to keep metrics
    # at @50 defined exactly as before.
    already = set(retrieved)
    retrieved.extend(candidate_id for candidate_id in item.prediction.retrieved_ids if candidate_id not in already)
    return Prediction(
        question_id=item.prediction.question_id,
        retrieved_ids=retrieved,
        gold_ids=item.prediction.gold_ids,
        is_abstention=item.prediction.is_abstention,
        has_target=item.prediction.has_target,
    )


def fuse_top50_hidden_bm25(item: ScoredPrediction, alpha: float) -> Prediction:
    top_indices = np.argsort(item.scores)[::-1][:50]
    top_records = [item.candidate_records[index] for index in top_indices]
    hidden_scores = item.scores[top_indices]
    query_tokens = simple_tokens(str(item.query_record.get("text", "")))
    bm25 = bm25_scores(query_tokens, [str(record.get("text", "")) for record in top_records])
    fused = alpha * zscore_1d(hidden_scores) + (1.0 - alpha) * zscore_1d(bm25)
    order = np.argsort(fused)[::-1]
    retrieved = [top_records[index]["candidate_id"] for index in order]
    already = set(retrieved)
    retrieved.extend(candidate_id for candidate_id in item.prediction.retrieved_ids if candidate_id not in already)
    return Prediction(
        question_id=item.prediction.question_id,
        retrieved_ids=retrieved,
        gold_ids=item.prediction.gold_ids,
        is_abstention=item.prediction.is_abstention,
        has_target=item.prediction.has_target,
    )


def zscore_1d(values: np.ndarray) -> np.ndarray:
    std = float(np.std(values))
    if std <= 1e-12:
        return np.zeros_like(values, dtype=np.float64)
    return (values - float(np.mean(values))) / std


def simple_tokens(text: str) -> list[str]:
    return [token for token in text.split(" ") if token]


def bm25_scores(query_tokens: list[str], documents: list[str], k1: float = 1.5, b: float = 0.75) -> np.ndarray:
    """Small local BM25 over top-50 documents, avoiding a new runtime dependency."""
    if not query_tokens or not documents:
        return np.zeros(len(documents), dtype=np.float64)
    tokenized = [simple_tokens(document) for document in documents]
    lengths = np.asarray([len(tokens) for tokens in tokenized], dtype=np.float64)
    avgdl = float(np.mean(lengths)) if np.any(lengths) else 1.0
    query_terms = list(dict.fromkeys(query_tokens))
    doc_freq = {
        term: sum(1 for tokens in tokenized if term in set(tokens))
        for term in query_terms
    }
    scores = np.zeros(len(documents), dtype=np.float64)
    n_docs = len(documents)
    for doc_index, tokens in enumerate(tokenized):
        if not tokens:
            continue
        counts = {token: tokens.count(token) for token in set(tokens)}
        norm = k1 * (1.0 - b + b * lengths[doc_index] / max(avgdl, 1e-12))
        for term in query_terms:
            tf = counts.get(term, 0)
            if tf == 0:
                continue
            idf = np.log(1.0 + (n_docs - doc_freq[term] + 0.5) / (doc_freq[term] + 0.5))
            scores[doc_index] += idf * ((tf * (k1 + 1.0)) / (tf + norm))
    return scores


def reference_scored_question_ids(dump_dir: Path, manifest: dict[str, Any]) -> set[str]:
    """Return the non-abstention Tier A question IDs with at least one gold turn."""
    del dump_dir
    by_qid: dict[str, dict[str, bool]] = {}
    for record in manifest["prompts"].values():
        if not record.get("tier_a_file"):
            continue
        qid = str(record["question_id"])
        bucket = by_qid.setdefault(qid, {"has_query": False, "has_gold": False})
        if record["role"] == "query":
            bucket["has_query"] = True
        elif record.get("is_gold"):
            bucket["has_gold"] = True
    return {
        qid
        for qid, flags in by_qid.items()
        if flags["has_query"] and flags["has_gold"] and "_abs" not in qid
    }


def load_available_baseline_predictions(reference_qids: set[str]) -> dict[str, list[Prediction]]:
    candidates = {
        "bm25": find_result_file("bm25"),
        "qwen_embedding": find_result_file("qwen_embedding"),
        "contriever": find_result_file("contriever"),
    }
    output = {}
    for name, path in candidates.items():
        if path is None or not path.exists():
            output[name] = []
            continue
        predictions = load_predictions_from_result(path)
        output[name] = filter_predictions_to_qids(predictions, reference_qids)
    return output


def find_result_file(method: str) -> Path | None:
    exact = ROOT / "results" / f"phase1a_{method}_longmemeval_s_cleaned_round_100.json"
    if exact.exists():
        return exact
    for path in sorted((ROOT / "results").glob(f"phase1a_{method}*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        config = data.get("config", {})
        if (
            str(config.get("data", "")).endswith("longmemeval_s_cleaned.json")
            and config.get("granularity") == "round"
            and config.get("subset") == 100
        ):
            return path
    return None


def load_predictions_from_result(path: Path) -> list[Prediction]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        Prediction(
            question_id=str(item["question_id"]),
            retrieved_ids=[str(value) for value in item["retrieved_ids"]],
            gold_ids=[str(value) for value in item["gold_ids"]],
            is_abstention=bool(item["is_abstention"]),
            has_target=bool(item["has_target"]),
        )
        for item in data.get("predictions", [])
    ]


def filter_predictions_to_qids(predictions: list[Prediction], qids: set[str]) -> list[Prediction]:
    return [
        prediction
        for prediction in predictions
        if isinstance(prediction, Prediction) and prediction.question_id in qids
    ]


def compact_method_metrics(predictions: list[Prediction], bootstrap_samples: int) -> dict[str, Any]:
    valid_predictions = [prediction for prediction in predictions if isinstance(prediction, Prediction)]
    if not valid_predictions:
        return {"error": "No predictions available."}
    turn_metrics = evaluate(
        valid_predictions,
        skip_abstention=True,
        bootstrap_samples=bootstrap_samples,
        ks=(1, 3, 5, 10, 20, 30, 50),
    )
    return {
        "n_predictions": len(valid_predictions),
        "turn_metrics": turn_metrics,
        "session_metrics": session_retrieval_metrics(valid_predictions),
        "rank_metrics": rank_metrics(valid_predictions),
        "summary": {
            "turn_recall_all@5": metric_mean(turn_metrics, "recall_all@5"),
            "turn_recall_all@10": metric_mean(turn_metrics, "recall_all@10"),
            "session_hit@5": session_retrieval_metrics(valid_predictions).get("session_hit@5"),
            "session_recall_all@5": session_retrieval_metrics(valid_predictions).get("session_recall_all@5"),
            "mrr": rank_metrics(valid_predictions).get("mrr"),
        },
    }


def hidden_state_core_predictions(
    records: list[dict[str, Any]],
    tensors: dict[str, np.ndarray],
) -> dict[str, list[Prediction]]:
    layer21 = tensors["last_by_layer"][:, 21, :]
    layer22 = tensors["last_by_layer"][:, 22, :]
    stats21 = global_anti_pca_stats(records, layer21, max_components=10)
    stats22 = global_anti_pca_stats(records, layer22, max_components=10)
    return {
        "hidden_final_cosine": predictions_from_vectors(records, tensors["final_post_norm"], "cosine"),
        "hidden_layer22_center_instance": predictions_from_vectors(
            records,
            layer22,
            "transformed_cosine",
            transform="center_instance",
        ),
        "hidden_layer22_anti_pca_both_k10": predictions_from_vectors(
            records,
            layer22,
            "transformed_cosine",
            transform="anti_pca_global",
            transform_kwargs={"components": 10},
            global_stats=stats22,
        ),
        "hidden_layer22_query_only_anti_pca_k10": predictions_from_vectors(
            records,
            layer22,
            "transformed_cosine",
            transform="anti_pca_global_query_only",
            transform_kwargs={"components": 10},
            global_stats=stats22,
        ),
        "hidden_layer21_query_only_anti_pca_k5": predictions_from_vectors(
            records,
            layer21,
            "transformed_cosine",
            transform="anti_pca_global_query_only",
            transform_kwargs={"components": 5},
            global_stats=stats21,
        ),
    }


def split_stability(configs: dict[str, list[Prediction]], seed: int) -> dict[str, Any]:
    qids = sorted({prediction.question_id for predictions in configs.values() for prediction in predictions})
    rng = np.random.default_rng(seed)
    shuffled = np.asarray(qids, dtype=object)
    rng.shuffle(shuffled)
    midpoint = len(shuffled) // 2
    halves = {
        "first_half": set(str(value) for value in shuffled[:midpoint]),
        "second_half": set(str(value) for value in shuffled[midpoint:]),
    }
    output = {}
    for half_name, half_qids in halves.items():
        rows = {}
        for config_name, predictions in configs.items():
            filtered = filter_predictions_to_qids(predictions, half_qids)
            rows[config_name] = compact_method_metrics(filtered, bootstrap_samples=200)
        output[half_name] = {
            "metrics": rows,
            "rank_by_turn_recall@5": sorted(
                rows,
                key=lambda name: rows[name]["summary"]["turn_recall_all@5"],
                reverse=True,
            ),
        }
    return output


def oracle_prediction_metrics(configs: dict[str, list[Prediction]]) -> dict[str, Any]:
    by_qid: dict[str, list[tuple[str, Prediction]]] = {}
    for name, predictions in configs.items():
        for prediction in predictions:
            by_qid.setdefault(prediction.question_id, []).append((name, prediction))
    selected = []
    selected_config_counts: dict[str, int] = {}
    for qid, candidates in by_qid.items():
        name, prediction = max(candidates, key=lambda item: oracle_sort_key(item[1]))
        selected.append(prediction)
        selected_config_counts[name] = selected_config_counts.get(name, 0) + 1
    return {
        "selected_config_counts": selected_config_counts,
        "metrics": compact_method_metrics(selected, bootstrap_samples=1000),
    }


def oracle_sort_key(prediction: Prediction) -> tuple[float, float, float]:
    return (
        float(all_gold_in_top_k(prediction, 5)),
        float(all_gold_in_top_k(prediction, 10)),
        1.0 / first_gold_position(prediction),
    )


def all_gold_in_top_k(prediction: Prediction, k: int) -> bool:
    if not prediction.gold_ids:
        return False
    return set(prediction.gold_ids).issubset(set(prediction.retrieved_ids[:k]))


def first_gold_position(prediction: Prediction) -> int:
    gold = set(prediction.gold_ids)
    for index, candidate_id in enumerate(prediction.retrieved_ids, start=1):
        if candidate_id in gold:
            return index
    return 10_000


def rank_overlap_jaccard(configs: dict[str, list[Prediction]], k: int) -> dict[str, float]:
    by_config = {
        name: {prediction.question_id: prediction for prediction in predictions}
        for name, predictions in configs.items()
    }
    names = sorted(by_config)
    output = {}
    for left_index, left_name in enumerate(names):
        for right_name in names[left_index + 1 :]:
            shared_qids = sorted(set(by_config[left_name]) & set(by_config[right_name]))
            values = []
            for qid in shared_qids:
                left = set(by_config[left_name][qid].retrieved_ids[:k])
                right = set(by_config[right_name][qid].retrieved_ids[:k])
                union = left | right
                values.append(float(len(left & right) / len(union)) if union else 0.0)
            output[f"{left_name}__vs__{right_name}"] = float(np.mean(values)) if values else float("nan")
    return output


def normalize_session_key(candidate_id: str) -> str:
    session_key = candidate_id.rsplit("_", 1)[0]
    return session_key.replace("noans", "answer")


def spearman(x_values: np.ndarray, y_values: np.ndarray) -> float:
    if x_values.size < 2 or y_values.size < 2:
        return float("nan")
    x_rank = ordinal_ranks(x_values)
    y_rank = ordinal_ranks(y_values)
    x_centered = x_rank - np.mean(x_rank)
    y_centered = y_rank - np.mean(y_rank)
    denom = float(np.linalg.norm(x_centered) * np.linalg.norm(y_centered))
    if denom == 0.0:
        return float("nan")
    return float((x_centered @ y_centered) / denom)


def ordinal_ranks(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values)
    ranks = np.empty_like(order, dtype=np.float64)
    ranks[order] = np.arange(1, values.size + 1, dtype=np.float64)
    return ranks


def summarize_scored_predictions(items: list[ScoredPrediction]) -> dict[str, Any]:
    gold_scores = []
    non_gold_scores = []
    pairwise_win_rates = []
    false_positives = []
    for item in items:
        if item.prediction.is_abstention or not item.prediction.has_target:
            continue
        gold = item.scores[item.gold_mask]
        non_gold = item.scores[~item.gold_mask]
        if gold.size == 0 or non_gold.size == 0:
            continue
        gold_scores.extend(gold.tolist())
        non_gold_scores.extend(non_gold.tolist())
        pairwise_win_rates.append(float(np.mean(gold[:, None] > non_gold[None, :])))
        top_index = int(np.argmax(item.scores))
        if not item.gold_mask[top_index]:
            false_positives.append(
                {
                    "question_id": item.prediction.question_id,
                    "top_candidate_id": item.candidate_ids[top_index],
                    "top_score": float(item.scores[top_index]),
                    "best_gold_score": float(np.max(gold)),
                }
            )
    return {
        "gold_scores": summarize_array(np.asarray(gold_scores, dtype=np.float64)),
        "non_gold_scores": summarize_array(np.asarray(non_gold_scores, dtype=np.float64)),
        "pairwise_gold_beats_non_gold": summarize_array(np.asarray(pairwise_win_rates, dtype=np.float64)),
        "top_false_positive_examples": false_positives[:20],
    }


def suffix_vector(layer_tensor: np.ndarray, pool: str) -> np.ndarray:
    if pool == "last":
        return layer_tensor[-1]
    if pool == "minus2":
        return layer_tensor[-2] if layer_tensor.shape[0] >= 2 else layer_tensor[-1]
    if pool == "minus3":
        return layer_tensor[-3] if layer_tensor.shape[0] >= 3 else layer_tensor[-1]
    if pool == "mean_last3":
        return np.mean(layer_tensor[-min(3, layer_tensor.shape[0]) :], axis=0)
    if pool == "mean_last5":
        return np.mean(layer_tensor[-min(5, layer_tensor.shape[0]) :], axis=0)
    raise ValueError(f"Unsupported suffix pool: {pool}")


def normalize(array: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(array, axis=-1, keepdims=True)
    return array / np.maximum(norms, 1e-12)


def pairwise_cosines(vectors: np.ndarray) -> np.ndarray:
    normalized = normalize(vectors.astype(np.float32))
    matrix = normalized @ normalized.T
    upper = np.triu_indices(matrix.shape[0], k=1)
    return matrix[upper]


def summarize_array(values: np.ndarray) -> dict[str, float]:
    if values.size == 0:
        return {"mean": float("nan"), "std": float("nan"), "min": float("nan"), "max": float("nan")}
    return {
        "mean": float(np.mean(values)),
        "std": float(np.std(values)),
        "min": float(np.min(values)),
        "max": float(np.max(values)),
    }


def top_metric_rows(configs: dict[str, Any], limit: int = 10) -> list[dict[str, float | str]]:
    rows = []
    for name, result in configs.items():
        metrics = result.get("metrics", {})
        recall = metric_mean(result, "recall_all@5")
        ndcg = metric_mean(result, "ndcg_any@5")
        rows.append({"config": name, "recall_all@5": recall, "ndcg_any@5": ndcg, "n_scored": result.get("n_scored", 0)})
    rows.sort(key=lambda row: float(row["recall_all@5"]), reverse=True)
    return rows[:limit]


def metric_mean(result: dict[str, Any], metric_name: str) -> float:
    return float(result.get("metrics", {}).get(metric_name, {}).get("mean", float("nan")))


def write_analysis_result(name: str, result: dict[str, Any]) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result_dir = ROOT / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    json_path = result_dir / f"analysis_{name}_{timestamp}.json"
    md_path = result_dir / f"analysis_{name}_{timestamp}.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown_summary(name, result, json_path), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


def render_markdown_summary(name: str, result: dict[str, Any], json_path: Path) -> str:
    return "\n".join(
        [
            f"# Analysis: {name}",
            "",
            f"Full JSON: `{json_path}`",
            "",
            "This summary is intentionally brief; inspect the JSON for full metrics.",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2)[:4000],
            "```",
            "",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
