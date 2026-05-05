"""Offline analyses for compact Stage 2 vector stores.

Stage 2 keeps compact suffix/end vectors in chunked safetensors so we can test
new geometry hypotheses without rerunning Qwen. This script reads a single
Stage 2 dump lazily, one `(variant, layer, position)` slice at a time, and
computes the follow-up analyses requested after the 9B-4bit 100-subset run:
anti-PCA/query-only anti-PCA, BM25 fusion, session-level metrics, and a
cross-layer summary.

Why: Stage 1 showed that post-processing geometry matters nearly as much as the
model forward itself. Stage 2 should keep model execution serial and expensive
forward passes minimal, then do cheap retrieval experiments over saved vectors.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from baselines.bm25 import BM25Retriever
from eval.longmemeval_metrics import Prediction, evaluate
from longmemeval.data import has_round_side_answer_label, iter_round_candidates, load_instances


DEFAULT_DUMP_DIR = ROOT / "tensors" / "stage2" / "9b_4bit_100_p0"
DEFAULT_DATA = ROOT / "data" / "longmemeval_s_cleaned.json"
DEFAULT_VARIANT = "P0"
DEFAULT_LAYER = 30
DEFAULT_POSITION = "last"
DEFAULT_TOP_K = 50


@dataclass(frozen=True)
class Stage2Record:
    prompt_id: str
    instance_index: int
    question_id: str
    role: str
    candidate_id: str | None
    is_gold: bool
    gold_ids: tuple[str, ...]
    token_count: int
    text: str
    is_abstention: bool
    has_target: bool
    chunk_file: str
    chunk_index: int


@dataclass(frozen=True)
class InstanceBucket:
    query_index: int | None
    candidate_indices: list[int]
    gold_ids: list[str]


@dataclass(frozen=True)
class ScoredPrediction:
    prediction: Prediction
    query_record: Stage2Record
    candidate_records: list[Stage2Record]
    candidate_ids: list[str]
    scores: np.ndarray


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(DEFAULT_DATA))
    parser.add_argument(
        "--analysis",
        choices=[
            "anti_pca_sweep",
            "bm25_fusion_alpha_sweep",
            "session_metrics",
            "cross_layer_top_summary",
            "all",
        ],
        required=True,
    )
    parser.add_argument("--variant", default=DEFAULT_VARIANT)
    parser.add_argument("--layer", type=int, default=DEFAULT_LAYER)
    parser.add_argument("--position", default=DEFAULT_POSITION)
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    dump_dir = Path(args.dump_dir)
    manifest = load_manifest(dump_dir)
    validate_manifest(manifest)
    records = load_records(dump_dir, manifest, Path(args.data))

    analyses: dict[str, Callable[[], dict[str, Any]]] = {
        "anti_pca_sweep": lambda: anti_pca_sweep(
            dump_dir,
            manifest,
            records,
            variant=args.variant,
            layer=args.layer,
            position=args.position,
            top_k=args.top_k,
            bootstrap_samples=args.bootstrap_samples,
        ),
        "bm25_fusion_alpha_sweep": lambda: bm25_fusion_alpha_sweep(
            dump_dir,
            manifest,
            records,
            variant=args.variant,
            layer=args.layer,
            position=args.position,
            top_k=args.top_k,
            bootstrap_samples=args.bootstrap_samples,
        ),
        "session_metrics": lambda: session_metrics_analysis(
            dump_dir,
            manifest,
            records,
            variant=args.variant,
            layer=args.layer,
            position=args.position,
            top_k=args.top_k,
            bootstrap_samples=args.bootstrap_samples,
        ),
        "cross_layer_top_summary": lambda: cross_layer_top_summary(
            dump_dir,
            manifest,
            records,
            variant=args.variant,
            top_k=args.top_k,
            bootstrap_samples=args.bootstrap_samples,
        ),
    }

    if args.analysis == "all":
        combined = {name: fn() for name, fn in analyses.items()}
        write_analysis_result("all", combined)
    else:
        write_analysis_result(args.analysis, analyses[args.analysis]())
    return 0


def load_manifest(dump_dir: Path) -> dict[str, Any]:
    path = dump_dir / "manifest.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing Stage 2 manifest: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def validate_manifest(manifest: dict[str, Any]) -> None:
    required = [
        "chunks",
        "prompts",
        "prompt_variants",
        "layers",
        "positions",
        "hidden_dim",
        "tensor_key",
    ]
    missing = [key for key in required if key not in manifest]
    if missing:
        raise ValueError(f"Stage 2 manifest missing required keys: {missing}")
    if manifest["tensor_key"] != "states":
        raise ValueError(f"Expected tensor_key='states', got {manifest['tensor_key']!r}")
    if not manifest["chunks"]:
        raise ValueError("Stage 2 manifest has no chunks.")


def load_records(dump_dir: Path, manifest: dict[str, Any], data_path: Path) -> list[Stage2Record]:
    """Return records in tensor-row order, enriched with LongMemEval text.

    The vector store manifest intentionally avoids duplicating all candidate
    text. For BM25 fusion and readable diagnostics we rejoin records to the
    cleaned LongMemEval JSON by `(instance_index, candidate_id)`.
    """
    instances = load_instances(data_path)
    max_instance = max(int(meta["instance_index"]) for meta in manifest["prompts"].values())
    if max_instance >= len(instances):
        raise ValueError(
            f"Manifest references instance {max_instance}, but {data_path} has only {len(instances)} items."
        )

    candidate_texts: dict[tuple[int, str], str] = {}
    gold_by_instance: dict[int, set[str]] = {}
    question_texts: dict[int, str] = {}
    is_abs: dict[int, bool] = {}
    has_target: dict[int, bool] = {}
    for index, instance in enumerate(instances[: max_instance + 1]):
        question_texts[index] = instance.question
        is_abs[index] = instance.is_abstention
        has_target[index] = has_round_side_answer_label(instance)
        gold_ids = set()
        for candidate_id, text, is_gold in iter_round_candidates(instance):
            candidate_texts[(index, candidate_id)] = text
            if is_gold:
                gold_ids.add(candidate_id)
        gold_by_instance[index] = gold_ids

    records: list[Stage2Record] = []
    prompt_meta = manifest["prompts"]
    for chunk in manifest["chunks"]:
        chunk_path = dump_dir / chunk["file"]
        if not chunk_path.exists():
            raise FileNotFoundError(f"Manifest chunk is missing: {chunk_path}")
        for prompt_id in chunk["prompt_ids"]:
            meta = prompt_meta[prompt_id]
            instance_index = int(meta["instance_index"])
            role = str(meta["role"])
            candidate_id = meta.get("candidate_id")
            if role == "query":
                text = question_texts[instance_index]
            else:
                if candidate_id is None:
                    raise ValueError(f"Candidate prompt {prompt_id} lacks candidate_id.")
                text = candidate_texts.get((instance_index, str(candidate_id)), "")
            records.append(
                Stage2Record(
                    prompt_id=prompt_id,
                    instance_index=instance_index,
                    question_id=str(meta["question_id"]),
                    role=role,
                    candidate_id=str(candidate_id) if candidate_id is not None else None,
                    is_gold=bool(meta.get("is_gold", False)),
                    gold_ids=tuple(sorted(gold_by_instance[instance_index])),
                    token_count=int(meta.get("token_count", 0)),
                    text=text,
                    is_abstention=is_abs[instance_index],
                    has_target=has_target[instance_index],
                    chunk_file=str(meta["chunk_file"]),
                    chunk_index=int(meta["chunk_index"]),
                )
            )

    # The online evaluator skipped a few empty candidates. Gold IDs should come
    # from the dataset, not only the vector store, so strict recall still
    # penalizes a skipped gold if that ever happens.
    for index, gold_ids in gold_by_instance.items():
        if gold_ids and not any(record.instance_index == index and record.is_gold for record in records):
            # Abstention/no-target questions can lack gold rows; real gold-loss
            # is caught in predictions because gold_ids are dataset-backed.
            continue
    return records


def group_by_instance(records: list[Stage2Record]) -> dict[int, InstanceBucket]:
    buckets: dict[int, dict[str, Any]] = {}
    for index, record in enumerate(records):
        bucket = buckets.setdefault(
            record.instance_index,
            {"query": None, "candidates": [], "gold_ids": list(record.gold_ids)},
        )
        if record.role == "query":
            bucket["query"] = index
        else:
            bucket["candidates"].append(index)
    return {
        index: InstanceBucket(
            query_index=bucket["query"],
            candidate_indices=bucket["candidates"],
            gold_ids=list(bucket["gold_ids"]),
        )
        for index, bucket in buckets.items()
    }


def load_vector_matrix(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[Stage2Record],
    *,
    variant: str,
    layer: int,
    position: str,
) -> np.ndarray:
    """Load one compact Stage 2 vector slice.

    Only `states[:, variant, layer, position, :]` is materialized. The default
    9B 100-subset slice is roughly 24.8k x 4096 fp32, about 400MB, and does not
    load unrelated layers/positions from the 8GB vector store.
    """
    variant_index = index_of(manifest["prompt_variants"], variant, "variant")
    layer_index = index_of(manifest["layers"], layer, "layer")
    position_index = index_of(manifest["positions"], position, "position")
    hidden_dim = int(manifest["hidden_dim"])
    output = np.empty((len(records), hidden_dim), dtype=np.float32)

    records_by_chunk: dict[str, list[tuple[int, Stage2Record]]] = {}
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
        except Exception:
            # Fallback for environments where safetensors numpy slicing cannot
            # expose bf16 rows. This loads one chunk at a time, never the whole
            # dump, so peak memory remains bounded.
            import mlx.core as mx

            states = mx.load(str(path))["states"]
            for row_index, record in rows:
                output[row_index] = np.array(
                    states[
                        record.chunk_index,
                        variant_index,
                        layer_index,
                        position_index,
                        :,
                    ].astype(mx.float32)
                )
            del states
    if not np.all(np.isfinite(output)):
        raise ValueError(f"Non-finite vector in {variant}|layer{layer}|{position}.")
    return output


def index_of(values: list[Any], target: Any, name: str) -> int:
    if target not in values:
        raise ValueError(f"{name} {target!r} not present in manifest values {values!r}")
    return int(values.index(target))


def anti_pca_sweep(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[Stage2Record],
    *,
    variant: str,
    layer: int,
    position: str,
    top_k: int,
    bootstrap_samples: int,
) -> dict[str, Any]:
    """Evaluate 9B anti-PCA and query-only anti-PCA over saved vectors.

    Stage 1 showed anti-PCA removes prompt-suffix shared directions and that
    query-only anti-PCA is nearly as good while being deployment-friendly. This
    repeats that test on 9B-4bit without rerunning the model.
    """
    vectors = load_vector_matrix(dump_dir, manifest, records, variant=variant, layer=layer, position=position)
    mean, pcs = global_anti_pca(records, vectors, max_components=20)
    configs: dict[str, Any] = {}
    for components in [2, 5, 10, 15, 20]:
        for mode in ["both", "query_only"]:
            name = f"{variant}|layer{layer}|{position}|anti_pca_{mode}_k{components}"
            predictions = predictions_from_vectors(
                records,
                vectors,
                top_k=top_k,
                score_fn=lambda query, candidates, *, components=components, mode=mode: anti_pca_scores(
                    query,
                    candidates,
                    mean=mean,
                    pcs=pcs[:components],
                    mode=mode,
                ),
            )
            configs[name] = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
    return {
        "analysis": "anti_pca_sweep",
        "base_vector": {"variant": variant, "layer": layer, "position": position},
        "configs": configs,
        "top_configs": top_metric_rows(configs),
    }


def bm25_fusion_alpha_sweep(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[Stage2Record],
    *,
    variant: str,
    layer: int,
    position: str,
    top_k: int,
    bootstrap_samples: int,
) -> dict[str, Any]:
    """Fuse 9B hidden scores with cheap BM25 inside the hidden top-50 set.

    Stage 1 showed BM25 adds lexical precision to semantic hidden-state scores.
    This analysis keeps model inference fixed and only reranks each hidden top
    50 with `alpha * zscore(hidden) + (1-alpha) * zscore(BM25)`.
    """
    vectors = load_vector_matrix(dump_dir, manifest, records, variant=variant, layer=layer, position=position)
    scored = scored_predictions_from_vectors(
        records,
        vectors,
        top_k=top_k,
        score_fn=centered_cosine_scores,
    )
    configs: dict[str, Any] = {}
    for alpha in [0.0, 0.25, 0.5, 0.75, 1.0]:
        name = f"{variant}|layer{layer}|{position}|centered_cosine_bm25_fusion_alpha{alpha:g}"
        predictions = [fuse_hidden_bm25(item, alpha=alpha) for item in scored]
        configs[name] = evaluate(predictions, skip_abstention=True, bootstrap_samples=bootstrap_samples)
    return {
        "analysis": "bm25_fusion_alpha_sweep",
        "base_vector": {"variant": variant, "layer": layer, "position": position},
        "note": "alpha=1.0 is hidden-only order restricted to the hidden top-50; alpha=0.0 is BM25 rerank inside hidden top-50, not global BM25.",
        "configs": configs,
        "top_configs": top_metric_rows(configs),
    }


def session_metrics_analysis(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[Stage2Record],
    *,
    variant: str,
    layer: int,
    position: str,
    top_k: int,
    bootstrap_samples: int,
) -> dict[str, Any]:
    """Report turn-level and session-level retrieval metrics for 9B.

    Stage 1 reframed the method as a strong session router. The 9B run should
    be judged both by strict turn recall and by whether it routes the query to
    the right conversation session.
    """
    vectors = load_vector_matrix(dump_dir, manifest, records, variant=variant, layer=layer, position=position)
    predictions = predictions_from_vectors(records, vectors, top_k=top_k, score_fn=centered_cosine_scores)
    return {
        "analysis": "session_metrics",
        "base_vector": {"variant": variant, "layer": layer, "position": position},
        "turn_metrics": evaluate(
            predictions,
            skip_abstention=True,
            bootstrap_samples=bootstrap_samples,
            ks=(1, 3, 5, 10, 20, 30, 50),
        ),
        "session_metrics": session_retrieval_metrics(predictions),
        "rank_metrics": rank_metrics(predictions),
    }


def cross_layer_top_summary(
    dump_dir: Path,
    manifest: dict[str, Any],
    records: list[Stage2Record],
    *,
    variant: str,
    top_k: int,
    bootstrap_samples: int,
) -> dict[str, Any]:
    """Recompute a compact cross-layer/position leaderboard from the dump.

    This is a sanity summary for readers: it confirms that the 9B winner is
    late-layer + prompt-final + centered cosine, and that stored non-final
    positions are diagnostics rather than the main retrieval path.
    """
    configs: dict[str, Any] = {}
    for layer in manifest["layers"]:
        for position in manifest["positions"]:
            vectors = load_vector_matrix(
                dump_dir,
                manifest,
                records,
                variant=variant,
                layer=int(layer),
                position=str(position),
            )
            for score_name, score_fn in [
                ("cosine", cosine_scores),
                ("centered_cosine", centered_cosine_scores),
            ]:
                name = f"{variant}|layer{layer}|{position}|{score_name}"
                predictions = predictions_from_vectors(records, vectors, top_k=top_k, score_fn=score_fn)
                configs[name] = evaluate(
                    predictions,
                    skip_abstention=True,
                    bootstrap_samples=bootstrap_samples,
                )
    return {
        "analysis": "cross_layer_top_summary",
        "variant": variant,
        "configs": configs,
        "top_configs": top_metric_rows(configs),
    }


def predictions_from_vectors(
    records: list[Stage2Record],
    vectors: np.ndarray,
    *,
    top_k: int,
    score_fn: Callable[[np.ndarray, np.ndarray], np.ndarray],
) -> list[Prediction]:
    return [item.prediction for item in scored_predictions_from_vectors(records, vectors, top_k, score_fn)]


def scored_predictions_from_vectors(
    records: list[Stage2Record],
    vectors: np.ndarray,
    top_k: int,
    score_fn: Callable[[np.ndarray, np.ndarray], np.ndarray],
) -> list[ScoredPrediction]:
    buckets = group_by_instance(records)
    output: list[ScoredPrediction] = []
    for bucket in buckets.values():
        if bucket.query_index is None or not bucket.candidate_indices:
            continue
        query_record = records[bucket.query_index]
        candidate_records = [records[index] for index in bucket.candidate_indices]
        candidate_ids = [record.candidate_id for record in candidate_records if record.candidate_id is not None]
        if len(candidate_ids) != len(candidate_records):
            raise ValueError(f"Missing candidate_id in instance {query_record.instance_index}.")
        candidate_matrix = vectors[bucket.candidate_indices]
        query_vector = vectors[bucket.query_index]
        scores = np.asarray(score_fn(query_vector, candidate_matrix), dtype=np.float64)
        if scores.shape != (len(candidate_records),):
            raise ValueError(f"score_fn returned {scores.shape}, expected {(len(candidate_records),)}")
        order = np.argsort(scores)[::-1][:top_k]
        retrieved = [candidate_ids[int(index)] for index in order]
        prediction = Prediction(
            question_id=query_record.question_id,
            retrieved_ids=retrieved,
            gold_ids=bucket.gold_ids,
            is_abstention=query_record.is_abstention,
            has_target=query_record.has_target,
        )
        output.append(
            ScoredPrediction(
                prediction=prediction,
                query_record=query_record,
                candidate_records=candidate_records,
                candidate_ids=candidate_ids,
                scores=scores,
            )
        )
    return output


def cosine_scores(query: np.ndarray, candidates: np.ndarray) -> np.ndarray:
    return normalize(candidates) @ normalize(query)


def centered_cosine_scores(query: np.ndarray, candidates: np.ndarray) -> np.ndarray:
    center = np.mean(candidates, axis=0)
    return normalize(candidates - center) @ normalize(query - center)


def anti_pca_scores(
    query: np.ndarray,
    candidates: np.ndarray,
    *,
    mean: np.ndarray,
    pcs: np.ndarray,
    mode: str,
) -> np.ndarray:
    if mode == "both":
        transformed_candidates = remove_pc_projection(candidates - mean, pcs)
        transformed_query = remove_pc_projection(query - mean, pcs)
    elif mode == "query_only":
        transformed_candidates = candidates
        transformed_query = remove_pc_projection(query - mean, pcs)
    else:
        raise ValueError(f"Unsupported anti-PCA mode: {mode}")
    return normalize(transformed_candidates) @ normalize(transformed_query)


def global_anti_pca(
    records: list[Stage2Record],
    vectors: np.ndarray,
    max_components: int,
) -> tuple[np.ndarray, np.ndarray]:
    candidate_indices = [index for index, record in enumerate(records) if record.role != "query"]
    candidates = vectors[candidate_indices].astype(np.float32, copy=False)
    mean = np.mean(candidates, axis=0)
    centered = candidates - mean
    covariance = (centered.T @ centered) / max(centered.shape[0] - 1, 1)
    values, eigvecs = np.linalg.eigh(covariance)
    order = np.argsort(values)[::-1][:max_components]
    pcs = eigvecs[:, order].T.astype(np.float32, copy=False)
    return mean.astype(np.float32, copy=False), pcs


def remove_pc_projection(vectors: np.ndarray, pcs: np.ndarray) -> np.ndarray:
    if pcs.size == 0:
        return vectors
    return vectors - (vectors @ pcs.T) @ pcs


def normalize(vectors: np.ndarray) -> np.ndarray:
    arr = np.asarray(vectors, dtype=np.float32)
    if arr.ndim == 1:
        norm = float(np.linalg.norm(arr))
        if norm <= 1e-12:
            return np.zeros_like(arr)
        return arr / norm
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-12)


def fuse_hidden_bm25(item: ScoredPrediction, alpha: float) -> Prediction:
    top_indices = np.argsort(item.scores)[::-1][:50]
    top_records = [item.candidate_records[index] for index in top_indices]
    hidden_scores = item.scores[top_indices]

    retriever = BM25Retriever().fit([record.text for record in top_records])
    bm25_pairs = retriever.query(item.query_record.text, top_k=len(top_records))
    bm25_scores = np.zeros(len(top_records), dtype=np.float64)
    for index, score in bm25_pairs:
        bm25_scores[int(index)] = float(score)

    fused = alpha * zscore_1d(hidden_scores) + (1.0 - alpha) * zscore_1d(bm25_scores)
    order = np.argsort(fused)[::-1]
    retrieved = [top_records[int(index)].candidate_id for index in order]
    already = {candidate_id for candidate_id in retrieved if candidate_id is not None}
    hidden_order = np.argsort(item.scores)[::-1]
    retrieved.extend(
        item.candidate_ids[int(index)]
        for index in hidden_order
        if item.candidate_ids[int(index)] not in already
    )
    return Prediction(
        question_id=item.prediction.question_id,
        retrieved_ids=[candidate_id for candidate_id in retrieved if candidate_id is not None],
        gold_ids=item.prediction.gold_ids,
        is_abstention=item.prediction.is_abstention,
        has_target=item.prediction.has_target,
    )


def zscore_1d(values: np.ndarray) -> np.ndarray:
    arr = np.asarray(values, dtype=np.float64)
    std = float(np.std(arr))
    if std <= 1e-12:
        return np.zeros_like(arr)
    return (arr - float(np.mean(arr))) / std


def session_retrieval_metrics(predictions: list[Prediction]) -> dict[str, float]:
    scored = [item for item in predictions if not item.is_abstention and item.has_target and item.gold_ids]
    metrics: dict[str, float] = {}
    for k in [1, 3, 5, 10, 20, 30, 50]:
        hit_values = []
        recall_values = []
        for prediction in scored:
            gold_sessions = {normalize_session_key(gold_id) for gold_id in prediction.gold_ids}
            retrieved_sessions = {
                normalize_session_key(candidate_id)
                for candidate_id in prediction.retrieved_ids[:k]
            }
            hit_values.append(float(bool(gold_sessions & retrieved_sessions)))
            recall_values.append(float(gold_sessions.issubset(retrieved_sessions)))
        metrics[f"session_hit@{k}"] = float(np.mean(hit_values)) if hit_values else float("nan")
        metrics[f"session_recall_all@{k}"] = float(np.mean(recall_values)) if recall_values else float("nan")
    return metrics


def rank_metrics(predictions: list[Prediction]) -> dict[str, Any]:
    scored = [item for item in predictions if not item.is_abstention and item.has_target and item.gold_ids]
    reciprocal_ranks = []
    first_hits: dict[str, int] = {}
    for prediction in scored:
        gold = set(prediction.gold_ids)
        first_position: int | None = None
        for index, candidate_id in enumerate(prediction.retrieved_ids, start=1):
            if candidate_id in gold:
                first_position = index
                break
        key = ">50" if first_position is None else str(first_position)
        first_hits[key] = first_hits.get(key, 0) + 1
        reciprocal_ranks.append(0.0 if first_position is None else 1.0 / first_position)
    return {
        "mrr": float(np.mean(reciprocal_ranks)) if reciprocal_ranks else float("nan"),
        "first_hit_position_histogram": dict(sorted(first_hits.items(), key=first_hit_sort_key)),
    }


def first_hit_sort_key(item: tuple[str, int]) -> tuple[int, str]:
    key, _value = item
    if key == ">50":
        return (10_000, key)
    return (int(key), key)


def normalize_session_key(candidate_id: str) -> str:
    return candidate_id.rsplit("_", 1)[0].replace("noans", "answer")


def top_metric_rows(configs: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for name, metrics in configs.items():
        recall5 = metrics["metrics"]["recall_all@5"]
        ndcg5 = metrics["metrics"]["ndcg_any@5"]
        rows.append(
            {
                "config": name,
                "recall_all@5": recall5["mean"],
                "recall_all@5_ci95": recall5["ci95"],
                "ndcg_any@5": ndcg5["mean"],
                "ndcg_any@5_ci95": ndcg5["ci95"],
                "n_scored": metrics["n_scored"],
            }
        )
    return sorted(rows, key=lambda row: (row["recall_all@5"], row["ndcg_any@5"]), reverse=True)


def write_analysis_result(name: str, result: dict[str, Any]) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    result_dir = ROOT / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    json_path = result_dir / f"stage2_offline_{name}_{timestamp}.json"
    md_path = result_dir / f"stage2_offline_{name}_{timestamp}.md"

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": name,
        "result": result,
    }
    json_path.write_text(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown_summary(name, result), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


def render_markdown_summary(name: str, result: dict[str, Any]) -> str:
    lines = [
        f"# Stage 2 offline analysis: {name}",
        "",
        "This analysis reads saved Stage 2 compact vectors and does not rerun the model.",
        "",
    ]
    if "top_configs" in result:
        lines.extend(render_top_table(result["top_configs"]))
    elif name == "all":
        for sub_name, sub_result in result.items():
            lines.extend([f"## {sub_name}", ""])
            if isinstance(sub_result, dict) and "top_configs" in sub_result:
                lines.extend(render_top_table(sub_result["top_configs"]))
            elif isinstance(sub_result, dict) and "session_metrics" in sub_result:
                lines.extend(render_session_table(sub_result))
    elif "session_metrics" in result:
        lines.extend(render_session_table(result))
    return "\n".join(lines).rstrip() + "\n"


def render_top_table(rows: list[dict[str, Any]], limit: int = 10) -> list[str]:
    lines = [
        "| config | R@5 | NDCG@5 | n |",
        "|---|---:|---:|---:|",
    ]
    for row in rows[:limit]:
        lines.append(
            f"| `{row['config']}` | {row['recall_all@5']:.3f} | "
            f"{row['ndcg_any@5']:.3f} | {row['n_scored']} |"
        )
    lines.append("")
    return lines


def render_session_table(result: dict[str, Any]) -> list[str]:
    session = result["session_metrics"]
    turn = result["turn_metrics"]["metrics"]
    return [
        "| metric | value |",
        "|---|---:|",
        f"| turn recall_all@5 | {turn['recall_all@5']['mean']:.3f} |",
        f"| turn ndcg_any@5 | {turn['ndcg_any@5']['mean']:.3f} |",
        f"| session_hit@5 | {session['session_hit@5']:.3f} |",
        f"| session_recall_all@5 | {session['session_recall_all@5']:.3f} |",
        f"| MRR | {result['rank_metrics']['mrr']:.3f} |",
        "",
    ]


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
