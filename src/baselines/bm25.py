"""BM25 baseline for Phase 1a LongMemEval replication.

MVP_Plan.md sections 5.1 and 8 define BM25 as an official-anchor baseline, not
the final fair comparator for the hidden-state method. The tokenizer here is
intentionally minimal: `text.split()`, with no lowercasing, stemming, or custom
normalization.

Why: the official LongMemEval retrieval script tokenizes BM25 inputs with
`split(" ")`. Matching that behavior is more important than improving BM25
quality during pipeline validation.
"""

from __future__ import annotations

import numpy as np
from rank_bm25 import BM25Okapi


class BM25Retriever:
    """Small per-query-corpus BM25 retriever."""

    def __init__(self) -> None:
        self._corpus_texts: list[str] = []
        self._bm25: BM25Okapi | None = None

    def fit(self, corpus_texts: list[str]) -> "BM25Retriever":
        self._corpus_texts = list(corpus_texts)
        # Official LongMemEval uses split(" ") exactly; split() would treat
        # repeated spaces and tabs differently and can shift BM25 scores.
        tokenized = [text.split(" ") for text in self._corpus_texts]
        self._bm25 = BM25Okapi(tokenized)
        return self

    def query(self, query_text: str, top_k: int) -> list[tuple[int, float]]:
        if self._bm25 is None:
            raise RuntimeError("BM25Retriever.fit must be called before query.")
        # Keep query tokenization identical to official run_retrieval.py.
        scores = np.asarray(self._bm25.get_scores(query_text.split(" ")), dtype=np.float64)
        order = np.argsort(scores)[::-1][:top_k]
        return [(int(index), float(scores[index])) for index in order]
