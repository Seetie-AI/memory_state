"""Offline asymmetric prompt probe for saved PrefEval hidden-vector caches."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


BENCH_DIR = Path(__file__).resolve().parent
DEFAULT_RESULTS_DIR = BENCH_DIR / "results"
DEFAULT_TENSOR_ROOT = BENCH_DIR / "tensors"
DEFAULT_DATA_DIR = BENCH_DIR / "data"


@dataclass(frozen=True)
class Row:
    name: str
    candidate_cell: str
    query_cell: str
    summary: dict[str, float]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", default="auto")
    parser.add_argument("--data-jsonl", default="auto")
    parser.add_argument("--output-prefix", default=None)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.monotonic()
    cache_dir = resolve_cache_dir(args.cache_dir)
    data_path = resolve_data_jsonl(args.data_jsonl)
    prefix = args.output_prefix or f"asymmetric_2-3_n100_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    output_json = DEFAULT_RESULTS_DIR / f"{prefix}.json"
    output_md = DEFAULT_RESULTS_DIR / f"{prefix}.md"
    if not args.overwrite and (output_json.exists() or output_md.exists()):
        raise FileExistsError(f"Output exists; use --overwrite or change --output-prefix: {prefix}")

    print(f"cache_dir={cache_dir}", flush=True)
    print(f"data_jsonl={data_path}", flush=True)

    data = load_data(data_path)
    manifest = json.loads((cache_dir / "manifest.json").read_text(encoding="utf-8"))
    validate_manifest_alignment(data, manifest)
    with np.load(cache_dir / "raw_hidden_vectors.npz") as arrays:
        result_rows = []
        configs = [
            ("2-3-1 symmetric", "2-3-1|L31|anti_pca_both_k15", "2-3-1|L31|anti_pca_both_k15"),
            ("2-3-2_mem symmetric", "2-3-2_mem|L31|anti_pca_both_k15", "2-3-2_mem|L31|anti_pca_both_k15"),
            ("2-3-2_query symmetric", "2-3-2_query|L31|anti_pca_both_k15", "2-3-2_query|L31|anti_pca_both_k15"),
            ("2-3-2_mem -> 2-3-2_query", "2-3-2_mem|L31|anti_pca_both_k15", "2-3-2_query|L31|anti_pca_both_k15"),
            ("2-3-2_query -> 2-3-2_mem", "2-3-2_query|L31|anti_pca_both_k15", "2-3-2_mem|L31|anti_pca_both_k15"),
        ]
        for name, candidate_cell, query_cell in configs:
            scores = score_pair(arrays, candidate_cell, query_cell)
            predictions = predictions_from_scores(scores, data)
            summary = summarize(predictions)
            result_rows.append(Row(name, candidate_cell, query_cell, summary))
            print(
                f"{name}: R@1={summary['recall@1']:.3f} R@3={summary['recall@3']:.3f} "
                f"R@5={summary['recall@5']:.3f} NDCG@5={summary['ndcg@5']:.3f} MRR={summary['mrr']:.3f}",
                flush=True,
            )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "prefeval_asymmetric_2-3_probe",
        "inputs": {
            "cache_dir": str(cache_dir),
            "data_jsonl": str(data_path),
            "manifest_expected": manifest.get("expected", {}),
        },
        "rows": [
            {
                "name": row.name,
                "candidate_cell": row.candidate_cell,
                "query_cell": row.query_cell,
                "summary": row.summary,
            }
            for row in sorted(result_rows, key=lambda row: (row.summary["recall@5"], row.summary["ndcg@5"]), reverse=True)
        ],
        "elapsed_seconds": time.monotonic() - started,
    }
    DEFAULT_RESULTS_DIR.mkdir(exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {output_json}", flush=True)
    print(f"wrote {output_md}", flush=True)
    return 0


def resolve_cache_dir(spec: str) -> Path:
    if spec != "auto":
        path = Path(spec)
        if not path.exists():
            raise FileNotFoundError(path)
        return path
    candidates = sorted(
        DEFAULT_TENSOR_ROOT.glob("hidden_implicit_persona_n100_*"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for path in candidates:
        if (path / "manifest.json").exists() and (path / "raw_hidden_vectors.npz").exists():
            return path
    raise FileNotFoundError("No hidden_implicit_persona_n100_* cache found.")


def resolve_data_jsonl(spec: str) -> Path:
    if spec != "auto":
        path = Path(spec)
        if not path.exists():
            raise FileNotFoundError(path)
        return path
    candidates = sorted(
        DEFAULT_DATA_DIR.glob("implicit_persona_n100_*.jsonl"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError("No implicit_persona_n100_*.jsonl prepared data found.")
    return candidates[0]


def load_data(path: Path) -> dict[str, list[Any]]:
    items = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                items.append(json.loads(line))
    candidate_ids = [item["item_id"] for item in items]
    query_ids = [item["query_id"] for item in items]
    gold_ids = [list(item["gold_ids"]) for item in items]
    preferences = [clean_text(item.get("preference", "")) for item in items]
    questions = [clean_text(item.get("question", "")) for item in items]
    topics = [clean_text(item.get("topic", "")) for item in items]
    preference_types = [clean_text(item.get("preference_type", "")) for item in items]
    return {
        "candidate_ids": candidate_ids,
        "query_ids": query_ids,
        "gold_ids": gold_ids,
        "preferences": preferences,
        "questions": questions,
        "topics": topics,
        "preference_types": preference_types,
    }


def validate_manifest_alignment(data: dict[str, list[Any]], manifest: dict[str, Any]) -> None:
    expected = manifest.get("expected", {})
    if expected.get("item_ids") != data["candidate_ids"]:
        raise ValueError("Prepared JSONL item ids do not match tensor manifest item ids.")
    manifest_fingerprint = expected.get("data_fingerprint")
    if manifest_fingerprint is not None:
        data_fingerprint = fingerprint_data(data)
        if manifest_fingerprint != data_fingerprint:
            raise ValueError(
                "Prepared JSONL content does not match tensor manifest data_fingerprint "
                f"(prepared={data_fingerprint}, manifest={manifest_fingerprint})."
            )


def score_pair(arrays: Any, candidate_cell: str, query_cell: str) -> np.ndarray:
    candidates = np.asarray(arrays[f"{candidate_cell}::candidates"], dtype=np.float32)
    queries = np.asarray(arrays[f"{query_cell}::queries"], dtype=np.float32)
    mean, pcs = fit_anti_pca(candidates, components=15)
    candidate_repr = remove_pc_projection(candidates - mean, pcs)
    query_repr = remove_pc_projection(queries - mean, pcs)
    return normalize_rows(query_repr) @ normalize_rows(candidate_repr).T


def fit_anti_pca(candidates: np.ndarray, components: int) -> tuple[np.ndarray, np.ndarray]:
    mean = np.mean(candidates, axis=0).astype(np.float32, copy=False)
    centered = candidates - mean
    if centered.shape[0] < 2:
        return mean, np.zeros((0, candidates.shape[1]), dtype=np.float32)
    _u, _s, vt = np.linalg.svd(centered, full_matrices=False)
    pcs = vt[: min(components, vt.shape[0])].astype(np.float32, copy=False)
    return mean, pcs


def remove_pc_projection(vectors: np.ndarray, pcs: np.ndarray) -> np.ndarray:
    if pcs.size == 0:
        return vectors.astype(np.float32, copy=False)
    return (vectors - (vectors @ pcs.T) @ pcs).astype(np.float32, copy=False)


def normalize_rows(vectors: np.ndarray) -> np.ndarray:
    arr = np.asarray(vectors, dtype=np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-12)


def predictions_from_scores(scores: np.ndarray, data: dict[str, list[Any]]) -> list[dict[str, Any]]:
    predictions = []
    candidate_ids = data["candidate_ids"]
    for query_index, query_id in enumerate(data["query_ids"]):
        order = np.argsort(scores[query_index])[::-1]
        predictions.append(
            {
                "query_id": query_id,
                "retrieved_ids": [candidate_ids[int(index)] for index in order[:50]],
                "gold_ids": data["gold_ids"][query_index],
            }
        )
    return predictions


def summarize(predictions: list[dict[str, Any]]) -> dict[str, float]:
    summary: dict[str, float] = {}
    for k in [1, 3, 5, 10, 20, 50]:
        summary[f"recall@{k}"] = float(np.mean([recall_at_k(pred, k) for pred in predictions]))
        summary[f"ndcg@{k}"] = float(np.mean([ndcg_at_k(pred, k) for pred in predictions]))
    summary["mrr"] = mean_reciprocal_rank(predictions)
    return summary


def recall_at_k(prediction: dict[str, Any], k: int) -> float:
    return float(bool(set(prediction["gold_ids"]).intersection(prediction["retrieved_ids"][:k])))


def ndcg_at_k(prediction: dict[str, Any], k: int) -> float:
    gold = set(prediction["gold_ids"])
    seen_gold = False
    relevances = []
    for item in prediction["retrieved_ids"][:k]:
        if item in gold and not seen_gold:
            relevances.append(1.0)
            seen_gold = True
        else:
            relevances.append(0.0)
    relevances = np.asarray(relevances, dtype=np.float64)
    if relevances.size == 0:
        return 0.0
    discounts = np.log2(np.arange(2, relevances.size + 2))
    actual = float(np.sum(relevances / discounts))
    return actual


def mean_reciprocal_rank(predictions: list[dict[str, Any]]) -> float:
    values = []
    for prediction in predictions:
        gold = set(prediction["gold_ids"])
        rank = 0
        for index, item in enumerate(prediction["retrieved_ids"], start=1):
            if item in gold:
                rank = index
                break
        values.append(0.0 if rank == 0 else 1.0 / rank)
    return float(np.mean(values))


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def fingerprint_data(data: dict[str, list[Any]]) -> str:
    values = []
    for index, item_id in enumerate(data["candidate_ids"]):
        values.append(
            json.dumps(
                {
                    "item_id": item_id,
                    "preference": data["preferences"][index],
                    "question": data["questions"][index],
                    "topic": data["topics"][index],
                    "preference_type": data["preference_types"][index],
                    "query_id": data["query_ids"][index],
                    "gold_ids": data["gold_ids"][index],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    return short_hash(values)


def short_hash(values: list[str]) -> str:
    import hashlib

    return hashlib.sha1("\n".join(values).encode("utf-8")).hexdigest()[:10]


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# PrefEval 2-3 Asymmetric Probe",
        "",
        f"- Created UTC: `{payload['created_utc']}`",
        f"- Cache: `{payload['inputs']['cache_dir']}`",
        f"- Data: `{payload['inputs']['data_jsonl']}`",
        "",
        "| rank | config | R@1 | R@3 | R@5 | NDCG@5 | MRR |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(payload["rows"], start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | `{row['name']}` | {summary['recall@1']:.3f} | "
            f"{summary['recall@3']:.3f} | {summary['recall@5']:.3f} | "
            f"{summary['ndcg@5']:.3f} | {summary['mrr']:.3f} |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    raise SystemExit(main())
