"""Evaluate a local embedding model on the Stage 3 LongMemEval round setup.

This script is the embedding-model counterpart to `stage3_prompt_sweep.py`.
It is intentionally separate because embedding models encode each text once;
they do not use prompt-suffix KV reuse, layer scans, hidden-state anti-PCA, or
top-logit storage. The evaluation target is still identical: LongMemEval-S
round/evidence retrieval with the same candidate IDs, strict `recall_all@5`,
and `ndcg_any@5` metrics.

Operational choices:
- Use `--subset-start` plus `--subset` so two machines can split a run without
  instance-index collisions.
- Store per-instance embeddings in small `.npz` chunks by default. Embeddings
  are cheap relative to the model run, and storing them prevents reruns.
- Write `manifest.json` atomically after every completed instance so a graceful
  interrupt preserves all finished instances.
- Keep memory bounded by encoding one instance at a time and controlling only
  `--batch-size`; no global candidate matrix is held during model inference.
- Default to the SentenceTransformers backend because NVIDIA
  llama-embed-nemotron-8b exposes `encode_query` / `encode_document`, matching
  its model-card retrieval recipe. A generic Transformers backend is included
  for Qwen-style last-token or average-pooling experiments.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from eval.longmemeval_metrics import Prediction, evaluate
from longmemeval.data import (
    Instance,
    has_round_side_answer_label,
    iter_round_candidates,
    load_instances,
)


DEFAULT_TASK_DESCRIPTION = (
    "Given a long-term chat memory question, retrieve the relevant conversation "
    "turn that contains evidence needed to answer it"
)


class EmbeddingBackend(Protocol):
    dim: int | None

    def encode_documents(self, texts: list[str]) -> np.ndarray:
        ...

    def encode_queries(self, texts: list[str]) -> np.ndarray:
        ...

    def memory_summary(self) -> str:
        ...


@dataclass(frozen=True)
class InstanceEmbeddingMetadata:
    instance_index: int
    question_id: str
    file: str
    candidate_ids: list[str]
    gold_ids: list[str]
    has_target: bool
    is_abstention: bool
    candidate_count: int


class EmbeddingStoreWriter:
    """Small per-instance embedding store with atomic manifest snapshots."""

    def __init__(
        self,
        output_dir: Path,
        *,
        model_path: str,
        backend: str,
        pooling: str,
        dtype: str,
        storage_dtype: str,
        normalize: bool,
        config: dict[str, Any],
    ) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        existing = list(self.output_dir.iterdir())
        if existing:
            raise FileExistsError(
                f"Refusing to write into non-empty output directory: {self.output_dir}. "
                "Choose a new --output-dir or remove the old run after review."
            )
        self.storage_dtype = np.float16 if storage_dtype == "float16" else np.float32
        self.manifest: dict[str, Any] = {
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "model_path": model_path,
            "backend": backend,
            "pooling": pooling,
            "dtype": dtype,
            "storage_dtype": storage_dtype,
            "normalize": normalize,
            "config": config,
            "embedding_dim": None,
            "instances": [],
        }

    def add_instance(
        self,
        metadata: InstanceEmbeddingMetadata,
        *,
        candidate_embeddings: np.ndarray,
        query_embedding: np.ndarray,
    ) -> None:
        candidate_embeddings = np.asarray(candidate_embeddings, dtype=np.float32)
        query_embedding = np.asarray(query_embedding, dtype=np.float32)
        if candidate_embeddings.ndim != 2:
            raise ValueError(f"candidate_embeddings must be 2D, got {candidate_embeddings.shape}")
        if query_embedding.ndim == 2 and query_embedding.shape[0] == 1:
            query_embedding = query_embedding[0]
        if query_embedding.ndim != 1:
            raise ValueError(f"query_embedding must be 1D, got {query_embedding.shape}")
        if candidate_embeddings.shape[1] != query_embedding.shape[0]:
            raise ValueError(
                "candidate/query embedding dims differ: "
                f"{candidate_embeddings.shape[1]} vs {query_embedding.shape[0]}"
            )
        if len(metadata.candidate_ids) != candidate_embeddings.shape[0]:
            raise ValueError(
                f"{metadata.question_id} candidate id count {len(metadata.candidate_ids)} "
                f"!= embedding rows {candidate_embeddings.shape[0]}"
            )

        if self.manifest["embedding_dim"] is None:
            self.manifest["embedding_dim"] = int(query_embedding.shape[0])
        elif int(self.manifest["embedding_dim"]) != int(query_embedding.shape[0]):
            raise ValueError("embedding dimension changed during run")

        np.savez(
            self.output_dir / metadata.file,
            candidate_embeddings=candidate_embeddings.astype(self.storage_dtype, copy=False),
            query_embedding=query_embedding.astype(self.storage_dtype, copy=False),
        )
        self.manifest["instances"].append(asdict(metadata))
        self.write_manifest()

    def write_manifest(self) -> None:
        target = self.output_dir / "manifest.json"
        tmp = self.output_dir / "manifest.json.tmp"
        tmp.write_text(json.dumps(self.manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, target)


class SentenceTransformerBackend:
    """SentenceTransformers backend for Nemotron-style embedding models."""

    def __init__(
        self,
        model_path: str,
        *,
        batch_size: int,
        device: str | None,
        dtype: str,
        task_description: str,
        trust_remote_code: bool,
        normalize: bool,
    ) -> None:
        import torch
        from sentence_transformers import SentenceTransformer

        torch_dtype = dtype_to_torch(dtype)
        model_kwargs: dict[str, Any] = {"torch_dtype": torch_dtype}
        # Eager attention is the portable choice on Mac/MPS/CPU. CUDA users can
        # explicitly set ATTENTION_IMPLEMENTATION=flash_attention_2 if installed.
        attn_impl = os.environ.get("ATTENTION_IMPLEMENTATION", "eager")
        model_kwargs["attn_implementation"] = attn_impl
        tokenizer_kwargs = {"padding_side": "left"}
        self.model = SentenceTransformer(
            model_path,
            trust_remote_code=trust_remote_code,
            device=device,
            model_kwargs=model_kwargs,
            tokenizer_kwargs=tokenizer_kwargs,
        )
        self.batch_size = batch_size
        self.task_description = task_description
        self.normalize = normalize
        self.dim: int | None = None

    def encode_documents(self, texts: list[str]) -> np.ndarray:
        if hasattr(self.model, "encode_document"):
            output = self.model.encode_document(
                texts,
                batch_size=self.batch_size,
                convert_to_numpy=True,
                normalize_embeddings=self.normalize,
                show_progress_bar=False,
            )
        else:
            output = self.model.encode(
                texts,
                batch_size=self.batch_size,
                convert_to_numpy=True,
                normalize_embeddings=self.normalize,
                show_progress_bar=False,
            )
        return self._finalize(output)

    def encode_queries(self, texts: list[str]) -> np.ndarray:
        if hasattr(self.model, "encode_query"):
            output = self.model.encode_query(
                texts,
                batch_size=self.batch_size,
                convert_to_numpy=True,
                normalize_embeddings=self.normalize,
                show_progress_bar=False,
            )
        else:
            prepared = [format_query(self.task_description, text) for text in texts]
            output = self.model.encode(
                prepared,
                batch_size=self.batch_size,
                convert_to_numpy=True,
                normalize_embeddings=self.normalize,
                show_progress_bar=False,
            )
        return self._finalize(output)

    def _finalize(self, embeddings: Any) -> np.ndarray:
        arr = np.asarray(embeddings, dtype=np.float32)
        if arr.ndim == 1:
            arr = arr[None, :]
        if self.normalize:
            arr = normalize_rows(arr)
        self.dim = int(arr.shape[1])
        return arr

    def memory_summary(self) -> str:
        return ""


class TransformersBackend:
    """Generic AutoModel backend with configurable pooling.

    This backend mirrors the local Qwen3-Embedding-0.6B baseline for last-token
    pooling, while also supporting Nemotron's documented average pooling.
    """

    def __init__(
        self,
        model_path: str,
        *,
        batch_size: int,
        max_length: int,
        device: str | None,
        dtype: str,
        pooling: str,
        task_description: str,
        trust_remote_code: bool,
        normalize: bool,
    ) -> None:
        import torch
        from transformers import AutoModel, AutoTokenizer

        self.torch = torch
        self.batch_size = batch_size
        self.max_length = max_length
        self.pooling = pooling
        self.task_description = task_description
        self.normalize = normalize
        self.device = torch.device(device or auto_torch_device())
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            padding_side="left",
            trust_remote_code=trust_remote_code,
        )
        self.model = AutoModel.from_pretrained(
            model_path,
            trust_remote_code=trust_remote_code,
            torch_dtype=dtype_to_torch(dtype),
            low_cpu_mem_usage=True,
        ).to(self.device)
        self.model.eval()
        self.dim: int | None = None

    def encode_documents(self, texts: list[str]) -> np.ndarray:
        return self._encode(texts)

    def encode_queries(self, texts: list[str]) -> np.ndarray:
        return self._encode([format_query(self.task_description, text) for text in texts])

    def _encode(self, texts: list[str]) -> np.ndarray:
        import torch.nn.functional as F

        vectors = []
        with self.torch.no_grad():
            for start in range(0, len(texts), self.batch_size):
                batch = texts[start : start + self.batch_size]
                inputs = self.tokenizer(
                    batch,
                    padding=True,
                    truncation=True,
                    max_length=self.max_length,
                    return_tensors="pt",
                )
                inputs = {key: value.to(self.device) for key, value in inputs.items()}
                outputs = self.model(**inputs)
                if self.pooling == "mean":
                    pooled = mean_pool(outputs.last_hidden_state, inputs["attention_mask"])
                elif self.pooling == "last_token":
                    pooled = last_token_pool(outputs.last_hidden_state, inputs["attention_mask"])
                else:
                    raise ValueError(f"Unsupported pooling: {self.pooling}")
                if self.normalize:
                    pooled = F.normalize(pooled.to(self.torch.float32), p=2, dim=1)
                vectors.append(pooled.detach().cpu().to(self.torch.float32).numpy())
        arr = np.concatenate(vectors, axis=0).astype(np.float32, copy=False)
        self.dim = int(arr.shape[1])
        return arr

    def memory_summary(self) -> str:
        return ""


class MLXBackend:
    """MLX backend for local 4-bit Qwen3-Embedding conversions.

    The downloaded `mlx-community/Qwen3-Embedding-8B-4bit-DWQ` checkpoint is an
    MLX CausalLM-style model, not a PyTorch SentenceTransformers checkpoint.
    Qwen3-Embedding uses last-token pooling, so this backend forwards one text
    at a time, pools the final hidden state, L2-normalizes it, and stores the
    result as a normal dense embedding.
    """

    def __init__(
        self,
        model_path: str,
        *,
        pooling: str,
        task_description: str,
        normalize: bool,
        clear_cache_every: str,
    ) -> None:
        if pooling not in {"last_token", "mean"}:
            raise ValueError(f"MLX backend supports last_token/mean pooling, got {pooling!r}")
        import mlx.core as mx
        from mlx_lm import load

        self.mx = mx
        self.model, self.tokenizer = load(model_path)
        self.base_model = detect_mlx_base_model(self.model)
        self.pooling = pooling
        self.task_description = task_description
        self.normalize = normalize
        self.clear_cache_every = clear_cache_every
        self.dim: int | None = None

    def encode_documents(self, texts: list[str]) -> np.ndarray:
        return self._encode(texts)

    def encode_queries(self, texts: list[str]) -> np.ndarray:
        return self._encode([format_query(self.task_description, text) for text in texts])

    def _encode(self, texts: list[str]) -> np.ndarray:
        vectors = []
        for text in texts:
            token_ids = self.tokenizer.encode(text)
            if not token_ids:
                # Keep shape stable for rare empty strings; a newline tokenizes
                # under Qwen tokenizers and is semantically close to "blank".
                token_ids = self.tokenizer.encode("\n")
            input_ids = self.mx.array([token_ids], dtype=self.mx.int32)
            hidden = self.base_model(input_ids)
            hidden = hidden.astype(self.mx.float32)
            if self.pooling == "last_token":
                pooled = hidden[:, -1, :]
            else:
                pooled = self.mx.mean(hidden, axis=1)
            if self.normalize:
                norm = self.mx.maximum(self.mx.linalg.norm(pooled, axis=1, keepdims=True), 1e-12)
                pooled = pooled / norm
            self.mx.eval(pooled)
            vector = np.array(pooled[0], dtype=np.float32)
            if not np.all(np.isfinite(vector)):
                raise ValueError("Non-finite MLX embedding vector.")
            vectors.append(vector)
            if self.clear_cache_every == "text":
                clear_mlx_cache(self.mx)
        if self.clear_cache_every == "instance":
            clear_mlx_cache(self.mx)
        arr = np.stack(vectors, axis=0).astype(np.float32, copy=False)
        self.dim = int(arr.shape[1])
        return arr

    def memory_summary(self) -> str:
        return mlx_memory_summary(self.mx)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--data", default=str(ROOT / "data" / "longmemeval_s_cleaned.json"))
    parser.add_argument("--subset-start", type=int, default=0)
    parser.add_argument("--subset", type=int, default=100)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--backend", choices=["sentence-transformers", "transformers", "mlx"], default="sentence-transformers")
    parser.add_argument("--pooling", choices=["mean", "last_token"], default="mean")
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--max-length", type=int, default=4096)
    parser.add_argument("--dtype", choices=["float32", "float16", "bfloat16"], default="float16")
    parser.add_argument("--device", default=None, help="torch device, e.g. cpu, mps, cuda:0. Default: auto.")
    parser.add_argument("--trust-remote-code", action="store_true", default=True)
    parser.add_argument("--no-trust-remote-code", dest="trust_remote_code", action="store_false")
    parser.add_argument("--no-normalize", dest="normalize", action="store_false", default=True)
    parser.add_argument("--storage-dtype", choices=["float16", "float32"], default="float16")
    parser.add_argument("--task-description", default=DEFAULT_TASK_DESCRIPTION)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--result-path", default=None)
    parser.add_argument("--min-free-gb", type=float, default=10.0)
    parser.add_argument("--dry-run", action="store_true", help="Count work and estimate storage without loading model.")
    parser.add_argument(
        "--mlx-clear-cache-every",
        choices=["text", "instance", "never"],
        default="instance",
        help="MLX backend only: clear reusable Metal cache after each text, instance, or never.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    model_path = Path(args.model_path)
    all_instances = load_instances(args.data)
    if args.subset_start < 0:
        raise ValueError(f"--subset-start must be >= 0, got {args.subset_start}")
    if args.subset_start >= len(all_instances):
        raise ValueError(f"--subset-start {args.subset_start} outside dataset length {len(all_instances)}")
    indexed_instances = list(enumerate(all_instances))
    if args.subset and args.subset > 0:
        indexed_instances = indexed_instances[args.subset_start : args.subset_start + args.subset]
    else:
        indexed_instances = indexed_instances[args.subset_start :]

    output_dir, result_path = result_paths(args, model_path)
    candidate_rows = sum(len(iter_round_candidates(instance)) for _idx, instance in indexed_instances)
    query_rows = len(indexed_instances)
    estimated_store_bytes = estimate_store_bytes(
        rows=candidate_rows + query_rows,
        embedding_dim=4096,
        storage_dtype=args.storage_dtype,
    )
    check_storage_budget(output_dir, estimated_store_bytes, args.min_free_gb)

    print(
        f"instances={len(indexed_instances)} candidates={candidate_rows} "
        f"queries={query_rows} estimated_store={estimated_store_bytes / 1024**2:.1f}MiB"
    )
    if args.dry_run:
        print("dry-run complete; model not loaded")
        return 0

    backend = make_backend(args, str(model_path))
    writer = EmbeddingStoreWriter(
        output_dir,
        model_path=str(model_path),
        backend=args.backend,
        pooling=args.pooling,
        dtype=args.dtype,
        storage_dtype=args.storage_dtype,
        normalize=args.normalize,
        config={
            "data": args.data,
            "subset_start": args.subset_start,
            "subset": args.subset,
            "selected_instance_indices": [idx for idx, _instance in indexed_instances],
            "top_k": args.top_k,
            "bootstrap_samples": args.bootstrap_samples,
            "batch_size": args.batch_size,
            "max_length": args.max_length,
            "mlx_clear_cache_every": args.mlx_clear_cache_every,
            "task_description": args.task_description,
        },
    )

    predictions: list[Prediction] = []
    timing = {"document_encode_s": 0.0, "query_encode_s": 0.0, "scoring_s": 0.0, "writer_s": 0.0}
    start_time = time.monotonic()
    stop_requested = False

    def handle_stop(signum: int, _frame: Any) -> None:
        nonlocal stop_requested
        print(f"\nreceived signal {signum}; stopping after current operation")
        stop_requested = True

    for stop_signal in (signal.SIGINT, signal.SIGTERM):
        signal.signal(stop_signal, handle_stop)

    for local_index, (instance_index, instance) in enumerate(indexed_instances):
        candidates = iter_round_candidates(instance)
        candidate_ids = [candidate_id for candidate_id, _text, _is_gold in candidates]
        candidate_texts = [text for _candidate_id, text, _is_gold in candidates]
        gold_ids = [candidate_id for candidate_id, _text, is_gold in candidates if is_gold]
        has_target = has_round_side_answer_label(instance)

        doc_started = time.perf_counter()
        candidate_embeddings = backend.encode_documents(candidate_texts)
        timing["document_encode_s"] += time.perf_counter() - doc_started

        query_started = time.perf_counter()
        query_embedding = backend.encode_queries([instance.question])
        timing["query_encode_s"] += time.perf_counter() - query_started

        scoring_started = time.perf_counter()
        scores = (query_embedding[0].astype(np.float32) @ candidate_embeddings.astype(np.float32).T)
        top_indices = np.argsort(-scores)[: min(args.top_k, len(scores))]
        retrieved_ids = [candidate_ids[int(index)] for index in top_indices]
        predictions.append(
            Prediction(
                question_id=instance.question_id,
                retrieved_ids=retrieved_ids,
                gold_ids=gold_ids,
                is_abstention=instance.is_abstention,
                has_target=has_target,
            )
        )
        timing["scoring_s"] += time.perf_counter() - scoring_started

        writer_started = time.perf_counter()
        writer.add_instance(
            InstanceEmbeddingMetadata(
                instance_index=instance_index,
                question_id=instance.question_id,
                file=f"instance_{instance_index:04d}.npz",
                candidate_ids=candidate_ids,
                gold_ids=gold_ids,
                has_target=has_target,
                is_abstention=instance.is_abstention,
                candidate_count=len(candidate_ids),
            ),
            candidate_embeddings=candidate_embeddings,
            query_embedding=query_embedding,
        )
        timing["writer_s"] += time.perf_counter() - writer_started

        elapsed = time.monotonic() - start_time
        done = local_index + 1
        rate = done / max(elapsed, 1e-9)
        remaining = (len(indexed_instances) - done) / max(rate, 1e-9)
        print(
            f"processed {done}/{len(indexed_instances)} instances "
            f"(global {instance_index}) elapsed {format_duration(elapsed)} "
            f"ETA {format_duration(remaining)} {backend.memory_summary()}".rstrip()
        )
        if stop_requested:
            print("stop requested; exiting after completed instance")
            break

    metrics = evaluate(
        predictions,
        skip_abstention=True,
        bootstrap_samples=args.bootstrap_samples,
    )
    total_runtime_s = time.monotonic() - start_time
    payload = {
        "stage": "stage3_embedding_eval",
        "config": {
            "model_path": str(model_path),
            "data": args.data,
            "subset_start": args.subset_start,
            "subset": args.subset,
            "selected_instance_indices": [idx for idx, _instance in indexed_instances],
            "backend": args.backend,
            "pooling": args.pooling,
            "batch_size": args.batch_size,
            "max_length": args.max_length,
            "dtype": args.dtype,
            "device": args.device,
            "mlx_clear_cache_every": args.mlx_clear_cache_every,
            "storage_dtype": args.storage_dtype,
            "normalize": args.normalize,
            "task_description": args.task_description,
            "output_dir": str(output_dir),
        },
        "timing": {
            "total_runtime_s": total_runtime_s,
            "seconds": timing,
            "percent": {key: value / max(total_runtime_s, 1e-9) for key, value in timing.items()},
        },
        "metrics": metrics,
        "predictions": [asdict(prediction) for prediction in predictions],
    }
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    recall5 = metrics["metrics"]["recall_all@5"]["mean"]
    ndcg5 = metrics["metrics"]["ndcg_any@5"]["mean"]
    print("\nStage 3 embedding eval complete")
    print(f"instances: {len(predictions)}")
    print(f"Recall@5: {recall5:.3f}")
    print(f"NDCG@5: {ndcg5:.3f}")
    print(f"embedding_dir: {output_dir}")
    print(f"result file: {result_path}")
    return 0


def make_backend(args: argparse.Namespace, model_path: str) -> EmbeddingBackend:
    if args.backend == "sentence-transformers":
        device = args.device or auto_torch_device()
        return SentenceTransformerBackend(
            model_path,
            batch_size=args.batch_size,
            device=device,
            dtype=args.dtype,
            task_description=args.task_description,
            trust_remote_code=args.trust_remote_code,
            normalize=args.normalize,
        )
    if args.backend == "transformers":
        device = args.device or auto_torch_device()
        return TransformersBackend(
            model_path,
            batch_size=args.batch_size,
            max_length=args.max_length,
            device=device,
            dtype=args.dtype,
            pooling=args.pooling,
            task_description=args.task_description,
            trust_remote_code=args.trust_remote_code,
            normalize=args.normalize,
        )
    if args.backend == "mlx":
        return MLXBackend(
            model_path,
            pooling=args.pooling,
            task_description=args.task_description,
            normalize=args.normalize,
            clear_cache_every=args.mlx_clear_cache_every,
        )
    raise ValueError(f"Unsupported backend: {args.backend}")


def result_paths(args: argparse.Namespace, model_path: Path) -> tuple[Path, Path]:
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        model_label = model_path.name.replace("/", "_")
        subset_end = args.subset_start + args.subset if args.subset and args.subset > 0 else "full"
        output_dir = (
            ROOT
            / "tensors"
            / "stage3"
            / "embedding_eval"
            / f"{model_label}_subset{args.subset_start}-{subset_end}_{args.backend}_{args.pooling}"
        )
    if args.result_path:
        result_path = Path(args.result_path)
    else:
        result_path = ROOT / "results" / "stage3" / "embedding_eval" / f"{output_dir.name}.json"
    return output_dir, result_path


def format_query(task_description: str, query: str) -> str:
    return f"Instruct: {task_description}\nQuery: {query}"


def normalize_rows(arr: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-12)
    return arr / norms


def mean_pool(last_hidden_states: Any, attention_mask: Any) -> Any:
    import torch

    states = last_hidden_states.to(torch.float32)
    mask = attention_mask[..., None].bool()
    states = states.masked_fill(~mask, 0.0)
    return states.sum(dim=1) / attention_mask.sum(dim=1)[..., None].clamp_min(1)


def last_token_pool(last_hidden_states: Any, attention_mask: Any) -> Any:
    import torch

    left_padding = attention_mask[:, -1].sum() == attention_mask.shape[0]
    if left_padding:
        return last_hidden_states[:, -1]
    sequence_lengths = attention_mask.sum(dim=1) - 1
    return last_hidden_states[torch.arange(last_hidden_states.shape[0], device=last_hidden_states.device), sequence_lengths]


def dtype_to_torch(dtype: str) -> Any:
    import torch

    if dtype == "float32":
        return torch.float32
    if dtype == "float16":
        return torch.float16
    if dtype == "bfloat16":
        return torch.bfloat16
    raise ValueError(f"Unsupported dtype: {dtype}")


def auto_torch_device() -> str:
    import torch

    if torch.cuda.is_available():
        return "cuda:0"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def detect_mlx_base_model(model: Any) -> Any:
    if hasattr(model, "language_model"):
        language_model = model.language_model
        base_model = getattr(language_model, "model", None)
        if base_model is not None:
            return base_model
    if hasattr(model, "model"):
        return model.model
    raise TypeError(f"Unsupported MLX model layout: {type(model)!r}")


def clear_mlx_cache(mx: Any) -> None:
    try:
        if hasattr(mx, "clear_cache"):
            mx.clear_cache()
        elif hasattr(mx, "metal") and hasattr(mx.metal, "clear_cache"):
            mx.metal.clear_cache()
    except Exception:
        pass


def mlx_memory_summary(mx: Any) -> str:
    try:
        if hasattr(mx, "get_active_memory"):
            active = mx.get_active_memory()
            peak = mx.get_peak_memory() if hasattr(mx, "get_peak_memory") else 0
            cache = mx.get_cache_memory() if hasattr(mx, "get_cache_memory") else 0
        elif hasattr(mx, "metal"):
            active = mx.metal.get_active_memory()
            peak = mx.metal.get_peak_memory()
            cache = mx.metal.get_cache_memory()
        else:
            return ""
        return (
            f"metal_mem active {active / 1024**3:.2f}GiB "
            f"cache {cache / 1024**3:.2f}GiB peak {peak / 1024**3:.2f}GiB"
        )
    except Exception:
        return ""


def estimate_store_bytes(rows: int, embedding_dim: int, storage_dtype: str) -> int:
    bytes_per_value = 2 if storage_dtype == "float16" else 4
    return rows * embedding_dim * bytes_per_value


def check_storage_budget(output_dir: Path, estimated_bytes: int, min_free_gb: float) -> None:
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    stat = os.statvfs(output_dir.parent)
    free_bytes = stat.f_bavail * stat.f_frsize
    if free_bytes - estimated_bytes < min_free_gb * 1024**3:
        raise RuntimeError(
            f"Refusing run: estimated output {estimated_bytes / 1024**3:.2f}GiB would leave "
            f"{(free_bytes - estimated_bytes) / 1024**3:.2f}GiB free, below --min-free-gb={min_free_gb}."
        )


def format_duration(seconds: float) -> str:
    seconds_int = max(int(seconds), 0)
    minutes, seconds_rem = divmod(seconds_int, 60)
    hours, minutes_rem = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minutes_rem:02d}m{seconds_rem:02d}s"
    if minutes:
        return f"{minutes}m{seconds_rem:02d}s"
    return f"{seconds_rem}s"


if __name__ == "__main__":
    raise SystemExit(main())
