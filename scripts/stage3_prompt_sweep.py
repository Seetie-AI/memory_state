"""Stage 3 prompt-variant sweep encoder/evaluator.

This file is a small fork of `stage2_online_eval.py`, not a replacement. The
original script stays untouched so historical README commands and prior Stage 2
results remain reproducible while Stage 3 explores prompt variants for chatbot
memory retrieval.

Design notes for this fork:
- `PROMPT_VARIANTS` contains the approved Stage 3 prompt matrix. P0 remains the
  exact historical suffix and should not be hand-typed in downstream scripts.
- Defaults keep the control variables slightly open around the current 9B best
  point: layers 29/30/31. The default position is `last` only: prior 9B results
  already favored the quote-final state over the colon position, and dropping
  `minus2` halves vector storage for the prompt sweep.
- This script encodes raw hidden-state vectors and keeps the original online
  cosine/centered-cosine sanity metrics. Optionally, `--store-topk-logits K`
  stores final-layer next-token top-K logits as a sparse PromptReps-style audit
  signal without saving full-vocab distributions. Query-only anti-PCA k=2 is an
  offline analysis step because prior results showed it matches the stronger
  both-sided anti-PCA result while keeping candidate vectors reusable.
- BM25 fusion is deliberately excluded from this prompt sweep so prompt effects
  are not diluted by a lexical signal.
- Default outputs live under `tensors/stage3/prompt_sweep/` and
  `results/stage3/prompt_sweep/` to avoid overwriting Stage 2 artifacts.
- LongMemEval is evidence/fact biased; preference/style/pattern prompt variants
  need a caveat when interpreting benchmark results.
- Speed/safety knobs are Stage 3-specific: by default the script keeps a small
  MLX Metal allocation cache and clears it once per text row, not once per
  suffix. This does not delete live prefix KV caches; it only controls reusable
  Metal buffers. Vectors are flushed after every instance, and SIGINT/SIGTERM
  closes the writer so completed chunks are not lost.

Prompt matrix audit notes:
- `1-1_CN` uses `代表` as the Chinese anchor verb because PromptReps found the
  English "represent" wording strong; this tests whether that lesson transfers
  to chatbot memory retrieval.
- The earlier "triggered memory" candidate was deleted because it overlapped
  with free association and was semantically awkward under symmetric encoding:
  an old memory asking what memory it should trigger is not the same as a query
  asking what to retrieve.
- `2-3-2_mem`/`2-3-2_query` is intentionally asymmetric: memory encoding asks
  what should be saved for later recall, while query encoding asks what should
  be recalled now. Query-only anti-PCA keeps this geometry viable by fitting
  candidate-corpus PCs and subtracting them only from query vectors.
- `2-7` uses the Chinese object `互动模式` instead of the borrowed word
  "dynamics" so the object axis does not get confounded with language choice.
- `2-4-1`, `2-4-2`, and `2-8` use `对方` instead of `用户` to avoid importing
  assistant/user product-interface baggage. `2-4-1_user_word` keeps one minimal
  control cell to measure whether the original word choice matters.
- `P0` remains off-matrix as the exact Stage 2 sanity baseline.
- LongMemEval labels evidence needed to answer questions; user-need,
  association, impression, interaction-pattern, and answer-strategy variants
  can only provide hints here and need a future preference/style eval set.
- TODO (separate research track): multi-token memory vectors. Generate N tokens
  with greedy decoding and store trajectory hidden states; combination methods
  include concat / stack matrix / diff. Storage tiers are about 0.57 / 3.4 /
  24 GiB for 1x1x1 / 1x3x2 / 7x3x2 settings; PromptReps found first-token
  strongest on BEIR, but chatbot memory may differ.
"""

from __future__ import annotations

import argparse
import json
import signal
import shutil
import sys
import time
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Any

import mlx.core as mx
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


