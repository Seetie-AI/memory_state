"""Qwen3-Embedding baseline for Phase 1b.

MVP_Plan.md sections 5.2 and 8 define Qwen3-Embedding-0.6B as the fair modern
embedding comparator for LongMemEval-S. Unlike Contriever, this model supports
longer inputs and uses a decoder-style last-token pooling recipe.

Official Qwen3-Embedding model-card choices mirrored here:

- load `Qwen/Qwen3-Embedding-0.6B` from `./models/qwen3-embedding-0.6b/`;
- tokenizer padding side is left;
- query side uses an instruction, document side does not;
- pool with the last non-padding token;
- L2-normalize embeddings and score by dot product, equivalent to cosine;
- use `max_length=8192` as in the Transformers usage example, even though the
  model supports 32k context.

Why: this baseline avoids the Contriever 512-token truncation caveat documented
in MVP_Plan.md section 5.3 and gives Phase 2 a stronger local comparator on the
same LongMemEval-S setting.
"""

from __future__ import annotations

from pathlib import Path

import torch
import torch.nn.functional as F
from torch import Tensor
from torch.utils.data import DataLoader
from transformers import AutoModel, AutoTokenizer


DEFAULT_TASK_DESCRIPTION = (
    "Given a long-term chat memory question, retrieve the relevant conversation "
    "session that contains evidence needed to answer it"
)


class QwenEmbeddingRetriever:
    """Dense retriever using Qwen3-Embedding last-token pooling."""

    def __init__(
        self,
        model_path: str | Path = "models/qwen3-embedding-0.6b",
        batch_size: int = 4,
        max_length: int = 8192,
        task_description: str = DEFAULT_TASK_DESCRIPTION,
        device: str | None = None,
    ) -> None:
        self.model_path = str(model_path)
        self.batch_size = batch_size
        self.max_length = max_length
        self.task_description = task_description
        self.device = torch.device(device or ("mps" if torch.backends.mps.is_available() else "cpu"))
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            padding_side="left",
            trust_remote_code=False,
        )
        self.model = AutoModel.from_pretrained(
            self.model_path,
            dtype=torch.bfloat16,
            trust_remote_code=False,
            low_cpu_mem_usage=True,
        ).to(self.device)
        self.model.eval()
        self._doc_embeddings: torch.Tensor | None = None

    def fit(self, corpus_texts: list[str]) -> "QwenEmbeddingRetriever":
        self._doc_embeddings = self._encode(corpus_texts, is_query=False)
        return self

    def query(self, query_text: str, top_k: int) -> list[tuple[int, float]]:
        if self._doc_embeddings is None:
            raise RuntimeError("QwenEmbeddingRetriever.fit must be called before query.")
        query_embedding = self._encode([query_text], is_query=True)
        scores = (query_embedding @ self._doc_embeddings.T).squeeze(0)
        top_scores, top_indices = torch.topk(scores, k=min(top_k, scores.shape[0]))
        return [
            (int(index), float(score))
            for index, score in zip(top_indices.cpu().tolist(), top_scores.cpu().tolist(), strict=True)
        ]

    def _encode(self, texts: list[str], is_query: bool) -> torch.Tensor:
        if not texts:
            raise ValueError("Cannot encode an empty text list.")

        prepared = [self._format_query(text) for text in texts] if is_query else texts
        vectors: list[torch.Tensor] = []
        dataloader = DataLoader(prepared, batch_size=self.batch_size, shuffle=False)
        with torch.no_grad():
            for batch in dataloader:
                inputs = self.tokenizer(
                    list(batch),
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors="pt",
                )
                inputs = {key: value.to(self.device) for key, value in inputs.items()}
                outputs = self.model(**inputs)
                pooled = last_token_pool(outputs.last_hidden_state, inputs["attention_mask"])
                normalized = F.normalize(pooled, p=2, dim=1)
                vectors.append(normalized.detach().cpu())

        return torch.cat(vectors, dim=0)

    def _format_query(self, query: str) -> str:
        return f"Instruct: {self.task_description}\nQuery:{query}"


def last_token_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    """Official Qwen3-Embedding last-token pooling helper."""
    left_padding = attention_mask[:, -1].sum() == attention_mask.shape[0]
    if left_padding:
        return last_hidden_states[:, -1]

    sequence_lengths = attention_mask.sum(dim=1) - 1
    batch_size = last_hidden_states.shape[0]
    return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]

