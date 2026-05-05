"""Stage 2 Step 1: compare 2B bf16 and 4-bit MLX hidden-state geometry.

Why: notes/stage_2_plan.md Step 1 makes 2B 4-bit validation a gate before
using quantized weights for Stage 2 prompt sweeps or as a proxy for the 9B
4-bit path. Stage 1 showed that retrieval quality depends on hidden-state
geometry, so this script compares the Stage 1 winning source directly:
Qwen3.5-2B layer 22, prompt-final suffix-end vectors.

The script loads one model at a time to keep unified-memory peak low. It does
not write tensors, only a compact JSON sanity report.
"""

from __future__ import annotations

import gc
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mlx.core as mx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hidden_state.mlx_wrapper import MLXHiddenStateExtractor


BF16_MODEL = ROOT / "models" / "Qwen3.5-2B-bf16"
FOUR_BIT_MODEL = ROOT / "models" / "Qwen3.5-2B-MLX-4bit"
RESULT_PATH = ROOT / "results" / "stage2_step1_4bit_sanity.json"
TARGET_LAYER_INDEX = 22
SUFFIX = "\n请用一个词来summarize上面这段文字，这个词是：“"
MEAN_COSINE_THRESHOLD = 0.98
MIN_COSINE_THRESHOLD = 0.97


@dataclass(frozen=True)
class EncodedPrompt:
    vector: np.ndarray
    top_token_ids: list[int]
    top_token_texts: list[str]
    next_token_text: str


def build_texts() -> list[str]:
    """Small mixed-language set shaped like memory turns and user queries."""
    return [
        "用户说早餐通常喝无糖拿铁，周末会加一块蓝莓司康。",
        "The user noted that the warranty expires in August and the receipt is stored in email.",
        "会议记录：Alice 负责清洗数据，Ben 负责把评估脚本接到 CI。",
        "旅行偏好：住在车站附近，不要太吵，房间可以小但必须干净。",
        "The debugging note says the cache bug appears only after the models directory is moved.",
        "孩子最近迷上天文学，尤其问了很多关于木星和月食的问题。",
        "用户写作偏好：不要夸张，不要鸡汤，多给清晰的下一步。",
        "Dinner preference: avoid cilantro, mild spice is fine, and clear soup is preferred.",
        "研究计划比较 BM25、Qwen embedding 和 LLM hidden-state retrieval。",
        "The customer complained that mobile tables are crowded and export is hard to find.",
        "用户上次提到想买轻薄的 14 寸笔记本，预算不要超过一千五百美元。",
        "A project note says dependencies must stay in the local .venv and models under the repo.",
        "财务备忘录提到电池供应链的关键风险是锂价和港口拥堵。",
        "The user said their preferred calendar reminder is one day before travel and again two hours before departure.",
        "健身记录：周一跑了五公里，周三力量训练，周五休息。",
        "A support thread says the login failure happens only when third-party cookies are disabled.",
    ]


def build_retrieval_cases() -> list[dict[str, Any]]:
    """Tiny retrieval-style smoke tests; these are not benchmark claims."""
    return [
        {
            "name": "breakfast",
            "query": "用户早餐通常喝什么？",
            "candidates": [
                "用户说早餐通常喝无糖拿铁，周末会加一块蓝莓司康。",
                "用户写作偏好：不要夸张，不要鸡汤，多给清晰的下一步。",
                "旅行偏好：住在车站附近，不要太吵，房间可以小但必须干净。",
                "健身记录：周一跑了五公里，周三力量训练，周五休息。",
                "客户反馈：移动端表格太拥挤，导出功能很重要。",
            ],
            "gold_index": 0,
        },
        {
            "name": "debug_cache",
            "query": "哪个问题和缓存目录或者模型目录有关？",
            "candidates": [
                "Dinner preference: avoid cilantro, mild spice is fine, and clear soup is preferred.",
                "The debugging note says the cache bug appears only after the models directory is moved.",
                "The user noted that the warranty expires in August and the receipt is stored in email.",
                "The customer complained that mobile tables are crowded and export is hard to find.",
                "A project note says dependencies must stay in the local .venv and models under the repo.",
            ],
            "gold_index": 1,
        },
        {
            "name": "alice_data",
            "query": "谁负责数据清洗？",
            "candidates": [
                "The support thread says login fails when third-party cookies are disabled.",
                "会议记录：Alice 负责清洗数据，Ben 负责把评估脚本接到 CI。",
                "研究计划比较 BM25、Qwen embedding 和 LLM hidden-state retrieval。",
                "孩子最近迷上天文学，尤其问了很多关于木星和月食的问题。",
                "用户上次提到想买轻薄的 14 寸笔记本。",
            ],
            "gold_index": 1,
        },
    ]


def prompt(text: str) -> str:
    return text + SUFFIX


def cosine(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.dot(left, right) / ((np.linalg.norm(left) * np.linalg.norm(right)) + 1e-12))


def topk_jaccard(left: list[int], right: list[int], k: int = 5) -> float:
    left_set = set(left[:k])
    right_set = set(right[:k])
    return len(left_set & right_set) / max(len(left_set | right_set), 1)


def clear_mlx_memory() -> None:
    gc.collect()
    try:
        if hasattr(mx, "metal") and hasattr(mx.metal, "clear_cache"):
            mx.metal.clear_cache()
    except Exception:
        pass