PROMPT_VARIANTS = {"P0": STAGE2_PROMPT_VARIANTS["P0"]}
# P0 is inherited verbatim from Stage 2 and remains the off-matrix sanity cell.
PROMPT_VARIANTS.update(
    {
        # 1-1_CN: anchor; verb=代表, object=content, language=CN, punctuation=full-width; projects to representation/content space.
        "1-1_CN": "\n用一个词代表上面这段对话，这个词是：“",
        # 1-1_CN_ASCII: punctuation step from anchor; pure ASCII colon+quote for CN text.
        "1-1_CN_ASCII": "\n用一个词代表上面这段对话，这个词是:\"",
        # 1-1_EN: language step from anchor; English/ASCII prompt tests single-token readability pressure.
        "1-1_EN": "\nIn one word, represent the conversation above. The word is:\"",
        # 1-2: verb step from anchor; 概括 vs 代表 tests summarization-style projection.
        "1-2": "\n用一个词概括上面这段对话，这个词是：“",
        # 1-3: verb step from anchor; 标记 vs 代表 tests label/tag-style projection.
        "1-3": "\n用一个词标记上面这段对话，这个词是：“",
        # 2-1: object->topic step from anchor; projects into topic space.
        "2-1": "\n用一个词代表上面这段对话中的话题，这个词是：“",
        # 2-3-1: object->recall-keyword step from anchor; symmetric retrieval-key projection.
        "2-3-1": "\n用一个词代表上面这段对话最该让我想起的关键词，这个词是：“",
        # 2-3-2_mem: asymmetric pair memory side; stores what this memory should recall later.
        "2-3-2_mem": "\n用一个词代表上面这段对话最该让我下次聊到相关话题时想起的关键词，这个词是：“",
        # 2-3-2_query: asymmetric pair query side; asks what current context should retrieve now.
        "2-3-2_query": "\n用一个词代表当前这段对话最该让我回忆起的关键词，这个词是：“",
        # 2-4-1: object->counterparty step from anchor; 对方 is more neutral than 用户 for persona/user-character space.
        "2-4-1": "\n用一个词代表上面这段对话中的对方，这个词是：“",
        # 2-4-1_user_word: minimal A/B control for 2-4-1; keeps 用户 to quantify word-choice drift.
        "2-4-1_user_word": "\n用一个词代表上面这段对话中的用户，这个词是：“",
        # 2-4-2: object->counterparty-need step from anchor; projects into intent/need space without user/app-role baggage.
        "2-4-2": "\n用一个词代表上面这段对话中的对方的需求，这个词是：“",
        # 2-5: object->association step from anchor; projects into free-association/pattern space.
        "2-5": "\n用一个词代表上面这段对话让我产生的联想，这个词是：“",
        # 2-6: object->impression step from anchor; projects into metacognitive impression space.
        "2-6": "\n用一个词代表上面这段对话给我的印象，这个词是：“",
        # 2-7: object->interaction-pattern step from anchor; Chinese replacement for dynamics.
        "2-7": "\n用一个词代表上面这段对话的互动模式，这个词是：“",
        # 2-8: object->answer-strategy step from anchor; 对方 anchors to the transcript counterpart without live-user drift.
        "2-8": "\n用一个词代表回答上面这段对话中的对方时最该采用的策略，这个词是：“",
    }
)
DEFAULT_POSITIONS = ["last"]
ONLINE_SCORE_MODES = ["cosine", "centered_cosine"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--data", default=str(ROOT / "data" / "longmemeval_s_cleaned.json"))
    parser.add_argument("--subset", type=int, default=30)
    parser.add_argument(
        "--subset-start",
        type=int,
        default=0,
        help=(
            "Global LongMemEval instance offset. For multi-machine runs this "
            "must preserve original instance_index values, otherwise merged "
            "vector stores collide on prompt IDs and labels."
        ),
    )
    parser.add_argument("--granularity", choices=["round"], default="round")
    parser.add_argument("--variants", default="1-1_CN")
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
    parser.add_argument(
        "--profile-timing",
        action="store_true",
        help=(
            "Persist coarse runtime timing counters in the result JSON. This is "
            "low overhead and useful for separating prefix prefill, suffix "
            "encoding, vector writing, and online scoring time."
        ),
    )
    parser.add_argument(
        "--store-topk-logits",
        type=int,
        default=0,
        help=(
            "When >0, store final-layer next-token top-K token ids/logits for "
            "each prompt row, variant, and position. Disabled by default because "
            "hidden-vector sweeps do not need logits and full-vocab logits would "
            "be too large."
        ),
    )
    parser.add_argument(
        "--metal-cache-limit-gb",
        type=float,
        default=2.0,
        help=(
            "MLX/Metal reusable cache limit. Stage 3 defaults to 2GB because "
            "the 16GB Mac target has limited headroom; raise cautiously only "
            "after watching active/cache memory stay below the 8GB target."
        ),
    )
    parser.add_argument(
        "--clear-cache-every",
        choices=["suffix", "row", "instance"],
        default="row",
        help=(
            "How often to call mx.metal.clear_cache(). `suffix` preserves the "
            "Stage 2 conservative behavior; `row` reuses Metal allocations "
            "across the 17 short suffix forwards for one text; `instance` is "
            "faster but uses more cache memory."
        ),
    )
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
    topk_logits: int,
) -> int:
    prompt_rows = sum(len(iter_round_candidates(instance)) + 1 for instance in instances)
    vector_bytes = prompt_rows * variant_count * layer_count * position_count * hidden_dim * 2
    logit_bytes = prompt_rows * variant_count * position_count * topk_logits * (4 + 2)
    return int((vector_bytes + logit_bytes) * 1.10)


