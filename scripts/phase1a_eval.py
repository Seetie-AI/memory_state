"""Run Phase 1a LongMemEval-M/session retrieval baseline evaluation.

MVP_Plan.md sections 5.1 and 8 define Phase 1a as official pipeline
replication: run BM25 and Contriever on LongMemEval-M/session and compare
Recall@5 against public anchors. This script intentionally uses user-only
session text for both BM25 and Contriever to match the official LongMemEval
retrieval baseline described in MVP_Plan.md section 5.3.

Why: the hidden-state method should not be evaluated until data loading,
candidate construction, abstention filtering, and metrics reproduce known
baseline behavior.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Protocol


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from baselines.bm25 import BM25Retriever
from baselines.contriever import ContrieverRetriever
from baselines.qwen_embedding import QwenEmbeddingRetriever
from eval.longmemeval_metrics import Prediction, evaluate
from longmemeval.data import (
    Instance,
    has_round_side_answer_label,
    has_user_side_answer_label,
    iter_round_candidates,
    load_instances,
    session_text_user_only,
)
from method.hidden_state import HiddenStateRetriever


OFFICIAL_ANCHORS = {
    ("bm25", "session"): {"recall_all@5": 0.634, "ndcg_any@5": 0.516},
    ("contriever", "session"): {"recall_all@5": 0.723, "ndcg_any@5": 0.634},
}


class Retriever(Protocol):
    def fit(self, corpus_texts: list[str]) -> "Retriever":
        ...

    def query(self, query_text: str, top_k: int) -> list[tuple[int, float]]:
        ...


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--method",
        choices=["bm25", "contriever", "qwen_embedding", "hidden_state"],
        required=True,
    )
    parser.add_argument("--subset", type=int, default=100)
    parser.add_argument("--data", default=str(ROOT / "data" / "longmemeval_m_cleaned.json"))
    parser.add_argument("--granularity", choices=["session", "round"], default="session")
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--contriever-batch-size", type=int, default=16)
    parser.add_argument("--qwen-embedding-batch-size", type=int, default=4)
    parser.add_argument("--qwen-embedding-max-length", type=int, default=8192)
    parser.add_argument(
        "--hidden-state-model-path",
        default=str(ROOT / "models" / "Qwen3.5-2B-bf16"),
    )
    parser.add_argument(
        "--hidden-state-layer-index",
        type=int,
        default=None,
        help=(
            "Optional Python-style layer index for hidden_state. Omit to keep "
            "the original final post-norm behavior; use -9 for the Qwen3.5-2B "
            "1/e-from-end experiment."
        ),
    )
    return parser.parse_args()


def make_retriever(args: argparse.Namespace) -> Retriever:
    if args.method == "bm25":
        return BM25Retriever()
    if args.method == "contriever":
        return ContrieverRetriever(
            model_path=ROOT / "models" / "contriever",
            batch_size=args.contriever_batch_size,
        )
    if args.method == "qwen_embedding":
        return QwenEmbeddingRetriever(
            model_path=ROOT / "models" / "qwen3-embedding-0.6b",
            batch_size=args.qwen_embedding_batch_size,
            max_length=args.qwen_embedding_max_length,
        )
    if args.method == "hidden_state":
        return HiddenStateRetriever(
            model_path=args.hidden_state_model_path,
            target_layer_index=args.hidden_state_layer_index,
        )
    raise ValueError(f"Unsupported method: {args.method}")


def run_instance(
    instance: Instance,
    retriever: Retriever,
    top_k: int,
    granularity: str,
) -> Prediction:
    if granularity == "session":
        corpus_ids, corpus_texts, gold_ids, has_target = build_session_corpus(instance)
    elif granularity == "round":
        corpus_ids, corpus_texts, gold_ids, has_target = build_round_corpus(instance)
    else:
        raise ValueError(f"Unsupported granularity: {granularity}")

    ranking = retriever.fit(corpus_texts).query(instance.question, top_k=top_k)
    retrieved_ids = [corpus_ids[index] for index, _score in ranking]
    return Prediction(
        question_id=instance.question_id,
        retrieved_ids=retrieved_ids,
        gold_ids=gold_ids,
        is_abstention=instance.is_abstention,
        has_target=has_target,
    )


def build_session_corpus(instance: Instance) -> tuple[list[str], list[str], list[str], bool]:
    corpus_ids = instance.haystack_session_ids
    corpus_texts = [session_text_user_only(session) for session in instance.haystack_sessions]
    gold_ids = instance.answer_session_ids
    has_target = has_user_side_answer_label(instance)
    return corpus_ids, corpus_texts, gold_ids, has_target


def build_round_corpus(instance: Instance) -> tuple[list[str], list[str], list[str], bool]:
    candidates = iter_round_candidates(instance)
    corpus_ids = [candidate_id for candidate_id, _text, _is_gold in candidates]
    corpus_texts = [text for _candidate_id, text, _is_gold in candidates]
    gold_ids = [candidate_id for candidate_id, _text, is_gold in candidates if is_gold]
    has_target = has_round_side_answer_label(instance)
    return corpus_ids, corpus_texts, gold_ids, has_target


def main() -> int:
    args = parse_args()
    instances = load_instances(args.data)
    if args.subset and args.subset > 0:
        instances = instances[: args.subset]

    retriever = make_retriever(args)
    hidden_state_metadata = {}
    if args.method == "hidden_state":
        hidden_state_metadata = retriever.layer_metadata()
    predictions = [
        run_instance(
            instance,
            retriever=retriever,
            top_k=args.top_k,
            granularity=args.granularity,
        )
        for instance in instances
    ]
    metrics = evaluate(
        predictions,
        skip_abstention=True,
        bootstrap_samples=args.bootstrap_samples,
    )
    data_stem = Path(args.data).stem
    anchor = OFFICIAL_ANCHORS.get((args.method, args.granularity))
    if "longmemeval_m_cleaned" not in data_stem:
        anchor = None

    output = {
        "config": {
            "method": args.method,
            "data": args.data,
            "subset": args.subset,
            "granularity": args.granularity,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "hidden_state_model_path": args.hidden_state_model_path,
            **hidden_state_metadata,
        },
        "official_anchor": anchor,
        "metrics": metrics,
        "predictions": [asdict(prediction) for prediction in predictions],
    }

    result_dir = ROOT / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    subset_label = args.subset if args.subset and args.subset > 0 else "full"
    method_label = args.method
    if args.method == "hidden_state" and args.hidden_state_layer_index is not None:
        method_label = f"{args.method}_layer{args.hidden_state_layer_index}"
    output_path = result_dir / f"phase1a_{method_label}_{data_stem}_{args.granularity}_{subset_label}.json"
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    metrics_by_name = metrics["metrics"]
    recall5 = metrics_by_name["recall_all@5"]["mean"]
    ndcg5 = metrics_by_name["ndcg_any@5"]["mean"]
    recall5_ci = metrics_by_name["recall_all@5"]["ci95"]
    ndcg5_ci = metrics_by_name["ndcg_any@5"]["ci95"]

    print(f"method: {args.method}")
    print(f"scored: {metrics['n_scored']} / total: {metrics['n_total']}")
    if anchor is None:
        print(f"Recall@5: {recall5:.3f} (95% CI {recall5_ci['low']:.3f}-{recall5_ci['high']:.3f})")
        print(f"NDCG@5: {ndcg5:.3f} (95% CI {ndcg5_ci['low']:.3f}-{ndcg5_ci['high']:.3f})")
    else:
        print(
            "Recall@5: "
            f"{recall5:.3f} "
            f"(95% CI {recall5_ci['low']:.3f}-{recall5_ci['high']:.3f}; "
            f"official anchor {anchor['recall_all@5']:.3f})"
        )
        print(
            "NDCG@5: "
            f"{ndcg5:.3f} "
            f"(95% CI {ndcg5_ci['low']:.3f}-{ndcg5_ci['high']:.3f}; "
            f"official anchor {anchor['ndcg_any@5']:.3f})"
        )
    print(f"result: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
