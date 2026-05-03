"""Transformers hidden-state extraction for Phase 0 sanity checks.

This path is not the primary MVP implementation. It exists only to validate
that the mlx-lm wrapper extracts the same option-A prompt-final hidden state
from an independently implemented model loader. See MVP_Plan.md sections 3.2
and 6.3.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from transformers import AutoModelForCausalLM, AutoModelForImageTextToText, AutoTokenizer


@dataclass(frozen=True)
class HiddenStateResult:
    """Prompt-final hidden-state result used by the sanity-check script."""

    next_token_text: str
    vector: np.ndarray
    top_token_ids: list[int]
    top_token_texts: list[str]


class TransformersHiddenStateExtractor:
    """Extract option-A hidden-state vectors from a Transformers model."""

    def __init__(
        self,
        model_id: str,
        dtype: torch.dtype = torch.bfloat16,
        device: str | None = None,
    ) -> None:
        self.model_id = model_id
        self.dtype = dtype
        self.device = torch.device(device or ("mps" if torch.backends.mps.is_available() else "cpu"))
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=False)
        self.model = self._load_model(model_id, dtype)
        self.model.to(self.device)
        self.model.eval()
        self.base_model, self.output_head = self._detect_model_parts(self.model)

    @staticmethod
    def _load_model(model_id: str, dtype: torch.dtype) -> torch.nn.Module:
        load_kwargs = {
            "dtype": dtype,
            "trust_remote_code": False,
            "low_cpu_mem_usage": True,
        }
        try:
            return AutoModelForCausalLM.from_pretrained(model_id, **load_kwargs)
        except (KeyError, ValueError, OSError):
            return AutoModelForImageTextToText.from_pretrained(model_id, **load_kwargs)

    @staticmethod
    def _detect_model_parts(model: torch.nn.Module) -> tuple[Any, torch.nn.Module]:
        if hasattr(model, "language_model"):
            language_model = model.language_model
            base_model = getattr(language_model, "model", None)
            head = getattr(language_model, "lm_head", None)
            if base_model is not None and head is not None:
                return base_model, head

        if hasattr(model, "model"):
            output_head = model.get_output_embeddings()
            if output_head is None and hasattr(model, "lm_head"):
                output_head = model.lm_head
            if output_head is not None:
                return model.model, output_head

        raise TypeError(f"Unsupported Transformers model layout: {type(model)!r}")

    def encode_prompt(self, prompt: str, top_k: int = 5) -> HiddenStateResult:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}

        with torch.no_grad():
            outputs = self.base_model(**inputs, use_cache=False, return_dict=True)
            hidden = outputs.last_hidden_state
            logits = self.output_head(hidden)
            last_hidden = hidden[:, -1, :]
            last_logits = logits[:, -1, :]
            top_ids_tensor = torch.topk(last_logits, k=top_k, dim=-1).indices

        vector = last_hidden[0].detach().float().cpu().numpy().astype(np.float32)
        vector = _l2_normalize(vector)
        top_ids = [int(x) for x in top_ids_tensor[0].detach().cpu().tolist()]
        top_texts = [self.tokenizer.decode([token_id]) for token_id in top_ids]

        return HiddenStateResult(
            next_token_text=top_texts[0],
            vector=vector,
            top_token_ids=top_ids,
            top_token_texts=top_texts,
        )


def extract_hidden_state(model_id: str, prompt: str) -> tuple[str, np.ndarray]:
    """Return (next_token_text, l2-normalized prompt-final hidden vector)."""
    result = TransformersHiddenStateExtractor(model_id).encode_prompt(prompt)
    return result.next_token_text, result.vector


def _l2_normalize(vector: np.ndarray) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if norm == 0.0 or not np.isfinite(norm):
        raise ValueError("Cannot normalize hidden state with zero/non-finite norm.")
    return vector / norm