def check_storage_budget(output_dir: Path, estimated_bytes: int, min_free_gb: float) -> None:
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(output_dir.parent).free
    projected = free - estimated_bytes
    min_free = int(min_free_gb * 1024**3)
    if projected < min_free:
        raise RuntimeError(
            "Stage 3 storage guard refused to start: "
            f"estimated_output={estimated_bytes / 1024**3:.2f}GB, "
            f"current_free={free / 1024**3:.2f}GB, "
            f"projected_free={projected / 1024**3:.2f}GB, "
            f"required_free={min_free_gb:.2f}GB."
        )


def format_duration(seconds: float) -> str:
    seconds_int = max(0, int(seconds))
    minutes, seconds_rem = divmod(seconds_int, 60)
    hours, minutes_rem = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minutes_rem:02d}m{seconds_rem:02d}s"
    if minutes:
        return f"{minutes}m{seconds_rem:02d}s"
    return f"{seconds_rem}s"


class TimingStats:
    """Small aggregate profiler for Stage 3 runs.

    The profiler stores only totals and counts, not per-row details, so it can
    stay enabled during smoke tests without making result JSON large.
    """

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled
        self.seconds: defaultdict[str, float] = defaultdict(float)
        self.counts: defaultdict[str, int] = defaultdict(int)

    def add(self, name: str, elapsed_s: float, count: int = 1) -> None:
        if not self.enabled:
            return
        self.seconds[name] += elapsed_s
        self.counts[name] += count

    def increment(self, name: str, count: int = 1) -> None:
        if not self.enabled:
            return
        self.counts[name] += count

    def summary(self, total_runtime_s: float) -> dict[str, Any]:
        if not self.enabled:
            return {"enabled": False}
        average_seconds = {
            name: self.seconds[name] / self.counts[name]
            for name in self.seconds
            if self.counts[name] > 0
        }
        accounted = sum(self.seconds.values())
        return {
            "enabled": True,
            "total_runtime_s": total_runtime_s,
            "seconds": dict(sorted(self.seconds.items())),
            "counts": dict(sorted(self.counts.items())),
            "average_seconds": dict(sorted(average_seconds.items())),
            "unaccounted_runtime_s": max(0.0, total_runtime_s - accounted),
            "note": (
                "suffix_encode_s includes cache deepcopy, suffix model forward, "
                "optional final-layer logits/top-k, and vector transfer."
            ),
        }


def configure_metal_cache(limit_gb: float) -> None:
    """Set an MLX/Metal reusable-cache cap without changing live tensor limits."""
    if limit_gb <= 0:
        return
    try:
        if hasattr(mx, "set_cache_limit"):
            mx.set_cache_limit(int(limit_gb * 1024**3))
            print(f"MLX cache limit set to {limit_gb:.2f} GiB")
        elif hasattr(mx, "metal") and hasattr(mx.metal, "set_cache_limit"):
            mx.metal.set_cache_limit(int(limit_gb * 1024**3))
            print(f"MLX Metal cache limit set to {limit_gb:.2f} GiB")
        if hasattr(mx, "reset_peak_memory"):
            mx.reset_peak_memory()
        elif hasattr(mx, "metal") and hasattr(mx.metal, "reset_peak_memory"):
            mx.metal.reset_peak_memory()
    except Exception as exc:
        print(f"warning: could not configure MLX Metal cache limit: {exc}")


