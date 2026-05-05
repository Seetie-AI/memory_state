"""Stage 2 Step 1.5: verify KV-cache suffix reuse matches full forward.

Why: notes/stage_2_plan.md Step 1.5 gates the Stage 2 prompt sweep. Prompt
variants share the same candidate prefix, so cache reuse can save most of the
forward work, but Qwen3.5 uses a hybrid cache (`ArraysCache` for linear
attention layers and `KVCache` for full-attention layers). This script uses
the model-provided `make_cache()` path and compares cached suffix vectors
against full-forward vectors before any retrieval metrics rely on caching.

The script also checks tokenizer boundary compositionality. If
encode(text + suffix) is not representable as a cached prefix token sequence
plus suffix token sequence, the cached path is not a valid replacement for
full prompt evaluation.
"""

from __future__ import annotations

import copy
import gc
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mlx.core as mx
import numpy as np
from mlx_lm.models.base import create_attention_mask, create_ssm_mask

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hidden_state.mlx_wrapper import MLXHiddenStateExtractor


BF16_MODEL = ROOT / "models" / "Qwen3.5-2B-bf16"
FOUR_BIT_MODEL = ROOT / "models" / "Qwen3.5-2B-MLX-4bit"
RESULT_PATH = ROOT / "results" / "stage2_step1_5_kv_cache_smoke.json"
TARGET_LAYER_INDEX = 22
PASS_THRESHOLD = 0.998
FAIL_THRESHOLD = 0.99


PROMPT_VARIANTS = {
    "P0": "\n请用一个词来summarize上面这段文字，这个词是：“",
    "P4": "\n用于记忆检索的关键词是：",
    "P5": "\nMemory key:",
}


@dataclass(frozen=True)
class TokenSplit:
    full_tokens: list[int]
    prefix_tokens: list[int]
    suffix_tokens: list[int]
    mode: str


@dataclass(frozen=True)
class ForwardResult:
    vector: np.ndarray
    top_token_ids: list[int]
    top_token_texts: list[str]


def build_texts() -> list[str]:
    return [
        "用户说早餐通常喝无糖拿铁，周末会加一块蓝莓司康。",
        "The warranty expires in August and the receipt is stored in email.",
        "会议记录：Alice 负责清洗数据，Ben 负责把评估脚本接到 CI。",
        "旅行偏好：住在车站附近，不要太吵，房间可以小但必须干净。",
        "The cache bug appears only after the models directory is moved.",
        "孩子最近迷上天文学，尤其问了很多关于木星和月食的问题。",
        "用户写作偏好：不要夸张，不要鸡汤，多给清晰的下一步。",
        "Dinner preference: avoid cilantro, mild spice is fine, and clear soup is preferred.",
        "研究计划比较 BM25、Qwen embedding 和 LLM hidden-state retrieval。",
        "A support thread says login failure happens only when third-party cookies are disabled.",
    ]


def clear_mlx_memory() -> None:
    gc.collect()
    try:
        if hasattr(mx, "metal") and hasattr(mx.metal, "clear_cache"):
            mx.metal.clear_cache()
    except Exception:
        pass


def cosine(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.dot(left, right) / ((np.linalg.norm(left) * np.linalg.norm(right)) + 1e-12))


def topk_jaccard(left: list[int], right: list[int], k: int = 5) -> float:
    left_set = set(left[:k])
    right_set = set(right[:k])
    return len(left_set & right_set) / max(len(left_set | right_set), 1)