def encode_texts(model_path: Path, texts: list[str]) -> list[EncodedPrompt]:
    print(f"Loading {model_path}")
    extractor = MLXHiddenStateExtractor(
        str(model_path),
        dtype_note="mlx",
        target_layer_index=TARGET_LAYER_INDEX,
    )
    encoded: list[EncodedPrompt] = []
    for index, text in enumerate(texts, start=1):
        result = extractor.encode_prompt(prompt(text))
        encoded.append(
            EncodedPrompt(
                vector=result.vector.astype(np.float32),
                top_token_ids=result.top_token_ids,
                top_token_texts=result.top_token_texts,
                next_token_text=result.next_token_text,
            )
        )
        if index % 4 == 0:
            clear_mlx_memory()
    del extractor
    clear_mlx_memory()
    return encoded


def retrieval_smoke(model_path: Path, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Run tiny retrieval checks within one model load."""
    print(f"Loading {model_path} for retrieval smoke")
    extractor = MLXHiddenStateExtractor(
        str(model_path),
        dtype_note="mlx",
        target_layer_index=TARGET_LAYER_INDEX,
    )
    rows: list[dict[str, Any]] = []
    for case in cases:
        query_vec = extractor.encode_prompt(prompt(case["query"])).vector.astype(np.float32)
        candidate_vecs = [
            extractor.encode_prompt(prompt(candidate)).vector.astype(np.float32)
            for candidate in case["candidates"]
        ]
        matrix = np.stack(candidate_vecs, axis=0)
        scores = matrix @ query_vec
        ranking = np.argsort(-scores).tolist()
        rows.append(
            {
                "name": case["name"],
                "gold_index": int(case["gold_index"]),
                "ranking": [int(value) for value in ranking],
                "gold_rank_1_indexed": int(ranking.index(case["gold_index"]) + 1),
                "top1_is_gold": bool(ranking[0] == case["gold_index"]),
                "scores": [float(value) for value in scores.tolist()],
            }
        )
        clear_mlx_memory()
    del extractor
    clear_mlx_memory()
    return rows


def compare_retrieval_rows(
    bf16_rows: list[dict[str, Any]],
    four_bit_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output = []
    for bf16, quantized in zip(bf16_rows, four_bit_rows, strict=True):
        output.append(
            {
                "name": bf16["name"],
                "gold_index": bf16["gold_index"],
                "bf16_ranking": bf16["ranking"],
                "four_bit_ranking": quantized["ranking"],
                "top3_overlap": len(set(bf16["ranking"][:3]) & set(quantized["ranking"][:3])) / 3.0,
                "bf16_gold_rank": bf16["gold_rank_1_indexed"],
                "four_bit_gold_rank": quantized["gold_rank_1_indexed"],
            }
        )
    return output


def main() -> int:
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    texts = build_texts()

    bf16 = encode_texts(BF16_MODEL, texts)
    four_bit = encode_texts(FOUR_BIT_MODEL, texts)

    rows = []
    for index, (left, right) in enumerate(zip(bf16, four_bit, strict=True), start=1):
        rows.append(
            {
                "index": index,
                "hidden_cosine": cosine(left.vector, right.vector),
                "top5_token_jaccard": topk_jaccard(left.top_token_ids, right.top_token_ids),
                "bf16_next_token": left.next_token_text,
                "four_bit_next_token": right.next_token_text,
                "bf16_top5": left.top_token_texts,
                "four_bit_top5": right.top_token_texts,
            }
        )

    hidden_cosines = np.asarray([row["hidden_cosine"] for row in rows], dtype=np.float64)
    top5_jaccards = np.asarray([row["top5_token_jaccard"] for row in rows], dtype=np.float64)

    cases = build_retrieval_cases()
    bf16_smoke = retrieval_smoke(BF16_MODEL, cases)
    four_bit_smoke = retrieval_smoke(FOUR_BIT_MODEL, cases)
    smoke_compare = compare_retrieval_rows(bf16_smoke, four_bit_smoke)

    passed = bool(
        float(hidden_cosines.mean()) > MEAN_COSINE_THRESHOLD
        and float(hidden_cosines.min()) > MIN_COSINE_THRESHOLD
    )
    payload = {
        "stage": "stage2_step1_4bit_sanity",
        "models": {
            "bf16": str(BF16_MODEL),
            "four_bit": str(FOUR_BIT_MODEL),
        },
        "target_layer_index": TARGET_LAYER_INDEX,
        "thresholds": {
            "hidden_cosine_mean": MEAN_COSINE_THRESHOLD,
            "hidden_cosine_min": MIN_COSINE_THRESHOLD,
        },
        "summary": {
            "prompt_count": len(rows),
            "hidden_cosine_mean": float(hidden_cosines.mean()),
            "hidden_cosine_min": float(hidden_cosines.min()),
            "top5_token_jaccard_mean": float(top5_jaccards.mean()),
            "top5_token_jaccard_min": float(top5_jaccards.min()),
            "passed": passed,
            "decision": "go" if passed else "no_go",
        },
        "rows": rows,
        "retrieval_smoke": {
            "bf16": bf16_smoke,
            "four_bit": four_bit_smoke,
            "comparison": smoke_compare,
        },
    }
    RESULT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\nStage 2 Step 1 4-bit sanity")
    print(f"hidden cosine mean/min: {payload['summary']['hidden_cosine_mean']:.6f}/"
          f"{payload['summary']['hidden_cosine_min']:.6f}")
    print(f"top-5 token jaccard mean/min: {payload['summary']['top5_token_jaccard_mean']:.3f}/"
          f"{payload['summary']['top5_token_jaccard_min']:.3f}")
    print(f"decision: {payload['summary']['decision']}")
    print(f"result file: {RESULT_PATH}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