def metal_memory_summary() -> str:
    """Return active/cache/peak Metal memory for progress logs when available."""
    try:
        if not hasattr(mx, "metal") and not any(
            hasattr(mx, attr)
            for attr in ["get_active_memory", "get_cache_memory", "get_peak_memory"]
        ):
            return "metal_mem unavailable"
        fields = []
        for label, attr in [
            ("active", "get_active_memory"),
            ("cache", "get_cache_memory"),
            ("peak", "get_peak_memory"),
        ]:
            if hasattr(mx, attr):
                value_gib = getattr(mx, attr)() / 1024**3
                fields.append(f"{label} {value_gib:.2f}GiB")
            elif hasattr(mx.metal, attr):
                value_gib = getattr(mx.metal, attr)() / 1024**3
                fields.append(f"{label} {value_gib:.2f}GiB")
        return "metal_mem " + " ".join(fields) if fields else "metal_mem unavailable"
    except Exception as exc:
        return f"metal_mem unavailable ({exc})"


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
    *,
    clear_metal_cache_after_text: bool = True,
    topk_logits: int = 0,
    timing: TimingStats | None = None,
) -> tuple[
    dict[tuple[str, int, str], np.ndarray],
    int,
    dict[tuple[str, str], tuple[np.ndarray, np.ndarray]],
]:
    """Encode all variants for one text while respecting BPE boundaries.

    Stage 3 variants are suffix prompts. They first try to reuse the raw text
    prefix. If BPE merges across the `text + "\n"` boundary, suffix variants
    fall back to a `text + "\n"` prefix and suffix body, while `content_end`
    remains sourced from the raw-text prefix for apples-to-apples diagnostics.
    """
    prefix_started = time.perf_counter()
    text_prefix_state = extractor.prefill_prefix(text, layers, positions)
    if timing is not None:
        timing.add("prefix_prefill_s", time.perf_counter() - prefix_started)
    newline_prefix_state: PrefixState | None = None
    output: dict[tuple[str, int, str], np.ndarray] = {}
    top_logit_output: dict[tuple[str, str], tuple[np.ndarray, np.ndarray]] = {}
    try:
        for variant in variants:
            suffix = PROMPT_VARIANTS[variant]
            try:
                suffix_started = time.perf_counter()
                vectors, top_logits = extractor.encode_suffix_with_logits(
                    text_prefix_state,
                    suffix,
                    layers,
                    positions,
                    topk_logits=topk_logits,
                )
                if timing is not None:
                    timing.add("suffix_encode_s", time.perf_counter() - suffix_started)
                    timing.increment("suffix_forwards")
            except ValueError as exc:
                if not str(exc).startswith("Cannot reuse prefix cache") or not suffix.startswith("\n"):
                    raise
                if newline_prefix_state is None:
                    newline_prefix_started = time.perf_counter()
                    newline_prefix_state = extractor.prefill_prefix(
                        text + "\n",
                        layers,
                        positions,
                    )
                    if timing is not None:
                        timing.add(
                            "newline_prefix_prefill_s",
                            time.perf_counter() - newline_prefix_started,
                        )
                suffix_started = time.perf_counter()
                vectors, top_logits = extractor.encode_suffix_with_logits(
                    newline_prefix_state,
                    suffix[1:],
                    layers,
                    positions,
                    topk_logits=topk_logits,
                )
                if timing is not None:
                    timing.add("suffix_encode_s", time.perf_counter() - suffix_started)
                    timing.increment("suffix_forwards")
                if "content_end" in positions:
                    for layer in layers:
                        source = text_prefix_state.vectors.get((layer, "content_end"))
                        if source is not None:
                            vectors[(layer, "content_end")] = source

            for (layer, position), vector in vectors.items():
                output[(variant, layer, position)] = vector
            for position, top_logit_pair in top_logits.items():
                top_logit_output[(variant, position)] = top_logit_pair
        return output, text_prefix_state.token_count, top_logit_output
    finally:
        cleanup_started = time.perf_counter()
        del text_prefix_state
        if newline_prefix_state is not None:
            del newline_prefix_state
        clear_mlx_memory(clear_metal_cache=clear_metal_cache_after_text)
        if timing is not None:
            timing.add("row_cleanup_s", time.perf_counter() - cleanup_started)


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
        vectors = extractor.encode_suffix(prefix_state, PROMPT_VARIANTS[variant], layers, positions)
        for (layer, position), vector in vectors.items():
            output[(variant, layer, position)] = vector
    return output


def prompt_id(prefix: str, instance_index: int, local_index: int) -> str:
    return f"{prefix}_{instance_index:04d}_{local_index:04d}"


