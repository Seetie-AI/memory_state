"""Hidden-state retriever for the Phase 2 proposed method.

This implements MVP_Plan.md sections 3.1, 3.2, and 6.2:

- use the symmetric one-word summary prompt for both memory candidates and
  queries;
- take option A, the prompt-final post-norm hidden state that predicts the next
  summary token;
- use the mlx-lm wrapper rather than forking or monkey-patching mlx-lm.

Why symmetric prompts: memory and query vectors should be produced under the
same instruction suffix to reduce prompt-template artifacts.

Why option A: it is the cheapest single-forward definition and avoids measuring
the state after the model has already consumed its own generated token.

Why no batching: the user asked to keep memory use ideally below 10GB. Single
prompt forward passes are slower but keep Qwen3.5-2B fp16/bf16 peak memory
predictable on a 16GB Mac.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from hidden_state.mlx_wrapper import MLXHiddenStateExtractor


SUMMARY_PROMPT_SUFFIX = "\n请用一个词来summarize上面这段文字，这个词是：“"


class HiddenStateRetriever:
    """Retriever backed by Qwen3.5 prompt-final hidden states."""

    def __init__(self, model_path: str | Path = "models/Qwen3.5-2B-bf16") -> None:
        self.model_path = str(model_path)
        self.extractor = MLXHiddenStateExtractor(self.model_path)
        self._doc_embeddings: np.ndarray | None = None

    def fit(self, corpus_texts: list[str]) -> "HiddenStateRetriever":
        if not corpus_texts:
            raise ValueError("Cannot fit HiddenStateRetriever on an empty corpus.")

        vectors: list[np.ndarray] = []
        for index, text in enumerate(corpus_texts, start=1):
            prompt = memory_prompt(text)
            result = self.extractor.encode_prompt(prompt)
            vectors.append(np.array(result.vector, dtype=np.float32, copy=True))
            if index == 1 or index % 50 == 0 or index == len(corpus_texts):
                print(f"hidden_state fit progress: {index}/{len(corpus_texts)} candidates")

        self._doc_embeddings = np.vstack(vectors).astype(np.float32, copy=False)
        return self

    def query(self, query_text: str, top_k: int) -> list[tuple[int, float]]:
        if self._doc_embeddings is None:
            raise RuntimeError("HiddenStateRetriever.fit must be called before query.")

        query_result = self.extractor.encode_prompt(query_prompt(query_text))
        query_vector = np.array(query_result.vector, dtype=np.float32, copy=False)
        scores = query_vector @ self._doc_embeddings.T
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [(int(index), float(scores[index])) for index in top_indices]


def memory_prompt(text: str) -> str:
    return f"{text}{SUMMARY_PROMPT_SUFFIX}"


def query_prompt(query_text: str) -> str:
    return f"{query_text}{SUMMARY_PROMPT_SUFFIX}"