def l2_normalize(vector: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if norm == 0.0 or not np.isfinite(norm):
        raise ValueError("Cannot normalize zero/non-finite vector.")
    return vector / norm


def split_tokens_for_cache(tokenizer: Any, text: str, suffix: str) -> TokenSplit:
    """Find an exact token split for full prompt = cached prefix + suffix.

    BPE tokenization may merge characters across a text/suffix boundary. For
    suffixes that begin with a newline, we also try caching `text + "\n"` and
    running only the suffix body. If neither split is token-prefix exact, cache
    reuse would compare a different token sequence and must fail loudly.
    """
    full_tokens = tokenizer.encode(text + suffix)
    attempts: list[tuple[str, list[int]]] = [("text", tokenizer.encode(text))]
    if suffix.startswith("\n"):
        attempts.append(("text_plus_newline", tokenizer.encode(text + "\n")))

    for mode, prefix_tokens in attempts:
        if full_tokens[: len(prefix_tokens)] == prefix_tokens:
            suffix_tokens = full_tokens[len(prefix_tokens) :]
            if suffix_tokens:
                return TokenSplit(
                    full_tokens=full_tokens,
                    prefix_tokens=prefix_tokens,
                    suffix_tokens=suffix_tokens,
                    mode=mode,
                )

    raise ValueError(
        "Cannot split prompt tokens exactly for cache reuse. "
        f"text={text[:80]!r}, suffix={suffix!r}, full_len={len(full_tokens)}, "
        f"attempt_prefix_lens={[len(tokens) for _, tokens in attempts]}"
    )


def make_model_cache(extractor: MLXHiddenStateExtractor) -> list[Any]:
    """Use mlx-lm's own cache constructor for Qwen3.5 hybrid cache layouts."""
    if hasattr(extractor.model, "make_cache"):
        return extractor.model.make_cache()
    if hasattr(extractor.model, "language_model") and hasattr(
        extractor.model.language_model, "make_cache"
    ):
        return extractor.model.language_model.make_cache()
    raise TypeError("Loaded model does not expose make_cache().")


def cache_subset(cache: list[Any], indices: int | list[int]) -> Any:
    if isinstance(indices, int):
        return cache[indices]
    return [cache[index] for index in indices]


def resolve_layer_index(extractor: MLXHiddenStateExtractor, layer_index: int) -> int:
    layer_count = extractor.num_layers
    if layer_count is None:
        raise TypeError("Cannot resolve layer index without base_model.layers.")
    resolved = layer_index if layer_index >= 0 else layer_count + layer_index
    if resolved < 0 or resolved >= layer_count:
        raise ValueError(f"Layer {layer_index} resolves to {resolved}, outside {layer_count}.")
    return resolved


def forward_target_from_tokens(
    extractor: MLXHiddenStateExtractor,
    token_ids: list[int],
    cache: list[Any] | None,
    target_layer_index: int,
) -> ForwardResult:
    """Forward token_ids and return the target-layer suffix-end vector.

    This mirrors MLXHiddenStateExtractor._forward_with_target_layer but accepts
    a caller-supplied cache so the cached suffix path can be compared against
    the full prompt path.
    """
    if not token_ids:
        raise ValueError("Cannot forward an empty token sequence.")

    layers = getattr(extractor.base_model, "layers", None)
    if not layers:
        raise TypeError("Target-layer KV smoke requires base_model.layers.")
    if cache is None:
        cache = [None] * len(layers)
    if len(cache) != len(layers):
        raise ValueError(f"Cache length {len(cache)} != layer count {len(layers)}.")

    target = resolve_layer_index(extractor, target_layer_index)
    input_ids = mx.array([token_ids], dtype=mx.int32)
    hidden_states = extractor.base_model.embed_tokens(input_ids)
    fa_mask = create_attention_mask(
        hidden_states,
        cache_subset(cache, extractor.base_model.fa_idx),
    )
    ssm_mask = create_ssm_mask(
        hidden_states,
        cache_subset(cache, extractor.base_model.ssm_idx),
    )

    selected = None
    for index, (layer, layer_cache) in enumerate(zip(layers, cache, strict=True)):
        mask = ssm_mask if layer.is_linear else fa_mask
        hidden_states = layer(hidden_states, mask, layer_cache)
        if index == target:
            selected = hidden_states[:, -1, :].astype(mx.float32)

    if selected is None:
        raise RuntimeError(f"Target layer {target} was not reached.")

    final_hidden = extractor.base_model.norm(hidden_states)
    logits = extractor._project_logits(final_hidden)[:, -1, :]
    top_indices = mx.argsort(logits, axis=-1)[:, -5:][:, ::-1]
    mx.eval(selected, top_indices)

    vector = l2_normalize(np.array(selected[0], dtype=np.float32))
    top_ids = [int(value) for value in np.asarray(top_indices[0]).tolist()]
    top_texts = [extractor.tokenizer.decode([token_id]) for token_id in top_ids]
    return ForwardResult(vector=vector, top_token_ids=top_ids, top_token_texts=top_texts)


def prefill_prefix_cache(
    extractor: MLXHiddenStateExtractor,
    prefix_tokens: list[int],
) -> list[Any]:
    """Run the prefix once and return a populated model-provided cache."""
    cache = make_model_cache(extractor)
    input_ids = mx.array([prefix_tokens], dtype=mx.int32)
    hidden = extractor.base_model(input_ids, cache=cache)
    mx.eval(hidden)
    return cache


def run_model_smoke(model_path: Path) -> dict[str, Any]:
    print(f"Loading {model_path}")
    extractor = MLXHiddenStateExtractor(str(model_path), dtype_note="mlx")
    texts = build_texts()
    rows: list[dict[str, Any]] = []

    try:
        cache_classes = [type(cache).__name__ for cache in make_model_cache(extractor)]
        for text_index, text in enumerate(texts, start=1):
            for variant_id, suffix in PROMPT_VARIANTS.items():
                split = split_tokens_for_cache(extractor.tokenizer, text, suffix)
                full = forward_target_from_tokens(
                    extractor,
                    split.full_tokens,
                    cache=None,
                    target_layer_index=TARGET_LAYER_INDEX,
                )
                prefix_cache = prefill_prefix_cache(extractor, split.prefix_tokens)
                suffix_cache = copy.deepcopy(prefix_cache)
                cached = forward_target_from_tokens(
                    extractor,
                    split.suffix_tokens,
                    cache=suffix_cache,
                    target_layer_index=TARGET_LAYER_INDEX,
                )
                hidden_cosine = cosine(full.vector, cached.vector)
                rows.append(
                    {
                        "text_index": text_index,
                        "variant_id": variant_id,
                        "split_mode": split.mode,
                        "full_token_count": len(split.full_tokens),
                        "prefix_token_count": len(split.prefix_tokens),
                        "suffix_token_count": len(split.suffix_tokens),
                        "hidden_cosine": hidden_cosine,
                        "top5_token_jaccard": topk_jaccard(full.top_token_ids, cached.top_token_ids),
                        "full_top5": full.top_token_texts,
                        "cached_top5": cached.top_token_texts,
                    }
                )
                del prefix_cache, suffix_cache
                clear_mlx_memory()
    finally:
        del extractor
        clear_mlx_memory()

    cosines = np.asarray([row["hidden_cosine"] for row in rows], dtype=np.float64)
    status = "go"
    if float(cosines.min()) < FAIL_THRESHOLD:
        status = "no_go"
    elif float(cosines.min()) < PASS_THRESHOLD:
        status = "warning"

    return {
        "model_path": str(model_path),
        "target_layer_index": TARGET_LAYER_INDEX,
        "cache_classes": cache_classes,
        "summary": {
            "pair_count": len(rows),
            "hidden_cosine_mean": float(cosines.mean()),
            "hidden_cosine_min": float(cosines.min()),
            "top5_token_jaccard_mean": float(
                np.mean([row["top5_token_jaccard"] for row in rows])
            ),
            "status": status,
            "passed": status == "go",
        },
        "rows": rows,
    }


def main() -> int:
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    models = {
        "bf16": BF16_MODEL,
        "four_bit": FOUR_BIT_MODEL,
    }
    results = {name: run_model_smoke(path) for name, path in models.items()}
    overall_status = "go"
    if any(result["summary"]["status"] == "no_go" for result in results.values()):
        overall_status = "no_go"
    elif any(result["summary"]["status"] == "warning" for result in results.values()):
        overall_status = "warning"

    payload = {
        "stage": "stage2_step1_5_kv_cache_smoke",
        "thresholds": {
            "pass_all_cosines_above": PASS_THRESHOLD,
            "fail_any_cosine_below": FAIL_THRESHOLD,
        },
        "prompt_variants": PROMPT_VARIANTS,
        "overall_status": overall_status,
        "overall_passed": overall_status == "go",
        "models": results,
    }
    RESULT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\nStage 2 Step 1.5 KV-cache smoke")
    for name, result in results.items():
        summary = result["summary"]
        print(
            f"{name}: status={summary['status']} "
            f"cosine mean/min={summary['hidden_cosine_mean']:.6f}/"
            f"{summary['hidden_cosine_min']:.6f}"
        )
    print(f"overall: {overall_status}")
    print(f"result file: {RESULT_PATH}")
    return 0 if overall_status == "go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