def result_paths(args: argparse.Namespace, model_path: Path) -> tuple[Path, Path]:
    if args.subset and args.subset > 0:
        subset_label = f"{args.subset_start}-{args.subset_start + args.subset}"
    else:
        subset_label = f"{args.subset_start}-full"
    model_label = model_path.name.replace("/", "_")
    variant_label = "-".join(parse_csv(args.variants))
    layer_label = parse_csv(args.layers) if args.layers != "all" else ["all"]
    layer_label_text = "layers_" + "-".join(layer_label)
    position_label_text = "pos_" + "-".join(parse_csv(args.positions))
    run_label = f"{model_label}_{variant_label}_{layer_label_text}_{position_label_text}_{subset_label}"
    vector_dir = (
        Path(args.output_dir)
        if args.output_dir
        else ROOT / "tensors" / "stage3" / "prompt_sweep" / run_label
    )
    result_path = (
        Path(args.result_path)
        if args.result_path
        else ROOT / "results" / "stage3" / "prompt_sweep" / f"{run_label}.json"
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
    all_instances = load_instances(args.data)
    if args.subset_start < 0:
        raise ValueError(f"--subset-start must be >= 0, got {args.subset_start}.")
    if args.subset_start >= len(all_instances):
        raise ValueError(
            f"--subset-start {args.subset_start} is outside dataset length {len(all_instances)}."
        )
    # Keep the original global instance_index. Two machines may encode
    # disjoint slices, and merged stores must not have prompt_id/label collisions.
    indexed_instances = list(enumerate(all_instances))
    if args.subset and args.subset > 0:
        indexed_instances = indexed_instances[args.subset_start : args.subset_start + args.subset]
    else:
        indexed_instances = indexed_instances[args.subset_start :]
    instances = [instance for _global_index, instance in indexed_instances]

    vector_dir, output_path = result_paths(args, model_path)
    estimated_bytes = estimate_output_bytes(
        instances=instances,
        variant_count=len(variants),
        layer_count=len(layers),
        position_count=len(positions),
        hidden_dim=config["hidden_dim"],
        topk_logits=args.store_topk_logits,
    )
    check_storage_budget(vector_dir, estimated_bytes, min_free_gb=args.min_free_gb)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    configure_metal_cache(args.metal_cache_limit_gb)

    writer = Stage2VectorWriter(
        vector_dir,
        model_path=str(model_path),
        tokenizer_path=str(model_path),
        prompt_variants=variants,
        layers=layers,
        positions=positions,
        score_modes_evaluated=ONLINE_SCORE_MODES,
        target_chunk_mb=args.target_chunk_mb,
        topk_logits=args.store_topk_logits,
    )
    clear_metal_on_suffix = args.clear_cache_every == "suffix"
    clear_metal_on_row = args.clear_cache_every == "row"
    clear_metal_on_instance = args.clear_cache_every == "instance"
    extractor = CachedSuffixExtractor(
        str(model_path),
        clear_metal_cache_after_suffix=clear_metal_on_suffix,
    )

    predictions_by_config: dict[str, list[Prediction]] = {}
    skipped_candidates: list[dict[str, Any]] = []
    processed_instances = 0
    total_prompt_rows = sum(len(iter_round_candidates(instance)) + 1 for instance in instances)
    progress_interval = max(total_prompt_rows // 10, 1)
    processed_prompt_rows = 0
    last_progress_report = 0
    start_time = time.monotonic()
    timing = TimingStats(enabled=args.profile_timing)

    def handle_stop(signum: int, _frame: Any) -> None:
        print(f"\nreceived signal {signum}; flushing vectors before exit")
        raise KeyboardInterrupt

    for stop_signal in (signal.SIGINT, signal.SIGTERM):
        signal.signal(stop_signal, handle_stop)

    def report_progress(local_instance_index: int, global_instance_index: int) -> None:
        nonlocal last_progress_report
        if processed_prompt_rows < total_prompt_rows and (
            processed_prompt_rows - last_progress_report < progress_interval
        ):
            return
        elapsed = time.monotonic() - start_time
        rate = processed_prompt_rows / max(elapsed, 1e-9)
        remaining = (total_prompt_rows - processed_prompt_rows) / max(rate, 1e-9)
        print(
            f"processed {processed_prompt_rows}/{total_prompt_rows} prompt rows "
            f"(instance {local_instance_index + 1}/{len(indexed_instances)}, "
            f"global {global_instance_index}) "
            f"elapsed {format_duration(elapsed)} ETA {format_duration(remaining)} "
            f"{metal_memory_summary()}"
        )
        last_progress_report = processed_prompt_rows

    try:
        for local_instance_index, (instance_index, instance) in enumerate(indexed_instances):
            candidates = iter_round_candidates(instance)
            gold_ids = [candidate_id for candidate_id, _text, is_gold in candidates if is_gold]
            active_candidate_ids: list[str] = []
            candidate_vector_maps: list[dict[tuple[str, int, str], np.ndarray]] = []

            for candidate_index, (candidate_id, text, is_gold) in enumerate(candidates):
                try:
                    vectors, token_count, top_logits = encode_variants_for_text(
                        extractor,
                        text,
                        variants,
                        layers,
                        positions,
                        clear_metal_cache_after_text=clear_metal_on_row,
                        topk_logits=args.store_topk_logits,
                        timing=timing,
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
                    clear_mlx_memory(clear_metal_cache=clear_metal_on_row)
                    processed_prompt_rows += 1
                    report_progress(local_instance_index, instance_index)
                    continue

                active_candidate_ids.append(candidate_id)
                candidate_vector_maps.append(vectors)
                writer_started = time.perf_counter()
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
                    top_logits=top_logits,
                )
                timing.add("writer_add_s", time.perf_counter() - writer_started)
                clear_mlx_memory(clear_metal_cache=False)
                processed_prompt_rows += 1
                report_progress(local_instance_index, instance_index)

            query_vectors, query_token_count, query_top_logits = encode_variants_for_text(
                extractor,
                instance.question,
                variants,
                layers,
                positions,
                clear_metal_cache_after_text=clear_metal_on_row,
                topk_logits=args.store_topk_logits,
                timing=timing,
            )
            writer_started = time.perf_counter()
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
                top_logits=query_top_logits,
            )
            timing.add("writer_add_s", time.perf_counter() - writer_started)
            clear_mlx_memory(clear_metal_cache=False)
            processed_prompt_rows += 1
            report_progress(local_instance_index, instance_index)

            scoring_started = time.perf_counter()
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
            timing.add("online_scoring_s", time.perf_counter() - scoring_started)

            processed_instances += 1
            flush_started = time.perf_counter()
            writer.flush_chunk()
            timing.add("writer_flush_s", time.perf_counter() - flush_started)
            if clear_metal_on_instance:
                clear_mlx_memory(clear_metal_cache=True)
    finally:
        writer.close()
        del extractor
        clear_mlx_memory(clear_metal_cache=True)

    metrics_by_config = {
        config_key: evaluate(
            predictions,
            skip_abstention=True,
            bootstrap_samples=args.bootstrap_samples,
        )
        for config_key, predictions in predictions_by_config.items()
    }
    total_runtime_s = time.monotonic() - start_time

    payload = {
        "stage": "stage3_prompt_sweep",
        "config": {
            "model_path": str(model_path),
            "data": args.data,
            "subset_start": args.subset_start,
            "subset": args.subset,
            "selected_instance_indices": [index for index, _instance in indexed_instances],
            "variants": variants,
            "layers": layers,
            "positions": positions,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "vector_dir": str(vector_dir),
            "estimated_vector_output_gb": estimated_bytes / 1024**3,
            "score_modes": ONLINE_SCORE_MODES,
            "metal_cache_limit_gb": args.metal_cache_limit_gb,
            "clear_cache_every": args.clear_cache_every,
            "store_topk_logits": args.store_topk_logits,
            "profile_timing": args.profile_timing,
        },
        "profile_timing": timing.summary(total_runtime_s),
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

    print("\nStage 3 prompt sweep complete")
    print(f"instances: {processed_instances}")
    print(f"vector_dir: {vector_dir}")
    print(f"result file: {output_path}")
    if args.profile_timing:
        summary = timing.summary(total_runtime_s)
        print("timing summary:")
        for name, seconds in summary["seconds"].items():
            count = summary["counts"].get(name, 0)
            average = summary["average_seconds"].get(name)
            if average is None:
                print(f"  {name}: {format_duration(seconds)}")
            else:
                print(f"  {name}: {format_duration(seconds)} total / {average:.3f}s avg over {count}")
    print("top configs by Recall@5:")
    for recall5, ndcg5, config_key in top_rows[:10]:
        print(f"  {recall5:.3f} R@5 / {ndcg5:.3f} NDCG@5 :: {config_key}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
