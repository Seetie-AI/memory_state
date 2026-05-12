"""Temporary BM25 overlay for saved Qwen3 embedding-eval tensors."""

from __future__ import annotations

import argparse
import json
import sys
import time
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

import stage2_offline_analyze as offline
import stage3_prompt_fusion_bm25_sweep as bm25_sweep
from baselines.bm25 import BM25Retriever
from eval.longmemeval_metrics import Prediction, evaluate


DEFAULT_QWEN_DIR = ROOT / "tensors" / "stage3" / "embedding_eval" / "qwen3_embedding_8b_dwq_subset0-100"
DEFAULT_DATA = ROOT / "data" / "longmemeval_s_cleaned.json"
DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "step3_bm25_fusion" / "second_stage"
DEFAULT_OUTPUT_PREFIX = "tmp_embedding_bm25"


@dataclass
class EmbeddingBucketScores:
    question_id: str
    candidate_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool
    vector_scores: np.ndarray
    bm25_scores: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--embedding-dir", default=str(DEFAULT_QWEN_DIR))
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--alphas", default="0.7,0.75,0.8")
    parser.add_argument("--bm25-scope", choices=["vector_top20", "vector_top50"], default="vector_top20")
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    embedding_dir = Path(args.embedding_dir)
    manifest = load_manifest(embedding_dir)
    instances = offline.load_instances(args.data)
    alphas = parse_float_list(args.alphas)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in [json_path, md_path] if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    rows = build_score_rows(embedding_dir, manifest, instances, bm25_scope=args.bm25_scope)
    result_rows = []
    for alpha in alphas:
        predictions = predictions_from_scores(rows, alpha=alpha, top_k=args.top_k, scope=args.bm25_scope)
        metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=args.bootstrap_samples)
        session = offline.session_retrieval_metrics(predictions)
        rank = offline.rank_metrics(predictions)
        summary = bm25_sweep.summarize_metrics(metrics, session, rank)
        result_rows.append(
            {
                "alpha": alpha,
                "bm25_scope": args.bm25_scope,
                "metrics": metrics,
                "session_metrics": session,
                "rank_metrics": rank,
                "summary": summary,
            }
        )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "tmp_embedding_bm25_sweep",
        "inputs": {
            "embedding_dir": str(embedding_dir),
            "data": str(Path(args.data)),
            "alphas": alphas,
            "bm25_scope": args.bm25_scope,
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "model_path": manifest.get("model_path"),
        },
        "rows": result_rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


def load_manifest(embedding_dir: Path) -> dict[str, Any]:
    path = embedding_dir / "manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing embedding manifest: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_score_rows(
    embedding_dir: Path,
    manifest: dict[str, Any],
    instances: list[Any],
    *,
    bm25_scope: str,
) -> list[EmbeddingBucketScores]:
    rows = []
    for meta in manifest.get("instances", []):
        instance_index = int(meta["instance_index"])
        instance = instances[instance_index]
        candidate_ids = list(meta["candidate_ids"])
        candidate_text_by_id = {
            candidate_id: text
            for candidate_id, text, _is_gold in offline.iter_round_candidates(instance)
        }
        candidate_texts = [candidate_text_by_id[candidate_id] for candidate_id in candidate_ids]
        with np.load(embedding_dir / meta["file"]) as data:
            candidates = np.asarray(data["candidate_embeddings"], dtype=np.float32)
            query = np.asarray(data["query_embedding"], dtype=np.float32)
        vector_scores = (candidates @ query).astype(np.float64, copy=False)
        bm25_scores = bm25_scores_for_scope(
            instance.question,
            candidate_texts,
            vector_scores,
            scope=bm25_scope,
        )
        rows.append(
            EmbeddingBucketScores(
                question_id=str(meta["question_id"]),
                candidate_ids=candidate_ids,
                gold_ids=list(meta["gold_ids"]),
                is_abstention=bool(meta["is_abstention"]),
                has_target=bool(meta["has_target"]),
                vector_scores=vector_scores,
                bm25_scores=bm25_scores,
            )
        )
    return rows


def bm25_scores_for_scope(
    query_text: str,
    candidate_texts: list[str],
    vector_scores: np.ndarray,
    *,
    scope: str,
) -> np.ndarray:
    shortlist_k = parse_vector_scope_k(scope)
    order = np.argsort(vector_scores)[::-1]
    top_indices = [int(index) for index in order[: min(shortlist_k, len(order))]]
    scores = np.zeros(len(candidate_texts), dtype=np.float64)
    texts = [candidate_texts[index] for index in top_indices]
    retriever = BM25Retriever().fit(texts)
    for local_rank, score in retriever.query(query_text, top_k=len(texts)):
        scores[top_indices[int(local_rank)]] = float(score)
    return scores


def predictions_from_scores(
    rows: list[EmbeddingBucketScores],
    *,
    alpha: float,
    top_k: int,
    scope: str,
) -> list[Prediction]:
    shortlist_k = parse_vector_scope_k(scope)
    predictions = []
    for row in rows:
        vector_order = np.argsort(row.vector_scores)[::-1]
        top_indices = vector_order[: min(shortlist_k, len(vector_order))]
        fused_top = (
            alpha * offline.zscore_1d(row.vector_scores[top_indices])
            + (1.0 - alpha) * offline.zscore_1d(row.bm25_scores[top_indices])
        )
        reranked_top = top_indices[np.argsort(fused_top)[::-1]]
        top_set = {int(index) for index in top_indices}
        tail = [int(index) for index in vector_order if int(index) not in top_set]
        order = np.asarray([int(index) for index in reranked_top] + tail, dtype=np.int64)
        predictions.append(
            Prediction(
                question_id=row.question_id,
                retrieved_ids=[row.candidate_ids[int(index)] for index in order[:top_k]],
                gold_ids=row.gold_ids,
                is_abstention=row.is_abstention,
                has_target=row.has_target,
            )
        )
    return predictions


def parse_vector_scope_k(scope: str) -> int:
    prefix = "vector_top"
    if not scope.startswith(prefix):
        raise ValueError(f"Unsupported scope: {scope}")
    return int(scope[len(prefix) :])


def parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise ValueError("No alpha values parsed.")
    return values


def render_markdown(payload: dict[str, Any]) -> str:
    rows = sorted(
        payload["rows"],
        key=lambda row: (
            row["summary"]["recall_all@5"],
            row["summary"]["ndcg_any@5"],
            row["summary"]["mrr"],
        ),
        reverse=True,
    )
    lines = [
        "# Temporary embedding + BM25 sweep",
        "",
        f"BM25 scope: `{payload['inputs']['bm25_scope']}`",
        "",
        "| rank | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(rows, start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | {row['alpha']:.2f} | "
            f"{summary['recall_all@3']:.3f} | {summary['ndcg_any@3']:.3f} | "
            f"{summary['recall_all@5']:.3f} | {summary['ndcg_any@5']:.3f} | "
            f"{summary['mrr']:.3f} | {summary['session_hit@5']:.3f} | {summary['n_scored']} |"
        )
    lines.extend(["", "## Inputs", ""])
    lines.append(f"- embedding_dir: `{payload['inputs']['embedding_dir']}`")
    lines.append(f"- model_path: `{payload['inputs']['model_path']}`")
    lines.append(f"- elapsed_seconds: {payload['elapsed_seconds']:.1f}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
