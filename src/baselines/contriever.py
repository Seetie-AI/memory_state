"""Contriever baseline for Phase 1a LongMemEval replication.

MVP_Plan.md sections 5.1, 5.3, and 8 use Contriever as an official pipeline
anchor. This implementation follows the official LongMemEval behavior:

- load `facebook/contriever` from the repo-local `./models/contriever/` path;
- tokenize with `truncation=True` and `padding=True`;
- rely on the model default maximum length, effectively 512 tokens;
- mean-pool token embeddings with the attention mask;
- score by dot product.

Why: Contriever is not the fairest final comparator for long-context hidden
states, but matching official truncation and pooling behavior validates the
LongMemEval data/metric pipeline before Phase 2.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from transformers import AutoModel, AutoTokenizer


class ContrieverRetriever:
    """Dense retriever using facebook/contriever-style mean pooling."""

    def __init__(
        self,
        model_path: str | Path = "models/contriever",
        batch_size: int = 16,
        device: str | None = None,
    ) -> None:
        self.model_path = str(model_path)
        self.batch_size = batch_size
        self.device = torch.device(device or ("mps" if torch.backends.mps.is_available() else "cpu"))
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModel.from_pretrained(self.model_path).to(self.device)
        self.model.eval()
        self._doc_embeddings: torch.Tensor | None = None

    def fit(self, corpus_texts: list[str]) -> "ContrieverRetriever":
        self._doc_embeddings = self._encode(corpus_texts)
        return self

    def query(self, query_text: str, top_k: int) -> list[tuple[int, float]]:
        if self._doc_embeddings is None:
            raise RuntimeError("ContrieverRetriever.fit must be called before query.")
        query_embedding = self._encode([query_text])
        scores = (query_embedding @ self._doc_embeddings.T).squeeze(0)
        top_scores, top_indices = torch.topk(scores, k=min(top_k, scores.shape[0]))
        return [
            (int(index), float(score))
            for index, score in zip(top_indices.cpu().tolist(), top_scores.cpu().tolist(), strict=True)
        ]

    def _encode(self, texts: list[str]) -> torch.Tensor:
        if not texts:
            raise ValueError("Cannot encode an empty text list.")

        vectors: list[torch.Tensor] = []
        dataloader = DataLoader(texts, batch_size=self.batch_size, shuffle=False)
        with torch.no_grad():
            for batch in dataloader:
                inputs = self.tokenizer(
                    list(batch),
                    padding=True,
                    truncation=True,
                    return_tensors="pt",
                )
                inputs = {key: value.to(self.device) for key, value in inputs.items()}
                outputs = self.model(**inputs)
                pooled = mean_pool(outputs.last_hidden_state, inputs["attention_mask"])
                vectors.append(pooled.detach().cpu())

        return torch.cat(vectors, dim=0)


def mean_pool(token_embeddings: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    mask = attention_mask[..., None].bool()
    masked_embeddings = token_embeddings.masked_fill(~mask, 0.0)
    token_counts = attention_mask.sum(dim=1).clamp(min=1)[..., None]
    return masked_embeddings.sum(dim=1) / token_counts

