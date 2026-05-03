"""LongMemEval retrieval metrics for Phase 1a.

MVP_Plan.md sections 4.2 and 8 specify that Phase 1a reports official-style
retrieval metrics rather than QA accuracy. The official LongMemEval code skips
abstention questions whose `question_id` contains `_abs` and also skips items
without user-side target labels. This module exposes those decisions explicitly
so subset and full-run numbers are comparable to the official anchor.

Why: testing hidden-state retrieval requires measuring whether the right
evidence session is ranked highly, independent of any downstream answer model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class Prediction:
    question_id: str
    retrieved_ids: list[str]
    gold_ids: list[str]
    is_abstention: bool
    has_target: bool


def recall_all_at_k(retrieved_ids: list[str], gold_ids: Iterable[str], k: int) -> float:
    gold = set(gold_ids)
    if not gold:
        return 0.0
    retrieved = set(retrieved_ids[:k])
    return float(gold.issubset(retrieved))


def ndcg_any_at_k(retrieved_ids: list[str], gold_ids: Iterable[str], k: int) -> float:
    gold = set(gold_ids)
    if not gold:
        return 0.0

    relevances = np.asarray([1.0 if doc_id in gold else 0.0 for doc_id in retrieved_ids[:k]])
    actual = _dcg(relevances)
    ideal_len = min(len(gold), k)
    ideal = _dcg(np.ones(ideal_len, dtype=np.float64))
    if ideal == 0.0:
        return 0.0
    return float(actual / ideal)


def evaluate(
    predictions: list[Prediction],
    skip_abstention: bool = True,
    bootstrap_samples: int = 1000,
    seed: int = 0,
    ks: tuple[int, ...] = (1, 3, 5, 10, 30, 50),
) -> dict[str, object]:
    """Evaluate predictions and return means plus bootstrap confidence intervals."""
    scored = [
        pred
        for pred in predictions
        if not (skip_abstention and pred.is_abstention) and pred.has_target and pred.gold_ids
    ]
    ignored_abstention = [pred.question_id for pred in predictions if skip_abstention and pred.is_abstention]
    ignored_no_target = [
        pred.question_id
        for pred in predictions
        if not pred.is_abstention and (not pred.has_target or not pred.gold_ids)
    ]

    if not scored:
        raise ValueError("No predictions left after official LongMemEval filtering.")

    metric_values: dict[str, list[float]] = {}
    for k in ks:
        metric_values[f"recall_all@{k}"] = [
            recall_all_at_k(pred.retrieved_ids, pred.gold_ids, k) for pred in scored
        ]
        metric_values[f"ndcg_any@{k}"] = [
            ndcg_any_at_k(pred.retrieved_ids, pred.gold_ids, k) for pred in scored
        ]

    metrics = {
        name: {
            "mean": float(np.mean(values)),
            "ci95": _bootstrap_ci(values, bootstrap_samples=bootstrap_samples, seed=seed),
        }
        for name, values in metric_values.items()
    }
    return {
        "n_total": len(predictions),
        "n_scored": len(scored),
        "ignored_abstention_count": len(ignored_abstention),
        "ignored_abstention_ids": ignored_abstention,
        "ignored_no_target_count": len(ignored_no_target),
        "ignored_no_target_ids": ignored_no_target,
        "metrics": metrics,
    }


def _dcg(relevances: np.ndarray) -> float:
    """Standard DCG: sum rel_i / log2(i + 1) for 1-indexed position i.

    `relevances[j]` is at 0-indexed position j, i.e. 1-indexed position j + 1,
    so its discount is log2((j + 1) + 1) = log2(j + 2).
    """
    if relevances.size == 0:
        return 0.0
    discounts = np.log2(np.arange(2, relevances.size + 2))
    return float(np.sum(relevances / discounts))


def _bootstrap_ci(values: list[float], bootstrap_samples: int, seed: int) -> dict[str, float]:
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 1 or bootstrap_samples <= 0:
        mean = float(np.mean(arr))
        return {"low": mean, "high": mean}

    rng = np.random.default_rng(seed)
    sample_means = []
    for _ in range(bootstrap_samples):
        sample = rng.choice(arr, size=arr.size, replace=True)
        sample_means.append(float(np.mean(sample)))
    low, high = np.percentile(sample_means, [2.5, 97.5])
    return {"low": float(low), "high": float(high)}
