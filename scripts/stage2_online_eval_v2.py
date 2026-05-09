"""Stage 2 prompt-variant exploration fork.

This file is a small fork of `stage2_online_eval.py`, not a replacement. The
original script stays untouched so historical README commands and prior Stage 2
results remain reproducible while this fork changes only prompt-sweep defaults.

Design notes for this fork:
- Prompt content is intentionally not redesigned here; future variants should be
  added to `PROMPT_VARIANTS` after the prompt discussion. P0 remains the exact
  historical suffix and should not be hand-typed in downstream scripts.
- Defaults keep the control variables slightly open around the current 9B best
  point: layers 29/30/31 and positions `last,minus2`.
- This script only encodes raw hidden-state vectors and keeps the original
  online cosine/centered-cosine sanity metrics. Query-only anti-PCA k=2 is an
  offline analysis step because prior results showed it matches the stronger
  both-sided anti-PCA result while keeping candidate vectors reusable.
- BM25 fusion is deliberately excluded from this prompt sweep so prompt effects
  are not diluted by a lexical signal.
- Default outputs live under `tensors/stage3_prompt_sweep/` and
  `results/stage3_prompt_sweep_*` to avoid overwriting Stage 2 artifacts.
- LongMemEval is evidence/fact biased; preference/style/pattern prompt variants
  need a caveat when interpreting benchmark results.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from eval.longmemeval_metrics import Prediction, evaluate
from hidden_state.cached_suffix_extractor import (
    CachedSuffixExtractor,
    PrefixState,
    clear_mlx_memory,
)
from longmemeval.data import (
    has_round_side_answer_label,
    iter_round_candidates,
    load_instances,
)
from stage2.vector_store import PromptMetadata, Stage2VectorWriter
from stage2_online_eval import PROMPT_VARIANTS as STAGE2_PROMPT_VARIANTS


PROMPT_VARIANTS = dict(STAGE2_PROMPT_VARIANTS)
DEFAULT_POSITIONS = ["last", "minus2"]
ONLINE_SCORE_MODES = ["cosine", "centered_cosine"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--data", default=str(ROOT / "data" / "longmemeval_s_cleaned.json"))
    parser.add_argument("--subset", type=int, default=30)
    parser.add_argument("--granularity", choices=["round"], default="round")
    parser.add_argument("--variants", default="P0")
    parser.add_argument(
        "--layers",
        default="29,30,31",
        help="Layer list/ranges, e.g. all, 0-23, 20-23, 0,8,16,24-31.",
    )
    parser.add_argument("--positions", default=",".join(DEFAULT_POSITIONS))
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--target-chunk-mb", type=int, default=512)
    parser.add_argument("--min-free-gb", type=float, default=20.0)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--result-path", default=None)
    return parser.parse_args()


def parse_layers(spec: str, num_layers: int) -> list[int]:
    if spec == "all":
        return list(range(num_layers))
    output: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            left, right = part.split("-", 1)
            output.extend(range(int(left), int(right) + 1))
        else:
            output.append(int(part))
    resolved = []
    for layer in output:
        value = layer if layer >= 0 else num_layers + layer
        if value < 0 or value >= num_layers:
            raise ValueError(f"Layer {layer} resolves to {value}, outside [0, {num_layers - 1}].")
        if value not in resolved:
            resolved.append(value)
    if not resolved:
        raise ValueError("No layers selected.")
    return resolved


def parse_csv(spec: str) -> list[str]:
    values = [part.strip() for part in spec.split(",") if part.strip()]
    if not values:
        raise ValueError(f"Empty CSV spec: {spec!r}")
    return values


def model_config(model_path: Path) -> dict[str, int]:
    config_path = model_path / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing model config: {config_path}")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    text_config = config.get("text_config", config)
    return {
        "num_layers": int(text_config["num_hidden_layers"]),
        "hidden_dim": int(text_config["hidden_size"]),
    }


def estimate_output_bytes(
    instances: list[Any],
    variant_count: int,
    layer_count: int,
    position_count: int,
    hidden_dim: int,
) -> int:
    prompt_rows = sum(len(iter_round_candidates(instance)) + 1 for instance in instances)
    return int(prompt_rows * variant_count * layer_count * position_count * hidden_dim * 2 * 1.10)


def check_storage_budget(output_dir: Path, estimated_bytes: int, min_free_gb: float) -> None:
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(output_dir.parent).free
    projected = free - estimated_bytes
    min_free = int(min_free_gb * 1024**3)
    if projected < min_free:
        raise RuntimeError(
            "Stage 2 storage guard refused to start: "
            f"estimated_output={estimated_bytes / 1024**3:.2f}GB, "
            f"current_free={free / 1024**3:.2f}GB, "
            f"projected_free={projected / 1024**3:.2f}GB, "
            f"required_free={min_free_gb:.2f}GB."
        )


def l2_normalize(vector: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if norm == 0.0 or not np.isfinite(norm):
        raise ValueError("Cannot normalize zero/non-finite vector.")
    return vector / norm


def l2_normalize_matrix(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(norms == 0.0) or not np.all(np.isfinite(norms)):
        raise ValueError("Cannot normalize matrix with zero/non-finite rows.")
    return matrix / norms


def rank_vectors(
    candidate_ids: list[str],
    candidate_vectors: list[np.ndarray],
    query_vector: np.ndarray,
    score_mode: str,
    top_k: int,
) -> list[str]:
    matrix = np.stack(candidate_vectors, axis=0).astype(np.float32)
    query = np.asarray(query_vector, dtype=np.float32)
    if not np.all(np.isfinite(matrix)) or not np.all(np.isfinite(query)):
        raise ValueError("Non-finite vector in ranking input.")

    if score_mode == "cosine":
        scores = l2_normalize_matrix(matrix) @ l2_normalize(query)
    elif score_mode == "centered_cosine":
        mean = np.mean(matrix, axis=0)
        scores = l2_normalize_matrix(matrix - mean) @ l2_normalize(query - mean)
    else:
        raise ValueError(f"Unsupported score mode: {score_mode}")

    order = np.argsort(-scores)[:top_k]
    return [candidate_ids[int(index)] for index in order]


def encode_variants_for_text(
    extractor: CachedSuffixExtractor,
    text: str,
    variants: list[str],
    layers: list[int],
    positions: list[str],
) -> tuple[dict[tuple[str, int, str], np.ndarray], int]:
    """Encode all variants for one text while respecting BPE boundaries.

    P1/no-suffix uses the raw text prefix. Suffix variants first try to reuse
    that same prefix. If BPE merges across the `text + "\n"` boundary, suffix
    variants fall back to a `text + "\n"` prefix and suffix body, while
    `content_end` remains sourced from the raw-text prefix for apples-to-apples
    diagnostics.
    """
    text_prefix_state = extractor.prefill_prefix(text, layers, positions)
    newline_prefix_state: PrefixState | None = None
    output: dict[tuple[str, int, str], np.ndarray] = {}
    try:
        for variant in variants:
            if variant == "P1":
                vectors = extractor.encode_no_suffix(text_prefix_state, layers, positions)
            else:
                suffix = PROMPT_VARIANTS[variant]
                try:
                    vectors = extractor.encode_suffix(text_prefix_state, suffix, layers, positions)
                except ValueError as exc:
                    if not str(exc).startswith("Cannot reuse prefix cache") or not suffix.startswith("\n"):
                        raise
                    if newline_prefix_state is None:
                        newline_prefix_state = extractor.prefill_prefix(
                            text + "\n",
                            layers,
                            positions,
                        )
                    vectors = extractor.encode_suffix(
                        newline_prefix_state,
                        suffix[1:],
                        layers,
                        positions,
                    )
                    if "content_end" in positions:
                        for layer in layers:
                            source = text_prefix_state.vectors.get((layer, "content_end"))
                            if source is not None:
                                vectors[(layer, "content_end")] = source

            for (layer, position), vector in vectors.items():
                output[(variant, layer, position)] = vector
        return output, text_prefix_state.token_count
    finally:
        del text_prefix_state
        if newline_prefix_state is not None:
            del newline_prefix_state
        clear_mlx_memory()


def encode_variants(
    extractor: CachedSuffixExtractor,
    prefix_state: PrefixState,
    variants: list[str],
    layers: list[int],
    positions: list[str],
) -> dict[tuple[str, int, str], np.ndarray]:
    """Deprecated compatibility wrapper; prefer encode_variants_for_text."""
    output: dict[tuple[str, int, str], np.ndarray] = {}
    for variant in variants:
        if variant == "P1":
            vectors = extractor.encode_no_suffix(prefix_state, layers, positions)
        else:
            vectors = extractor.encode_suffix(prefix_state, PROMPT_VARIANTS[variant], layers, positions)
        for (layer, position), vector in vectors.items():
            output[(variant, layer, position)] = vector
    return output


def prompt_id(prefix: str, instance_index: int, local_index: int) -> str:
    return f"{prefix}_{instance_index:04d}_{local_index:04d}"


def result_paths(args: argparse.Namespace, model_path: Path) -> tuple[Path, Path]:
    subset_label = args.subset if args.subset and args.subset > 0 else "full"
    model_label = model_path.name.replace("/", "_")
    variant_label = "-".join(parse_csv(args.variants))
    layer_label = parse_csv(args.layers) if args.layers != "all" else ["all"]
    layer_label_text = "layers_" + "-".join(layer_label)
    position_label_text = "pos_" + "-".join(parse_csv(args.positions))
    run_label = f"{model_label}_{variant_label}_{layer_label_text}_{position_label_text}_{subset_label}"
    vector_dir = (
        Path(args.output_dir)
        if args.output_dir
        else ROOT / "tensors" / "stage3_prompt_sweep" / run_label
    )
    result_path = (
        Path(args.result_path)
        if args.result_path
        else ROOT / "results" / f"stage3_prompt_sweep_{run_label}.json"
    )
    return vector_dir, result_path


def main() -> int:
    args = parse_args()
    model_path = Path(args.model_path)
    variants = parse_csv(args.variants)
    unsupported = [variant for variant in variants if variant not in PROMPT_VARIANTS]
    if unsupported:
        raise ValueError(f"Unsupported prompt variants: {unsupported}")

    config = model_config(model_path)
    layers = parse_layers(args.layers, num_layers=config["num_layers"])
    positions = parse_csv(args.positions)
    instances = load_instances(args.data)
    if args.subset and args.subset > 0:
        instances = instances[: args.subset]

    vector_dir, output_path = result_paths(args, model_path)
    estimated_bytes = estimate_output_bytes(
        instances=instances,
        variant_count=len(variants),
        layer_count=len(layers),
        position_count=len(positions),
        hidden_dim=config["hidden_dim"],
    )
    check_storage_budget(vector_dir, estimated_bytes, min_free_gb=args.min_free_gb)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    writer = Stage2VectorWriter(
        vector_dir,
        model_path=str(model_path),
        tokenizer_path=str(model_path),
        prompt_variants=variants,
        layers=layers,
        positions=positions,
        score_modes_evaluated=ONLINE_SCORE_MODES,
        target_chunk_mb=args.target_chunk_mb,
    )
    extractor = CachedSuffixExtractor(str(model_path))

    predictions_by_config: dict[str, list[Prediction]] = {}
    skipped_candidates: list[dict[str, Any]] = []
    processed_instances = 0

    try:
        for instance_index, instance in enumerate(instances):
            candidates = iter_round_candidates(instance)
            gold_ids = [candidate_id for candidate_id, _text, is_gold in candidates if is_gold]
            active_candidate_ids: list[str] = []
            candidate_vector_maps: list[dict[tuple[str, int, str], np.ndarray]] = []

            for candidate_index, (candidate_id, text, is_gold) in enumerate(candidates):
                try:
                    vectors, token_count = encode_variants_for_text(
                        extractor,
                        text,
                        variants,
                        layers,
                        positions,
                    )
                except ValueError as exc:
                    if "no prefix tokens" not in str(exc).lower():
                        raise
                    skipped_candidates.append(
                        {
                            "instance_index": instance_index,
                            "question_id": instance.question_id,
                            "candidate_index": candidate_index,
                            "candidate_id": candidate_id,
                            "is_gold": bool(is_gold),
                            "reason": "empty_prefix",
                        }
                    )
                    print(
                        "warning: skipped empty-prefix candidate "
                        f"{candidate_id} in {instance.question_id}"
                    )
                    clear_mlx_memory()
                    continue

                active_candidate_ids.append(candidate_id)
                candidate_vector_maps.append(vectors)
                writer.add(
                    PromptMetadata(
                        prompt_id=prompt_id("cand", instance_index, candidate_index),
                        instance_index=instance_index,
                        question_id=instance.question_id,
                        role="candidate",
                        candidate_id=candidate_id,
                        is_gold=bool(is_gold),
                        token_count=token_count,
                        resolved_positions={position: None for position in positions},
                    ),
                    vectors,
                )
                clear_mlx_memory()

            query_vectors, query_token_count = encode_variants_for_text(
                extractor,
                instance.question,
                variants,
                layers,
                positions,
            )
            writer.add(
                PromptMetadata(
                    prompt_id=prompt_id("query", instance_index, 0),
                    instance_index=instance_index,
                    question_id=instance.question_id,
                    role="query",
                    candidate_id=None,
                    is_gold=False,
                    token_count=query_token_count,
                    resolved_positions={position: None for position in positions},
                ),
                query_vectors,
            )
            clear_mlx_memory()

            for variant in variants:
                for layer in layers:
                    for position in positions:
                        vector_key = (variant, layer, position)
                        if vector_key not in query_vectors:
                            continue
                        if any(vector_key not in vectors for vectors in candidate_vector_maps):
                            continue
                        if not active_candidate_ids:
                            continue

                        candidate_vectors = [vectors[vector_key] for vectors in candidate_vector_maps]
                        for score_mode in ONLINE_SCORE_MODES:
                            config_key = f"{variant}|layer{layer}|{position}|{score_mode}"
                            retrieved = rank_vectors(
                                active_candidate_ids,
                                candidate_vectors,
                                query_vectors[vector_key],
                                score_mode=score_mode,
                                top_k=args.top_k,
                            )
                            predictions_by_config.setdefault(config_key, []).append(
                                Prediction(
                                    question_id=instance.question_id,
                                    retrieved_ids=retrieved,
                                    gold_ids=gold_ids,
                                    is_abstention=instance.is_abstention,
                                    has_target=has_round_side_answer_label(instance),
                                )
                            )

            processed_instances += 1
            if processed_instances % 5 == 0:
                writer.flush_chunk()
                clear_mlx_memory()
                print(f"processed {processed_instances}/{len(instances)} instances")
    finally:
        writer.close()
        del extractor
        clear_mlx_memory()

    metrics_by_config = {
        config_key: evaluate(
            predictions,
            skip_abstention=True,
            bootstrap_samples=args.bootstrap_samples,
        )
        for config_key, predictions in predictions_by_config.items()
    }

    payload = {
        "stage": "stage2_online_eval_v2",
        "config": {
            "model_path": str(model_path),
            "data": args.data,
            "subset": args.subset,
            "variants": variants,
            "layers": layers,
            "positions": positions,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "vector_dir": str(vector_dir),
            "estimated_vector_output_gb": estimated_bytes / 1024**3,
            "score_modes": ONLINE_SCORE_MODES,
        },
        "skipped_candidates": skipped_candidates,
        "skipped_candidate_count": len(skipped_candidates),
        "metrics_by_config": metrics_by_config,
        "predictions_by_config": {
            config_key: [asdict(prediction) for prediction in predictions]
            for config_key, predictions in predictions_by_config.items()
        },
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    top_rows = []
    for config_key, metrics in metrics_by_config.items():
        recall5 = metrics["metrics"]["recall_all@5"]["mean"]
        ndcg5 = metrics["metrics"]["ndcg_any@5"]["mean"]
        top_rows.append((recall5, ndcg5, config_key))
    top_rows.sort(reverse=True)

    print("\nStage 2 prompt sweep v2 online eval complete")
    print(f"instances: {processed_instances}")
    print(f"vector_dir: {vector_dir}")
    print(f"result file: {output_path}")
    print("top configs by Recall@5:")
    for recall5, ndcg5, config_key in top_rows[:10]:
        print(f"  {recall5:.3f} R@5 / {ndcg5:.3f} NDCG@5 :: {config_key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
