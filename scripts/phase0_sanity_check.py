"""Run the Phase 0 mlx-lm vs Transformers hidden-state sanity check."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hidden_state.mlx_wrapper import MLXHiddenStateExtractor
from hidden_state.transformers_wrapper import TransformersHiddenStateExtractor


MLX_MODEL_ID = os.environ.get("MLX_MODEL_ID", str(ROOT / "models" / "Qwen3.5-2B-bf16"))
HF_MODEL_ID = os.environ.get("HF_MODEL_ID", str(ROOT / "models" / "Qwen3.5-2B-hf"))
RESULT_PATH = ROOT / "results" / "phase0_sanity_check.json"
BLOCKER_PATH = ROOT / "notes" / "blockers.md"


def build_prompts() -> list[str]:
    raw_texts = [
        "用户喜欢在早上跑步，也经常记录每周训练距离。",
        "The user asked for a concise summary of an investment memo about battery supply chains.",
        "会议记录：Alice 负责数据清洗，Ben 负责评估脚本，周五前汇总结果。",
        "A travel note says the hotel near Shinjuku was quiet, inexpensive, and close to the station.",
        "孩子最近对天文学很感兴趣，尤其喜欢木星、土星和月食。",
        "The debugging session found that the failure only appears when the cache directory is missing.",
        "用户偏好：写作时少用夸张语气，多给可执行步骤。",
        "A research plan compares BM25, Contriever, and hidden-state retrieval on memory benchmarks.",
        "晚餐偏好记录：不吃香菜，可以接受微辣，喜欢清淡的汤。",
        "The project constraint says all dependencies must stay inside a local .venv and repo cache.",
        "客户反馈：移动端表格太拥挤，筛选按钮不明显，导出功能很重要。",
        "A long conversation mentioned that the warranty expires in August and the receipt is in email.",
    ]
    suffix = "\n请用一个词来summarize上面这段文字，这个词是：“"
    return [text + suffix for text in raw_texts]


def cosine(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.dot(left, right) / ((np.linalg.norm(left) * np.linalg.norm(right)) + 1e-12))


def top5_overlap(left: list[int], right: list[int]) -> float:
    return len(set(left) & set(right)) / max(len(set(left) | set(right)), 1)


def write_blocker(message: str) -> None:
    BLOCKER_PATH.parent.mkdir(parents=True, exist_ok=True)
    with BLOCKER_PATH.open("a", encoding="utf-8") as handle:
        handle.write("\n## Phase 0 blocker\n\n")
        handle.write(message.strip() + "\n")


def main() -> int:
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    prompts = build_prompts()
    dtype = torch.bfloat16
    threshold = 0.98
    precision_note = "MLX bf16 model compared with Transformers bfloat16."

    print(f"Loading MLX model: {MLX_MODEL_ID}")
    mlx_extractor = MLXHiddenStateExtractor(MLX_MODEL_ID, dtype_note="bf16")

    print(f"Loading Transformers model: {HF_MODEL_ID}")
    hf_extractor = TransformersHiddenStateExtractor(HF_MODEL_ID, dtype=dtype)

    rows = []
    for index, prompt in enumerate(prompts, start=1):
        mlx_result = mlx_extractor.encode_prompt(prompt)
        hf_result = hf_extractor.encode_prompt(prompt)
        hidden_cosine = cosine(mlx_result.vector, hf_result.vector)
        next_token_match = mlx_result.top_token_ids[0] == hf_result.top_token_ids[0]
        overlap = top5_overlap(mlx_result.top_token_ids, hf_result.top_token_ids)
        rows.append(
            {
                "index": index,
                "next_token_match": next_token_match,
                "mlx_next_token": mlx_result.next_token_text,
                "hf_next_token": hf_result.next_token_text,
                "top5_jaccard": overlap,
                "hidden_cosine": hidden_cosine,
                "mlx_top5": mlx_result.top_token_texts,
                "hf_top5": hf_result.top_token_texts,
            }
        )

    hidden_cosines = [row["hidden_cosine"] for row in rows]
    top5_overlaps = [row["top5_jaccard"] for row in rows]
    next_matches = [row["next_token_match"] for row in rows]
    summary = {
        "mlx_model_id": MLX_MODEL_ID,
        "hf_model_id": HF_MODEL_ID,
        "precision_note": precision_note,
        "threshold": threshold,
        "prompt_count": len(rows),
        "next_token_match_rate": float(np.mean(next_matches)),
        "top5_overlap_mean": float(np.mean(top5_overlaps)),
        "top5_overlap_min": float(np.min(top5_overlaps)),
        "hidden_cosine_mean": float(np.mean(hidden_cosines)),
        "hidden_cosine_min": float(np.min(hidden_cosines)),
        "passed": bool(np.min(hidden_cosines) >= threshold),
    }
    payload = {"summary": summary, "rows": rows}
    RESULT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\nPhase 0 sanity-check results")
    print(f"prompts: {summary['prompt_count']}")
    print(f"next-token match: {summary['next_token_match_rate']:.2%}")
    print(f"top-5 overlap mean/min: {summary['top5_overlap_mean']:.3f}/{summary['top5_overlap_min']:.3f}")
    print(f"hidden cosine mean/min: {summary['hidden_cosine_mean']:.6f}/{summary['hidden_cosine_min']:.6f}")
    print(f"result file: {RESULT_PATH}")

    if not summary["passed"]:
        write_blocker(
            "Phase 0 sanity check failed: hidden cosine min "
            f"{summary['hidden_cosine_min']:.6f} was below threshold {threshold:.2f}."
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
