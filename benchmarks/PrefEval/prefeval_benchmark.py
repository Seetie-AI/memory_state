"""Automatic PrefEval retrieval benchmark for chatbot preference memory.

This benchmark intentionally avoids LLM-as-judge evaluation. It converts each
PrefEval row into an exact-id retrieval task:

- memory candidates are stored user preference statements;
- each query is the row's final preference-sensitive question;
- the gold memory is the preference statement from the same row, with duplicate
  identical preference strings treated as equivalent by default.

The goal is to test whether Stage 3 hidden-state prompts transfer from
fact-retrieval LongMemEval to preference/persona memory retrieval. The active
prompt sweep is intentionally pruned after the first n=100 pass: duplicate,
language/punctuation controls, old "代表" controls, and repeatedly weak
interaction/strategy prompts are not encoded by default for the n=1000 run.

All HuggingFace cache paths are forced under this benchmark directory so the
script does not write outside the repository.
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import re
import signal
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from rank_bm25 import BM25Okapi


BENCH_DIR = Path(__file__).resolve().parent
ROOT = BENCH_DIR.parents[1]
SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
for path in [SCRIPTS, SRC]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

os.environ.setdefault("HF_HOME", str(BENCH_DIR / ".hf_home"))
os.environ.setdefault("HF_DATASETS_CACHE", str(BENCH_DIR / ".hf_home" / "datasets"))
os.environ.setdefault("HF_HUB_CACHE", str(BENCH_DIR / ".hf_home" / "hub"))

import stage2_offline_analyze as offline
from eval.longmemeval_metrics import Prediction, evaluate


DATASETS = {
    "explicit": "siyanzhao/prefeval_explicit",
    "implicit_choice": "siyanzhao/prefeval_implicit_choice",
    "implicit_persona": "siyanzhao/prefeval_implicit_persona",
}

DEFAULT_RETRIEVERS = [
    "bm25",
    "prompt_sweep_l28_l29_l30_l31_both_k15",
]
PROMPT_SWEEP_RETRIEVER = "prompt_sweep_l28_l29_l30_l31_both_k15"
EMBEDDING_RETRIEVERS = {"qwen3_embedding_bm25"}
ENGLISH_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "could",
    "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has",
    "have", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if",
    "in", "into", "is", "it", "its", "itself", "just", "me", "more", "most", "my", "myself", "no", "nor",
    "not", "now", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out",
    "over", "own", "s", "same", "she", "should", "so", "some", "such", "t", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to",
    "too", "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", "while",
    "who", "whom", "why", "will", "with", "would", "you", "your", "yours", "yourself", "yourselves",
}
WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")

PROMPT_VARIANTS = {
    "P0": "\n请用一个词来summarize上面这段文字，这个词是：“",
    "1-2": "\n用一个词概括上面这段对话，这个词是：“",
    "1-3": "\n用一个词标记上面这段对话，这个词是：“",
    "2-1": "\n用一个词标记上面这段对话中的话题，这个词是：“",
    "2-1_token": "\n用一个token标记上面这段对话中的话题，这个token是：“",
    "2-1-2": "\n用一个词标记这段对话中的话题，这个词是：“",
    "2-1_emoji": "\n用一个emoji标记上面这段对话中的话题，这个emoji是：“",
    "2-1_summarize": "\n用一个词概括上面这段对话中的话题，这个词是：“",
    "2-3-1": "\n用一个词标记上面这段对话最该让我想起的关键词，这个词是：“",
    "2-3-1_no_above": "\n用一个词标记这段对话最该让我想起的关键词，这个词是：“",
    "2-3-1_emoji": "\n用一个emoji标记上面这段对话最该让我想起的关键词，这个emoji是：“",
    "2-3-1_summarize": "\n用一个词概括上面这段对话最该让我想起的关键词，这个词是：“",
    "2-3-1_token": "\n用一个token标记上面这段对话最该让我想起的关键词，这个token是：“",
    "2-3-2_query": "\n用一个词标记当前这段对话最该让我回忆起的关键词，这个词是：“",
    "2-3-3": "\n用一个token标记上面这段对话最该让我想起的关键词，直接给token，不需要考虑可读性。这个token是：“",
    "2-4-1_user_word": "\n用一个词标记上面这段对话中的用户，这个词是：“",
    "2-4-2": "\n用一个词标记上面这段对话中的对方的需求，这个词是：“",
    "2-5": "\n用一个词标记上面这段对话让我产生的联想，这个词是：“",
    "2-5-2": "\n用一个词标记这段对话让我产生的联想。这个词是：“",
    "2-5-3": "\n用一个token标记上面这段对话让我产生的联想，直接给token，不需要考虑可读性。这个token是：“",
    "2-5_emoji": "\n用一个emoji标记上面这段对话让我产生的联想，这个emoji是：“",
    "2-5_summarize": "\n用一个词概括上面这段对话让我产生的联想，这个词是：“",
    "2-5_token": "\n用一个token标记上面这段对话让我产生的联想，这个token是：“",
    "2-7": "\n用一个词标记上面这段对话的互动模式，这个词是：“",
    "2-7_no_above": "\n用一个词标记这段对话的互动模式，这个词是：“",
    "2-7_emoji": "\n用一个emoji标记上面这段对话的互动模式，这个emoji是：“",
    "2-7_summarize": "\n用一个词概括上面这段对话的互动模式，这个词是：“",
    "2-7_token": "\n用一个token标记上面这段对话的互动模式，这个token是：“",
    "2-8": "\n用一个词标记上面这段对话的情绪，这个词是：“",
    "2-8_no_above": "\n用一个词标记这段对话的情绪，这个词是：“",
    "2-8_emoji": "\n用一个emoji标记上面这段对话的情绪，这个emoji是：“",
    "2-8_summarize": "\n用一个词概括上面这段对话的情绪，这个词是：“",
    "2-8_token": "\n用一个token标记上面这段对话的情绪，这个token是：“",
    "1-3_token": "\n用一个token标记上面这段对话，这个token是：“",
    "1-1-2": "\n用一个词标记这段对话，这个词是：“",
    "1-1_CN_explicit": "\n用中文，用一个词标记上面这段对话，这个词是：“",
    "1-1_EN_explicit": "\nIn English, tag the conversation above in one word. The word is:\"",
    "1-1_RU_explicit": "\nНа русском языке одним словом отметь диалог выше. Это слово: «",
    "1-1_JA_explicit": "\n日本語で、上の会話を一語でタグ付けしてください。その語は「",
    "1-1_EMOJI": "\n用一个emoji标记上面这段对话，这个emoji是：“",
    "user_preference": "\n用一个词标记上面这段对话中用户的偏好，这个词是：“",
    "user_preference_token": "\n用一个token标记上面这段对话中用户的偏好，这个token是：“",
    "user_avoidance": "\n用一个词标记上面这段对话中用户不喜欢或应避免的内容，这个词是：“",
    "personalization_need": "\n用一个词标记下次回答这个用户时最需要记住的个性化信息，这个词是：“",
}

# Keep the sweep compact for the n=1000 hidden-state run. `2-1` is retained
# because it led PrefEval n=100 by R@3, but its "话题" wording may benefit from
# PrefEval's topic-like structure; the paired `2-1_token` treatment checks
# whether a one-token key framing changes that signal. `2-4-1_user_word` and
# `2-5` are kept even though their single-prompt scores are modest because they
# diagnose the K3 concat components without extra product assumptions.
PROMPT_SWEEP_VARIANTS = [
    "P0",
    "1-2",
    "1-3",
    "2-1",
    "2-1_token",
    "2-3-1",
    "2-3-2_query",
    "2-4-1_user_word",
    "2-4-2",
    "2-5",
    "user_preference",
    "user_preference_token",
    "user_avoidance",
    "personalization_need",
]
# Layer labels are zero-based in the MLX extractor and Stage 3 result names:
# `L31` is the model's 32nd/final layer. The n=1000 run keeps L28-L31 for every
# active prompt so later offline analysis can compare the late-layer band
# without re-encoding the model.
PROMPT_SWEEP_LAYERS = [28, 29, 30, 31]

DEFAULT_HIDDEN_MODEL = ROOT / "models" / "Qwen3.5-9B-MLX-4bit"
DEFAULT_EMBEDDING_MODEL = ROOT / "models" / "Qwen3-Embedding-8B-4bit-DWQ"
DEFAULT_TASK_DESCRIPTION = (
    "Given a chatbot user's current question, retrieve the stored user preference "
    "memory needed to answer in a personalized way"
)


@dataclass(frozen=True)
class PrefEvalItem:
    item_id: str
    preference: str
    question: str
    topic: str
    preference_type: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class CellConfig:
    variant: str
    layer: int
    transform: str
    family: str

    @property
    def label(self) -> str:
        return f"{self.variant}|L{self.layer}|{self.transform}"


@dataclass
class CellVectors:
    cell: CellConfig
    candidate_vectors: np.ndarray
    query_vectors: np.ndarray
    note: str


@dataclass
class BenchmarkData:
    task: str
    dataset_id: str
    items: list[PrefEvalItem]
    candidate_ids: list[str]
    candidate_texts: list[str]
    query_ids: list[str]
    query_texts: list[str]
    gold_ids_by_query: list[list[str]]


CONFIGS = {
    "single_1-3": (
        "single hidden-state prompt 1-3, L31, anti_pca_both_k15",
        (CellConfig("1-3", 31, "anti_pca_both_k15", "tag"),),
        "single_vector",
    ),
    "k3_concat_selected": (
        "Stage 3 selected K3 concat layers/transforms, mark-default prompt wording",
        (
            CellConfig("2-4-1_user_word", 30, "anti_pca_both_k15", "user"),
            CellConfig("1-3", 31, "anti_pca_both_k15", "tag"),
            CellConfig("2-5", 29, "query_only_anti_pca_k2", "association"),
        ),
        "vertical_concat_norm_weighted",
    ),
    "k3_concat_uniform_l31_both_k15": (
        "same three prompts, all L31, all anti_pca_both_k15; overfit check",
        (
            CellConfig("2-4-1_user_word", 31, "anti_pca_both_k15", "user"),
            CellConfig("1-3", 31, "anti_pca_both_k15", "tag"),
            CellConfig("2-5", 31, "anti_pca_both_k15", "association"),
        ),
        "vertical_concat_norm_weighted",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    available_retrievers = sorted(set(DEFAULT_RETRIEVERS) | set(CONFIGS) | EMBEDDING_RETRIEVERS | {PROMPT_SWEEP_RETRIEVER})
    parser.add_argument("--task", choices=sorted(DATASETS), default="implicit_persona")
    parser.add_argument("--split", default="train")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument(
        "--shuffle-seed",
        type=int,
        default=0,
        help="Deterministically shuffle before --limit. Use -1 to keep dataset order.",
    )
    parser.add_argument(
        "--retrievers",
        default=",".join(DEFAULT_RETRIEVERS),
        help="Comma-separated retrievers, or 'all'. Available: "
        + ",".join(available_retrievers),
    )
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument(
        "--gold-policy",
        choices=["same_id", "same_preference_text"],
        default="same_preference_text",
        help="Treat identical preference strings as equivalent gold memories by default.",
    )
    parser.add_argument("--hidden-model-path", default=str(DEFAULT_HIDDEN_MODEL))
    parser.add_argument("--embedding-model-path", default=str(DEFAULT_EMBEDDING_MODEL))
    parser.add_argument("--embedding-alpha", type=float, default=0.75)
    parser.add_argument("--embedding-backend", choices=["mlx", "transformers"], default="mlx")
    parser.add_argument("--embedding-max-length", type=int, default=512)
    parser.add_argument("--embedding-batch-size", type=int, default=1)
    parser.add_argument("--embedding-dtype", choices=["float16", "bfloat16", "float32"], default="float16")
    parser.add_argument(
        "--store-topk-logits",
        type=int,
        default=0,
        help=(
            "When >0, store final next-token top-K token ids/logits for every "
            "encoded prompt/query/memory row. Full-vocab logits are intentionally "
            "not stored by this script because they would approach the local "
            "storage and memory budget."
        ),
    )
    parser.add_argument(
        "--store-promptreps-logits",
        action="store_true",
        help=(
            "Store a second PromptReps-style sparse logit representation: "
            "lowercase words from the source text, remove English stopwords and "
            "punctuation, tokenize the remaining words, keep only those token ids, "
            "apply ReLU+log1p saturation, keep top --promptreps-topk, and "
            "quantize by multiplying by 100."
        ),
    )
    parser.add_argument("--promptreps-topk", type=int, default=128)
    parser.add_argument(
        "--prompt-sweep-variants",
        default=None,
        help=(
            "Comma-separated prompt variants for the prompt sweep retriever. "
            "Defaults to the curated n=1000 prompt sweep list."
        ),
    )
    parser.add_argument(
        "--prompt-sweep-layers",
        default=None,
        help=(
            "Comma-separated zero-based layer labels for the prompt sweep retriever. "
            "Defaults to 28,29,30,31."
        ),
    )
    parser.add_argument("--output-prefix", default=None)
    parser.add_argument("--output-dir", default=str(BENCH_DIR / "results"))
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--synthetic-smoke", action="store_true", help="Use a tiny built-in dataset; no network/model needed.")
    parser.add_argument("--prepare-only", action="store_true", help="Only download/cache PrefEval and write prepared JSONL.")
    parser.add_argument("--dry-run", action="store_true", help="Build the task and estimate work without loading models.")
    parser.add_argument("--clear-cache-every", choices=["text", "never"], default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    output_prefix = args.output_prefix or default_output_prefix(args)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{output_prefix}.json"
    md_path = output_dir / f"{output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in [json_path, md_path] if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite or change --output-prefix: {existing}")

    retrievers = parse_retrievers(args.retrievers)
    data = load_benchmark_data(
        task=args.task,
        split=args.split,
        limit=args.limit,
        shuffle_seed=args.shuffle_seed,
        gold_policy=args.gold_policy,
        synthetic_smoke=args.synthetic_smoke,
    )
    write_prepared_jsonl(data, output_prefix)
    duplicate_count = len(data.candidate_ids) - len({normalize_key(text) for text in data.candidate_texts})
    log(
        f"task={data.task} dataset={data.dataset_id} items={len(data.items)} "
        f"candidates={len(data.candidate_ids)} queries={len(data.query_ids)} "
        f"duplicate_preferences={duplicate_count} retrievers={retrievers}"
    )

    if args.prepare_only or args.dry_run:
        payload = make_payload(args, data, [], started)
        payload["dry_run"] = bool(args.dry_run)
        payload["prepare_only"] = bool(args.prepare_only)
        write_outputs(payload, json_path, md_path)
        return 0

    stop_requested = False

    def handle_stop(signum: int, _frame: Any) -> None:
        nonlocal stop_requested
        log(f"received signal {signum}; stopping after current retriever")
        stop_requested = True

    for stop_signal in (signal.SIGINT, signal.SIGTERM):
        signal.signal(stop_signal, handle_stop)

    rows: list[dict[str, Any]] = []
    bm25_scores = score_bm25(data)
    if "bm25" in retrievers:
        rows.append(evaluate_score_matrix("bm25", "BM25 over preference memory strings", bm25_scores, data, args))
    if stop_requested:
        return finish(args, data, rows, started, json_path, md_path)

    hidden_retrievers = [name for name in retrievers if name in CONFIGS or name == PROMPT_SWEEP_RETRIEVER]
    if hidden_retrievers:
        rows.extend(run_hidden_retrievers(hidden_retrievers, data, args))
    if stop_requested:
        return finish(args, data, rows, started, json_path, md_path)

    if "qwen3_embedding_bm25" in retrievers:
        embedding_scores = score_qwen3_embedding(data, args)
        fused = fuse_zscores(embedding_scores, bm25_scores, alpha=args.embedding_alpha)
        rows.append(
            evaluate_score_matrix(
                "qwen3_embedding_bm25",
                f"Qwen3 embedding + BM25 z-score fusion, model={Path(args.embedding_model_path).name}, alpha={args.embedding_alpha:g}",
                fused,
                data,
                args,
                extra={"embedding_alpha": args.embedding_alpha},
            )
        )

    return finish(args, data, rows, started, json_path, md_path)


def finish(
    args: argparse.Namespace,
    data: BenchmarkData,
    rows: list[dict[str, Any]],
    started: float,
    json_path: Path,
    md_path: Path,
) -> int:
    payload = make_payload(args, data, rows, started)
    write_outputs(payload, json_path, md_path)
    log(f"wrote {json_path}")
    log(f"wrote {md_path}")
    return 0


def parse_retrievers(spec: str) -> list[str]:
    if spec == "all":
        return list(DEFAULT_RETRIEVERS)
    values = [part.strip() for part in spec.split(",") if part.strip()]
    allowed = set(DEFAULT_RETRIEVERS) | set(CONFIGS) | EMBEDDING_RETRIEVERS | {PROMPT_SWEEP_RETRIEVER}
    unknown = [value for value in values if value not in allowed]
    if unknown:
        raise ValueError(f"Unknown retriever(s): {unknown}. Allowed: {sorted(allowed)}")
    return values


def load_benchmark_data(
    *,
    task: str,
    split: str,
    limit: int,
    shuffle_seed: int | None,
    gold_policy: str,
    synthetic_smoke: bool,
) -> BenchmarkData:
    dataset_id = "synthetic" if synthetic_smoke else DATASETS[task]
    if synthetic_smoke:
        rows = synthetic_rows(task)
    else:
        from datasets import load_dataset

        log(f"loading {dataset_id} split={split} cache={os.environ['HF_DATASETS_CACHE']}")
        dataset = load_dataset(dataset_id, split=split, cache_dir=os.environ["HF_DATASETS_CACHE"])
        if shuffle_seed is not None and shuffle_seed >= 0:
            dataset = dataset.shuffle(seed=shuffle_seed)
        if limit and limit > 0:
            dataset = dataset.select(range(min(limit, len(dataset))))
        rows = [dict(row) for row in dataset]

    items: list[PrefEvalItem] = []
    for index, row in enumerate(rows):
        preference = clean_text(row.get("preference", ""))
        question = clean_text(row.get("question", "") or row.get("implicit_query", ""))
        if not preference or not question:
            raise ValueError(f"Row {index} is missing preference/question fields: {row.keys()}")
        item_id = f"{task}:{index:04d}"
        metadata = {
            key: value
            for key, value in row.items()
            if key not in {"preference", "question"}
        }
        items.append(
            PrefEvalItem(
                item_id=item_id,
                preference=preference,
                question=question,
                topic=clean_text(row.get("topic", "")),
                preference_type=clean_text(row.get("preference_type", task)),
                metadata=metadata,
            )
        )

    candidate_ids = [item.item_id for item in items]
    candidate_texts = [item.preference for item in items]
    query_ids = [f"{item.item_id}:query" for item in items]
    query_texts = [item.question for item in items]

    if gold_policy == "same_id":
        gold_ids_by_query = [[item.item_id] for item in items]
    else:
        ids_by_text: dict[str, list[str]] = {}
        for item in items:
            ids_by_text.setdefault(normalize_key(item.preference), []).append(item.item_id)
        gold_ids_by_query = [ids_by_text[normalize_key(item.preference)] for item in items]

    return BenchmarkData(
        task=task,
        dataset_id=dataset_id,
        items=items,
        candidate_ids=candidate_ids,
        candidate_texts=candidate_texts,
        query_ids=query_ids,
        query_texts=query_texts,
        gold_ids_by_query=gold_ids_by_query,
    )


def synthetic_rows(task: str) -> list[dict[str, str]]:
    return [
        {
            "preference": "I dislike horror games and prefer lighthearted adventure games.",
            "question": "What game should I play next if I want something thrilling but suitable for me?",
            "topic": "entertain_games",
            "preference_type": task,
        },
        {
            "preference": "I avoid virtual reality because it makes me motion sick.",
            "question": "Can you recommend immersive ways to explore historical sites?",
            "topic": "education_learning_styles",
            "preference_type": task,
        },
        {
            "preference": "I prefer in-person classroom learning over online courses.",
            "question": "What would you suggest for learning data analytics?",
            "topic": "education_learning_styles",
            "preference_type": task,
        },
        {
            "preference": "I dislike subscription-based learning resources.",
            "question": "What resources should I use to learn photography?",
            "topic": "education_resources",
            "preference_type": task,
        },
        {
            "preference": "I learn best through storytelling instead of flashcards.",
            "question": "How should I study historical dates for an exam?",
            "topic": "education_learning_styles",
            "preference_type": task,
        },
        {
            "preference": "I prefer cooperative board games over competitive card games.",
            "question": "What should I bring to game night this weekend?",
            "topic": "entertain_games",
            "preference_type": task,
        },
    ]


def write_prepared_jsonl(data: BenchmarkData, output_prefix: str) -> None:
    data_dir = BENCH_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / f"{output_prefix}.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for item, gold_ids in zip(data.items, data.gold_ids_by_query, strict=True):
            handle.write(
                json.dumps(
                    {
                        **asdict(item),
                        "query_id": f"{item.item_id}:query",
                        "gold_ids": gold_ids,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )


def score_bm25(data: BenchmarkData) -> np.ndarray:
    log("scoring BM25")
    tokenized = [text.split(" ") for text in data.candidate_texts]
    bm25 = BM25Okapi(tokenized)
    scores = np.zeros((len(data.query_texts), len(data.candidate_texts)), dtype=np.float32)
    for index, query in enumerate(data.query_texts, start=1):
        scores[index - 1] = np.asarray(bm25.get_scores(query.split(" ")), dtype=np.float32)
        if index == 1 or index == len(data.query_texts) or index % 50 == 0:
            log(f"  bm25 {index}/{len(data.query_texts)}")
    return scores


def run_hidden_retrievers(
    retriever_names: list[str],
    data: BenchmarkData,
    args: argparse.Namespace,
) -> list[dict[str, Any]]:
    needed_cells = unique_cells_for_retrievers(retriever_names, args)
    raw = load_or_encode_hidden_vectors(needed_cells, data, args)
    transformed = {cell.label: build_cell_vectors(cell, raw[cell.label]) for cell in needed_cells}

    rows: list[dict[str, Any]] = []
    for name in retriever_names:
        if name == PROMPT_SWEEP_RETRIEVER:
            for cell in prompt_sweep_cells(args):
                log(f"scoring prompt sweep cell {cell.label}")
                cell_vectors = transformed[cell.label]
                scores = score_single(cell_vectors)
                rows.append(
                    evaluate_score_matrix(
                        f"sweep_{cell.variant}_L{cell.layer}_both_k15",
                        f"prompt sweep single cell: {cell.variant}, L{cell.layer}, anti_pca_both_k15",
                        scores,
                        data,
                        args,
                        extra={"cells": [asdict(cell)], "scorer": "single_vector", "sweep": PROMPT_SWEEP_RETRIEVER},
                    )
                )
            continue
        description, cells, scorer = CONFIGS[name]
        log(f"scoring hidden retriever {name}")
        cell_vectors = [transformed[cell.label] for cell in cells]
        if scorer == "single_vector":
            scores = score_single(cell_vectors[0])
        elif scorer == "vertical_concat_norm_weighted":
            scores = score_vertical_concat(cell_vectors, component_normalize=False)
        else:
            raise ValueError(f"Unsupported scorer {scorer!r} for {name}")
        rows.append(
            evaluate_score_matrix(
                name,
                description,
                scores,
                data,
                args,
                extra={"cells": [asdict(cell) for cell in cells], "scorer": scorer},
            )
        )
    return rows


def unique_cells_for_retrievers(retriever_names: list[str], args: argparse.Namespace) -> list[CellConfig]:
    seen: set[str] = set()
    output: list[CellConfig] = []
    for name in retriever_names:
        if name == PROMPT_SWEEP_RETRIEVER:
            cells = tuple(prompt_sweep_cells(args))
        else:
            _description, cells, _scorer = CONFIGS[name]
        for cell in cells:
            if cell.label not in seen:
                output.append(cell)
                seen.add(cell.label)
    return output


def prompt_sweep_cells(args: argparse.Namespace | None = None) -> list[CellConfig]:
    variants = prompt_sweep_variants(args)
    layers = prompt_sweep_layers(args)
    return [
        CellConfig(variant, layer, "anti_pca_both_k15", "prompt-sweep")
        for variant in variants
        for layer in layers
    ]


def prompt_sweep_variants(args: argparse.Namespace | None = None) -> list[str]:
    if args is None or not getattr(args, "prompt_sweep_variants", None):
        return list(PROMPT_SWEEP_VARIANTS)
    variants = [part.strip() for part in args.prompt_sweep_variants.split(",") if part.strip()]
    unknown = [variant for variant in variants if variant not in PROMPT_VARIANTS]
    if unknown:
        raise ValueError(f"Unknown prompt sweep variant(s): {unknown}. Known: {sorted(PROMPT_VARIANTS)}")
    return unique_in_order(variants)


def prompt_sweep_layers(args: argparse.Namespace | None = None) -> list[int]:
    if args is None or not getattr(args, "prompt_sweep_layers", None):
        return list(PROMPT_SWEEP_LAYERS)
    layers = [int(part.strip()) for part in args.prompt_sweep_layers.split(",") if part.strip()]
    if not layers:
        raise ValueError("--prompt-sweep-layers must include at least one layer.")
    return layers


def promptreps_text_token_ids(text: str, tokenizer: Any) -> np.ndarray:
    """Token ids for the PromptReps sparse-logit filter.

    PromptReps lowercases text, extracts words, removes stopwords/punctuation,
    tokenizes each remaining word, and keeps logits only for those token ids.
    We use a small built-in English stopword list instead of adding NLTK as a
    dependency for this benchmark-only run.
    """
    words = [
        match.group(0)
        for match in WORD_RE.finditer(text.lower())
        if match.group(0) not in ENGLISH_STOPWORDS
    ]
    token_ids: set[int] = set()
    for word in words:
        try:
            encoded = tokenizer.encode(word, add_special_tokens=False)
        except TypeError:
            encoded = tokenizer.encode(word)
        for token_id in encoded:
            token_ids.add(int(token_id))
    if not token_ids:
        return np.zeros((0,), dtype=np.int32)
    return np.asarray(sorted(token_ids), dtype=np.int32)


def promptreps_sparse_topk(token_ids: np.ndarray, logits: np.ndarray, *, top_k: int) -> tuple[np.ndarray, np.ndarray]:
    """Apply the PromptReps sparse-logit recipe and return fixed-size arrays."""
    output_ids = np.full((top_k,), -1, dtype=np.int32)
    output_values = np.zeros((top_k,), dtype=np.int32)
    token_ids = np.asarray(token_ids, dtype=np.int32)
    logits = np.asarray(logits, dtype=np.float32)
    if token_ids.size == 0 or logits.size == 0:
        return output_ids, output_values
    weights = np.log1p(np.maximum(logits, 0.0))
    positive = weights > 0
    if not np.any(positive):
        return output_ids, output_values
    ids = np.asarray(token_ids, dtype=np.int32)[positive]
    values = weights[positive]
    order = np.argsort(-values)[:top_k]
    kept_values = np.floor(values[order] * 100.0).astype(np.int32, copy=False)
    nonzero = kept_values > 0
    kept_ids = ids[order][nonzero]
    kept_values = kept_values[nonzero]
    count = min(len(kept_ids), top_k)
    output_ids[:count] = kept_ids[:count]
    output_values[:count] = kept_values[:count]
    return output_ids, output_values


def load_or_encode_hidden_vectors(
    cells: list[CellConfig],
    data: BenchmarkData,
    args: argparse.Namespace,
) -> dict[str, dict[str, np.ndarray]]:
    prompt_hash = short_hash(
        [f"{cell.variant}:{PROMPT_VARIANTS[cell.variant]}" for cell in cells]
    )
    data_hash = benchmark_data_fingerprint(data)
    cache_dir = (
        BENCH_DIR
        / "tensors"
        / (
            f"hidden_{data.task}_n{len(data.items)}_"
            f"{data_hash}_"
            f"{short_hash([cell.label for cell in cells])}_"
            f"{prompt_hash}_"
            f"logits{args.store_topk_logits}_"
            f"promptreps{int(args.store_promptreps_logits)}x{args.promptreps_topk}"
        )
    )
    manifest_path = cache_dir / "manifest.json"
    vectors_path = cache_dir / "raw_hidden_vectors.npz"
    expected = {
        "kind": "prefeval_hidden_vectors",
        "task": data.task,
        "dataset_id": data.dataset_id,
        "item_ids": [item.item_id for item in data.items],
        "data_fingerprint": data_hash,
        "candidate_text_hash": short_hash(data.candidate_texts),
        "query_text_hash": short_hash(data.query_texts),
        "gold_ids_hash": short_hash([json.dumps(ids, ensure_ascii=False) for ids in data.gold_ids_by_query]),
        "model_path": str(Path(args.hidden_model_path)),
        "cells": [asdict(cell) for cell in cells],
        "prompt_variants": {cell.variant: PROMPT_VARIANTS[cell.variant] for cell in cells},
        "topk_logits": {
            "enabled": args.store_topk_logits > 0,
            "k": args.store_topk_logits,
            "schema": "per_variant_last_token_topk",
            "token_ids_suffix": "top_logit_token_ids",
            "values_suffix": "top_logit_values",
        },
        "promptreps_logits": {
            "enabled": bool(args.store_promptreps_logits),
            "top_k": args.promptreps_topk,
            "schema": "text_token_filtered_relu_log1p_topk_quantized",
            "token_ids_suffix": "promptreps_token_ids",
            "values_suffix": "promptreps_values",
            "value_dtype": "int32",
            "source": "PromptReps EMNLP 2024 sparse-logit recipe adapted without NLTK dependency.",
        },
    }
    if manifest_path.exists() and vectors_path.exists() and not args.overwrite:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("expected") == expected:
            log(f"loading hidden vector cache {cache_dir}")
            with np.load(vectors_path) as arrays:
                return {
                    cell.label: {
                        "candidates": np.asarray(arrays[f"{cell.label}::candidates"], dtype=np.float32),
                        "queries": np.asarray(arrays[f"{cell.label}::queries"], dtype=np.float32),
                    }
                    for cell in cells
                }
        if not args.resume:
            raise ValueError(
                f"Hidden cache exists but manifest does not match current run: {cache_dir}. "
                "Use --overwrite for a fresh cache."
            )

    if args.synthetic_smoke:
        log("synthetic smoke: using deterministic pseudo hidden vectors instead of loading MLX model")
        return pseudo_hidden_vectors(cells, data)

    from hidden_state.cached_suffix_extractor import CachedSuffixExtractor, clear_mlx_memory

    log(f"encoding hidden vectors with {args.hidden_model_path}")
    cache_dir.mkdir(parents=True, exist_ok=True)
    target_layers = sorted({cell.layer for cell in cells})
    target_variants = unique_in_order([cell.variant for cell in cells])
    extractor = CachedSuffixExtractor(args.hidden_model_path, clear_metal_cache_after_suffix=False)
    texts = data.candidate_texts + data.query_texts
    role_count = len(data.candidate_texts)
    raw_lists: dict[str, dict[str, list[np.ndarray]]] = {
        cell.label: {"candidates": [], "queries": []}
        for cell in cells
    }
    top_logit_lists: dict[str, dict[str, list[np.ndarray]]] = {}
    if args.store_topk_logits > 0:
        top_logit_lists = {
            variant: {
                "candidates_ids": [],
                "candidates_values": [],
                "queries_ids": [],
                "queries_values": [],
            }
            for variant in target_variants
        }
    promptreps_lists: dict[str, dict[str, list[np.ndarray]]] = {}
    if args.store_promptreps_logits:
        if args.promptreps_topk <= 0:
            raise ValueError(f"promptreps_topk must be > 0, got {args.promptreps_topk}.")
        promptreps_lists = {
            variant: {
                "candidates_ids": [],
                "candidates_values": [],
                "queries_ids": [],
                "queries_values": [],
            }
            for variant in target_variants
        }
    started = time.monotonic()
    for text_index, text in enumerate(texts):
        prefix_state = extractor.prefill_prefix(text, target_layers=target_layers, target_positions=["content_end"])
        suffix_vectors: dict[tuple[str, int], np.ndarray] = {}
        promptreps_token_ids = (
            promptreps_text_token_ids(text, extractor.tokenizer)
            if args.store_promptreps_logits
            else np.zeros((0,), dtype=np.int32)
        )
        for variant in target_variants:
            vectors, top_logits, selected_logits = extractor.encode_suffix_with_logit_outputs(
                prefix_state=prefix_state,
                suffix_text=PROMPT_VARIANTS[variant],
                target_layers=target_layers,
                target_positions=["last"],
                topk_logits=args.store_topk_logits,
                selected_logit_token_ids=promptreps_token_ids if args.store_promptreps_logits else None,
            )
            for layer in target_layers:
                value = vectors.get((layer, "last"))
                if value is not None:
                    suffix_vectors[(variant, layer)] = value.astype(np.float32, copy=False)
            if args.store_topk_logits > 0:
                try:
                    token_ids, logit_values = top_logits["last"]
                except KeyError as exc:
                    raise RuntimeError(f"Missing top-k logits for variant {variant!r}.") from exc
                side_prefix = "candidates" if text_index < role_count else "queries"
                top_logit_lists[variant][f"{side_prefix}_ids"].append(np.asarray(token_ids, dtype=np.int32))
                top_logit_lists[variant][f"{side_prefix}_values"].append(np.asarray(logit_values, dtype=np.float16))
            if args.store_promptreps_logits:
                side_prefix = "candidates" if text_index < role_count else "queries"
                if promptreps_token_ids.size > 0:
                    try:
                        selected_ids, selected_values = selected_logits["last"]
                    except KeyError as exc:
                        raise RuntimeError(f"Missing PromptReps logits for variant {variant!r}.") from exc
                else:
                    selected_ids = np.zeros((0,), dtype=np.int32)
                    selected_values = np.zeros((0,), dtype=np.float32)
                sparse_ids, sparse_values = promptreps_sparse_topk(
                    selected_ids,
                    selected_values,
                    top_k=args.promptreps_topk,
                )
                promptreps_lists[variant][f"{side_prefix}_ids"].append(sparse_ids)
                promptreps_lists[variant][f"{side_prefix}_values"].append(sparse_values)
        for cell in cells:
            vector = suffix_vectors[(cell.variant, cell.layer)]
            side = "candidates" if text_index < role_count else "queries"
            raw_lists[cell.label][side].append(vector)
        if args.clear_cache_every == "text":
            clear_mlx_memory(clear_metal_cache=True)
        done = text_index + 1
        elapsed = time.monotonic() - started
        eta = elapsed / max(done, 1) * (len(texts) - done)
        if done == 1 or done == len(texts) or done % 10 == 0:
            log(f"  hidden encoded {done}/{len(texts)} elapsed={fmt_duration(elapsed)} eta={fmt_duration(eta)}")
        del prefix_state
    del extractor
    clear_mlx_memory(clear_metal_cache=True)
    gc.collect()
    raw_by_cell = {
        cell.label: {
            "candidates": np.stack(raw_lists[cell.label]["candidates"], axis=0).astype(np.float32, copy=False),
            "queries": np.stack(raw_lists[cell.label]["queries"], axis=0).astype(np.float32, copy=False),
        }
        for cell in cells
    }
    save_npz = {
        f"{cell.label}::candidates": raw_by_cell[cell.label]["candidates"].astype(np.float16)
        for cell in cells
    }
    save_npz.update(
        {
            f"{cell.label}::queries": raw_by_cell[cell.label]["queries"].astype(np.float16)
            for cell in cells
        }
    )
    if args.store_topk_logits > 0:
        for variant, lists in top_logit_lists.items():
            save_npz[f"{variant}::candidates::top_logit_token_ids"] = np.stack(
                lists["candidates_ids"], axis=0
            ).astype(np.int32, copy=False)
            save_npz[f"{variant}::candidates::top_logit_values"] = np.stack(
                lists["candidates_values"], axis=0
            ).astype(np.float16, copy=False)
            save_npz[f"{variant}::queries::top_logit_token_ids"] = np.stack(
                lists["queries_ids"], axis=0
            ).astype(np.int32, copy=False)
            save_npz[f"{variant}::queries::top_logit_values"] = np.stack(
                lists["queries_values"], axis=0
            ).astype(np.float16, copy=False)
    if args.store_promptreps_logits:
        for variant, lists in promptreps_lists.items():
            save_npz[f"{variant}::candidates::promptreps_token_ids"] = np.stack(
                lists["candidates_ids"], axis=0
            ).astype(np.int32, copy=False)
            save_npz[f"{variant}::candidates::promptreps_values"] = np.stack(
                lists["candidates_values"], axis=0
            ).astype(np.int32, copy=False)
            save_npz[f"{variant}::queries::promptreps_token_ids"] = np.stack(
                lists["queries_ids"], axis=0
            ).astype(np.int32, copy=False)
            save_npz[f"{variant}::queries::promptreps_values"] = np.stack(
                lists["queries_values"], axis=0
            ).astype(np.int32, copy=False)
    np.savez_compressed(vectors_path, **save_npz)
    manifest_path.write_text(
        json.dumps({"expected": expected, "created_utc": now_utc(), "vector_dtype": "float16"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return raw_by_cell


def pseudo_hidden_vectors(cells: list[CellConfig], data: BenchmarkData) -> dict[str, dict[str, np.ndarray]]:
    output: dict[str, dict[str, np.ndarray]] = {}
    for cell in cells:
        dim = 128
        candidate_vectors = np.zeros((len(data.candidate_texts), dim), dtype=np.float32)
        query_vectors = np.zeros((len(data.query_texts), dim), dtype=np.float32)
        for index, text in enumerate(data.candidate_texts):
            candidate_vectors[index] = hash_vector(f"{cell.label}|doc|{text}", dim)
        for index, text in enumerate(data.query_texts):
            query_vectors[index] = hash_vector(f"{cell.label}|query|{text}", dim)
        output[cell.label] = {"candidates": candidate_vectors, "queries": query_vectors}
    return output


def build_cell_vectors(cell: CellConfig, raw: dict[str, np.ndarray]) -> CellVectors:
    candidates = np.asarray(raw["candidates"], dtype=np.float32)
    queries = np.asarray(raw["queries"], dtype=np.float32)
    if cell.transform == "anti_pca_both_k15":
        mean, pcs = fit_anti_pca(candidates, components=15)
        return CellVectors(
            cell=cell,
            candidate_vectors=remove_pc_projection(candidates - mean, pcs),
            query_vectors=remove_pc_projection(queries - mean, pcs),
            note="anti_pca_both_k15 via candidate-matrix SVD",
        )
    if cell.transform == "query_only_anti_pca_k2":
        mean, pcs = fit_anti_pca(candidates, components=2)
        return CellVectors(
            cell=cell,
            candidate_vectors=candidates,
            query_vectors=remove_pc_projection(queries - mean, pcs),
            note="candidate raw, query anti_pca_k2 via candidate-matrix SVD",
        )
    raise ValueError(f"Unsupported transform: {cell.transform}")


def fit_anti_pca(candidates: np.ndarray, components: int) -> tuple[np.ndarray, np.ndarray]:
    mean = np.mean(candidates, axis=0).astype(np.float32, copy=False)
    centered = candidates - mean
    if centered.shape[0] < 2 or components <= 0:
        return mean, np.zeros((0, candidates.shape[1]), dtype=np.float32)
    _u, _s, vt = np.linalg.svd(centered.astype(np.float32, copy=False), full_matrices=False)
    pcs = vt[: min(components, vt.shape[0])].astype(np.float32, copy=False)
    return mean, pcs


def remove_pc_projection(vectors: np.ndarray, pcs: np.ndarray) -> np.ndarray:
    if pcs.size == 0:
        return vectors.astype(np.float32, copy=False)
    return (vectors - (vectors @ pcs.T) @ pcs).astype(np.float32, copy=False)


def score_single(cell_vectors: CellVectors) -> np.ndarray:
    return normalize_rows(cell_vectors.query_vectors) @ normalize_rows(cell_vectors.candidate_vectors).T


def score_vertical_concat(cell_vectors: list[CellVectors], *, component_normalize: bool) -> np.ndarray:
    candidate_parts = []
    query_parts = []
    for cell in cell_vectors:
        candidates = cell.candidate_vectors
        queries = cell.query_vectors
        if component_normalize:
            candidates = normalize_rows(candidates)
            queries = normalize_rows(queries)
        candidate_parts.append(candidates)
        query_parts.append(queries)
    candidates = normalize_rows(np.concatenate(candidate_parts, axis=1))
    queries = normalize_rows(np.concatenate(query_parts, axis=1))
    return queries @ candidates.T


def score_qwen3_embedding(data: BenchmarkData, args: argparse.Namespace) -> np.ndarray:
    data_hash = benchmark_data_fingerprint(data)
    cache_dir = (
        BENCH_DIR
        / "tensors"
        / f"qwen3_embedding_{data.task}_n{len(data.items)}_{data_hash}"
    )
    manifest_path = cache_dir / "manifest.json"
    vectors_path = cache_dir / "embeddings.npz"
    expected = {
        "kind": "prefeval_qwen3_embedding",
        "task": data.task,
        "dataset_id": data.dataset_id,
        "item_ids": [item.item_id for item in data.items],
        "data_fingerprint": data_hash,
        "candidate_text_hash": short_hash(data.candidate_texts),
        "query_text_hash": short_hash(data.query_texts),
        "gold_ids_hash": short_hash([json.dumps(ids, ensure_ascii=False) for ids in data.gold_ids_by_query]),
        "model_path": str(Path(args.embedding_model_path)),
        "backend": args.embedding_backend,
        "max_length": args.embedding_max_length,
        "task_description": DEFAULT_TASK_DESCRIPTION,
    }
    if manifest_path.exists() and vectors_path.exists() and not args.overwrite:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("expected") == expected:
            log(f"loading Qwen3 embedding cache {cache_dir}")
            with np.load(vectors_path) as arrays:
                candidates = np.asarray(arrays["candidate_embeddings"], dtype=np.float32)
                queries = np.asarray(arrays["query_embeddings"], dtype=np.float32)
            return queries @ candidates.T
        if not args.resume:
            raise ValueError(
                f"Embedding cache exists but manifest does not match current run: {cache_dir}. "
                "Use --overwrite for a fresh cache."
            )

    if args.synthetic_smoke:
        log("synthetic smoke: using deterministic pseudo Qwen3 embeddings")
        candidates = np.stack([hash_vector(f"qwen|doc|{text}", 256) for text in data.candidate_texts])
        queries = np.stack([hash_vector(f"qwen|query|{text}", 256) for text in data.query_texts])
        return normalize_rows(queries) @ normalize_rows(candidates).T

    log(f"encoding Qwen3 embeddings with {args.embedding_model_path}")
    cache_dir.mkdir(parents=True, exist_ok=True)
    backend = make_embedding_backend(args)
    started = time.monotonic()
    candidates = encode_with_progress(
        backend,
        data.candidate_texts,
        kind="documents",
        batch_size=args.embedding_batch_size,
        started=started,
    )
    queries = encode_with_progress(
        backend,
        data.query_texts,
        kind="queries",
        batch_size=args.embedding_batch_size,
        started=started,
    )
    np.savez_compressed(
        vectors_path,
        candidate_embeddings=candidates.astype(np.float16),
        query_embeddings=queries.astype(np.float16),
    )
    manifest_path.write_text(
        json.dumps({"expected": expected, "created_utc": now_utc(), "vector_dtype": "float16"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return queries @ candidates.T


def make_embedding_backend(args: argparse.Namespace) -> Any:
    import stage3_embedding_eval as embedding_eval

    if args.embedding_backend == "mlx":
        return embedding_eval.MLXBackend(
            str(args.embedding_model_path),
            pooling="last_token",
            task_description=DEFAULT_TASK_DESCRIPTION,
            normalize=True,
            clear_cache_every="text",
        )
    if args.embedding_backend == "transformers":
        return embedding_eval.TransformersBackend(
            str(args.embedding_model_path),
            batch_size=args.embedding_batch_size,
            max_length=args.embedding_max_length,
            device=None,
            dtype=args.embedding_dtype,
            pooling="last_token",
            task_description=DEFAULT_TASK_DESCRIPTION,
            trust_remote_code=True,
            normalize=True,
        )
    raise ValueError(f"Unsupported embedding backend: {args.embedding_backend}")


def encode_with_progress(
    backend: Any,
    texts: list[str],
    *,
    kind: str,
    batch_size: int,
    started: float,
) -> np.ndarray:
    vectors = []
    encoder = backend.encode_documents if kind == "documents" else backend.encode_queries
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        vectors.append(encoder(batch))
        done = min(start + batch_size, len(texts))
        if done == len(texts) or done == batch_size or done % 25 == 0:
            elapsed = time.monotonic() - started
            eta = elapsed / max(done, 1) * (len(texts) * 2 - done)
            log(f"  qwen {kind} {done}/{len(texts)} elapsed={fmt_duration(elapsed)} eta~{fmt_duration(eta)}")
    return np.concatenate(vectors, axis=0).astype(np.float32, copy=False)


def evaluate_score_matrix(
    name: str,
    description: str,
    scores: np.ndarray,
    data: BenchmarkData,
    args: argparse.Namespace,
    *,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    raw_predictions = predictions_from_scores(scores, data, top_k=args.top_k)
    predictions = canonicalize_equivalent_gold_predictions(raw_predictions)
    metrics = evaluate(
        predictions,
        skip_abstention=True,
        bootstrap_samples=args.bootstrap_samples,
        ks=(1, 3, 5, 10, 20, 50),
    )
    summary = summarize_predictions(predictions, metrics)
    log(
        f"{name}: R@1={summary['recall_all@1']:.3f} R@3={summary['recall_all@3']:.3f} "
        f"R@5={summary['recall_all@5']:.3f} NDCG@5={summary['ndcg_any@5']:.3f} MRR={summary['mrr']:.3f}"
    )
    return {
        "name": name,
        "description": description,
        "metrics": metrics,
        "summary": summary,
        "gold_evaluation": {
            "mode": "any_equivalent_preference" if any(len(pred.gold_ids) > 1 for pred in raw_predictions) else "single_gold",
            "equivalent_gold_queries": sum(1 for pred in raw_predictions if len(pred.gold_ids) > 1),
            "note": (
                "Duplicate preference strings are treated as equivalent by collapsing a query's duplicate gold ids "
                "to one canonical id before LongMemEval-style recall_all/NDCG scoring."
            ),
        },
        **(extra or {}),
    }


def predictions_from_scores(scores: np.ndarray, data: BenchmarkData, *, top_k: int) -> list[Prediction]:
    predictions = []
    for query_index, query_id in enumerate(data.query_ids):
        order = np.argsort(scores[query_index])[::-1][:top_k]
        predictions.append(
            Prediction(
                question_id=query_id,
                retrieved_ids=[data.candidate_ids[int(index)] for index in order],
                gold_ids=data.gold_ids_by_query[query_index],
                is_abstention=False,
                has_target=True,
            )
        )
    return predictions


def canonicalize_equivalent_gold_predictions(predictions: list[Prediction]) -> list[Prediction]:
    """Make duplicate PrefEval preferences behave as equivalent gold memories.

    LongMemEval's `recall_all` metric requires every gold id to be retrieved.
    PrefEval's default `same_preference_text` policy instead means identical
    preference strings are interchangeable. For each query we collapse only that
    query's duplicate gold ids to a single canonical id, preserving unrelated
    retrieved ids so non-gold duplicates do not shift ranks.
    """
    output: list[Prediction] = []
    for prediction in predictions:
        if len(prediction.gold_ids) <= 1:
            output.append(prediction)
            continue
        canonical_gold = prediction.gold_ids[0]
        equivalent_gold = set(prediction.gold_ids)
        seen_equivalent = False
        retrieved_ids: list[str] = []
        for candidate_id in prediction.retrieved_ids:
            if candidate_id in equivalent_gold:
                if seen_equivalent:
                    continue
                retrieved_ids.append(canonical_gold)
                seen_equivalent = True
            else:
                retrieved_ids.append(candidate_id)
        output.append(
            Prediction(
                question_id=prediction.question_id,
                retrieved_ids=retrieved_ids,
                gold_ids=[canonical_gold],
                is_abstention=prediction.is_abstention,
                has_target=prediction.has_target,
            )
        )
    return output


def summarize_predictions(predictions: list[Prediction], metrics: dict[str, Any]) -> dict[str, float]:
    summary = {
        name: float(value["mean"])
        for name, value in metrics["metrics"].items()
        if name in {
            "recall_all@1",
            "recall_all@3",
            "recall_all@5",
            "recall_all@10",
            "recall_all@20",
            "recall_all@50",
            "ndcg_any@1",
            "ndcg_any@3",
            "ndcg_any@5",
            "ndcg_any@10",
            "ndcg_any@20",
            "ndcg_any@50",
        }
    }
    summary["mrr"] = mean_reciprocal_rank(predictions)
    return summary


def mean_reciprocal_rank(predictions: list[Prediction]) -> float:
    values = []
    for prediction in predictions:
        gold = set(prediction.gold_ids)
        rank = 0
        for index, candidate_id in enumerate(prediction.retrieved_ids, start=1):
            if candidate_id in gold:
                rank = index
                break
        values.append(0.0 if rank == 0 else 1.0 / rank)
    return float(np.mean(values)) if values else 0.0


def fuse_zscores(left: np.ndarray, right: np.ndarray, *, alpha: float) -> np.ndarray:
    if left.shape != right.shape:
        raise ValueError(f"Score matrices differ: {left.shape} vs {right.shape}")
    return alpha * row_zscore(left) + (1.0 - alpha) * row_zscore(right)


def row_zscore(scores: np.ndarray) -> np.ndarray:
    mean = np.mean(scores, axis=1, keepdims=True)
    std = np.std(scores, axis=1, keepdims=True)
    output = np.zeros_like(scores, dtype=np.float32)
    mask = (std[:, 0] > 1e-12)
    if np.any(mask):
        output[mask] = ((scores[mask] - mean[mask]) / std[mask]).astype(np.float32, copy=False)
    return output


def normalize_rows(vectors: np.ndarray) -> np.ndarray:
    arr = np.asarray(vectors, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-12)


def make_payload(
    args: argparse.Namespace,
    data: BenchmarkData,
    rows: list[dict[str, Any]],
    started: float,
) -> dict[str, Any]:
    rows = sorted(rows, key=lambda row: (row.get("summary", {}).get("recall_all@5", 0.0), row.get("summary", {}).get("ndcg_any@5", 0.0)), reverse=True)
    return {
        "created_utc": now_utc(),
        "analysis": "prefeval_automatic_retrieval",
        "inputs": {
            "task": args.task,
            "dataset_id": data.dataset_id,
            "split": args.split,
            "limit": args.limit,
            "shuffle_seed": args.shuffle_seed,
            "retrievers": parse_retrievers(args.retrievers),
            "top_k": args.top_k,
            "gold_policy": args.gold_policy,
            "hidden_model_path": args.hidden_model_path,
            "embedding_model_path": args.embedding_model_path,
            "embedding_alpha": args.embedding_alpha,
            "store_topk_logits": args.store_topk_logits,
            "store_promptreps_logits": args.store_promptreps_logits,
            "promptreps_topk": args.promptreps_topk,
            "prompt_sweep_variants": prompt_sweep_variants(args),
            "prompt_sweep_layers": prompt_sweep_layers(args),
            "output_dir": args.output_dir,
            "data_fingerprint": benchmark_data_fingerprint(data),
            "synthetic_smoke": args.synthetic_smoke,
        },
        "task_summary": {
            "items": len(data.items),
            "candidate_count": len(data.candidate_ids),
            "query_count": len(data.query_ids),
            "duplicate_preference_strings": len(data.candidate_ids) - len({normalize_key(text) for text in data.candidate_texts}),
            "duplicate_equivalent_queries": sum(1 for gold_ids in data.gold_ids_by_query if len(gold_ids) > 1),
            "topics": sorted({item.topic for item in data.items if item.topic}),
            "preference_types": sorted({item.preference_type for item in data.items if item.preference_type}),
        },
        "prompt_notes": {
            "prompt_sweep": PROMPT_SWEEP_RETRIEVER,
            "pruned_after_n100": [
                "1-1_CN",
                "1-1_CN_ASCII",
                "1-1_EN",
                "2-3-2_mem",
                "2-4-1",
                "2-6",
                "2-7",
                "2-8",
                "2-4-1_user_word_represent",
                "2-5_represent",
                "2-7_represent",
                "2-8_represent",
            ],
            "token_treatments": ["2-1_token", "user_preference_token"],
            "new_preference_prompts": ["user_preference", "user_avoidance", "personalization_need"],
            "note": (
                "PrefEval n=1000 uses a pruned prompt sweep. The 2-1 topic prompt "
                "is useful for the target companion scenario but may partly fit "
                "PrefEval's topic-structured rows, so it is tracked with a token "
                "wording treatment."
            ),
        },
        "rows": rows,
        "elapsed_seconds": time.monotonic() - started,
    }


def write_outputs(payload: dict[str, Any], json_path: Path, md_path: Path) -> None:
    json_path.write_text(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# PrefEval Automatic Retrieval",
        "",
        f"- Created UTC: `{payload['created_utc']}`",
        f"- Task: `{payload['inputs']['task']}`",
        f"- Dataset: `{payload['inputs']['dataset_id']}`",
        f"- Items: `{payload['task_summary']['items']}`",
        f"- Gold policy: `{payload['inputs']['gold_policy']}`",
        f"- Elapsed: `{fmt_duration(float(payload.get('elapsed_seconds', 0.0)))}`",
        "",
        "## Results",
        "",
    ]
    if not payload.get("rows"):
        lines.append("_No retrievers were evaluated._")
        return "\n".join(lines) + "\n"
    lines.extend(
        [
            "| rank | retriever | R@1 | R@3 | R@5 | NDCG@3 | NDCG@5 | MRR |",
            "|---:|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for index, row in enumerate(payload["rows"], start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | `{row['name']}` | {summary['recall_all@1']:.3f} | "
            f"{summary['recall_all@3']:.3f} | {summary['recall_all@5']:.3f} | "
            f"{summary['ndcg_any@3']:.3f} | {summary['ndcg_any@5']:.3f} | {summary['mrr']:.3f} |"
        )
    lines.extend(["", "## Configs", ""])
    for row in payload["rows"]:
        lines.append(f"- `{row['name']}`: {row['description']}")
    prompt_notes = payload.get("prompt_notes", {})
    lines.extend(["", "## Prompt Notes", ""])
    lines.append(f"- Sweep: `{prompt_notes.get('prompt_sweep', PROMPT_SWEEP_RETRIEVER)}`")
    if prompt_notes.get("new_preference_prompts"):
        lines.append("- New preference prompts: " + ", ".join(f"`{name}`" for name in prompt_notes["new_preference_prompts"]))
    if prompt_notes.get("token_treatments"):
        lines.append("- Token wording treatments: " + ", ".join(f"`{name}`" for name in prompt_notes["token_treatments"]))
    if prompt_notes.get("pruned_after_n100"):
        lines.append("- Pruned after n=100: " + ", ".join(f"`{name}`" for name in prompt_notes["pruned_after_n100"]))
    if prompt_notes.get("note"):
        lines.append(f"- Note: {prompt_notes['note']}")
    return "\n".join(lines) + "\n"


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def normalize_key(text: str) -> str:
    return clean_text(text).casefold()


def benchmark_data_fingerprint(data: BenchmarkData) -> str:
    values = []
    for item, query_id, gold_ids in zip(data.items, data.query_ids, data.gold_ids_by_query, strict=True):
        values.append(
            json.dumps(
                {
                    "item_id": item.item_id,
                    "preference": item.preference,
                    "question": item.question,
                    "topic": item.topic,
                    "preference_type": item.preference_type,
                    "query_id": query_id,
                    "gold_ids": gold_ids,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    return short_hash(values)


def unique_in_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output = []
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def short_hash(values: list[str]) -> str:
    import hashlib

    joined = "\n".join(values).encode("utf-8")
    return hashlib.sha1(joined).hexdigest()[:10]


def hash_vector(text: str, dim: int) -> np.ndarray:
    import hashlib

    digest = hashlib.sha256(text.encode("utf-8")).digest()
    seed = int.from_bytes(digest[:8], "little", signed=False)
    rng = np.random.default_rng(seed)
    vector = rng.normal(size=dim).astype(np.float32)
    return vector / max(float(np.linalg.norm(vector)), 1e-12)


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): to_jsonable(val) for key, val in value.items()}
    if isinstance(value, list | tuple):
        return [to_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_output_prefix(args: argparse.Namespace) -> str:
    mode = "synthetic" if args.synthetic_smoke else args.task
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{mode}_n{args.limit}_{stamp}"


def fmt_duration(seconds: float) -> str:
    seconds_int = max(int(seconds), 0)
    minutes, second = divmod(seconds_int, 60)
    hours, minute = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minute:02d}m{second:02d}s"
    if minutes:
        return f"{minute}m{second:02d}s"
    return f"{second}s"


def log(message: str) -> None:
    print(message, flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
