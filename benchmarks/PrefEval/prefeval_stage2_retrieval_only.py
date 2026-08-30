"""PrefEval Stage 2 retrieval-only benchmark.

This stage uses official PrefEval distractor turns to build a per-query memory
store:

- one target preference memory from the current row;
- shared distractor chunks from `filtered_inter_turns.json`.

It evaluates whether the target memory ranks above distractors. Unlike Stage 1,
it never searches across unrelated benchmark users' target preferences.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from rank_bm25 import BM25Okapi

import prefeval_benchmark as base
import prefeval_stage1_offline as offline


BENCH_DIR = Path(__file__).resolve().parent
ROOT = BENCH_DIR.parents[1]
DEFAULT_PREPARED_JSONL = (
    BENCH_DIR
    / "data"
    / "implicit_persona_n1000_pruned_hidden_l28_l29_l30_l31_logits256_promptreps128_20260512.jsonl"
)
DEFAULT_DISTRACTOR_JSON = BENCH_DIR / "data" / "official" / "filtered_inter_turns.json"
DEFAULT_OUTPUT_DIR = BENCH_DIR / "results" / "prefeval_stage2"
DEFAULT_MAIN_TENSOR = (
    BENCH_DIR
    / "tensors"
    / "hidden_implicit_persona_n1000_a3f7b8b21e_59d5500483_41ed8fec5e_logits256_promptreps1x128"
)
DEFAULT_EXTRA_TENSOR = (
    BENCH_DIR
    / "tensors"
    / "hidden_implicit_persona_n1000_a3f7b8b21e_3eda71273c_ab153df708_logits0_promptreps0x128"
)

DEFAULT_CELLS = (
    offline.DenseCellSpec("2-3-1_L30_both_k15", "2-3-1", 30, "anti_pca_both", 15, "key"),
    offline.DenseCellSpec("2-5_L29_both_k15", "2-5", 29, "anti_pca_both", 15, "association"),
    offline.DenseCellSpec("2-1-2_L30_both_k15", "2-1-2", 30, "anti_pca_both", 15, "topic"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared-jsonl", default=str(DEFAULT_PREPARED_JSONL))
    parser.add_argument("--distractor-json", default=str(DEFAULT_DISTRACTOR_JSON))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=None)
    parser.add_argument("--limit", type=int, default=0, help="0 means all rows.")
    parser.add_argument("--turns", type=int, default=300)
    parser.add_argument("--chunk-size", type=int, default=10, help="Messages per distractor chunk.")
    parser.add_argument("--stride", type=int, default=5, help="Message stride between distractor chunks.")
    parser.add_argument(
        "--retrievers",
        default="bm25",
        help="Comma list: bm25,hidden_singles,k3_vector_average,k3_zsum,k3_bm25.",
    )
    parser.add_argument(
        "--tensor-dir",
        action="append",
        default=None,
        help="Stage 1 hidden tensor dirs. Defaults to main + Stage 1.1 supplement tensor dirs.",
    )
    parser.add_argument("--hidden-model-path", default=str(base.DEFAULT_HIDDEN_MODEL))
    parser.add_argument("--bm25-weight", type=float, default=0.10)
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--bootstrap-samples", type=int, default=0)
    parser.add_argument("--synthetic-smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--resume", action="store_true", default=True)
    parser.add_argument("--clear-cache-every", choices=["never", "text"], default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    data = offline.load_prepared_jsonl(Path(args.prepared_jsonl))
    if args.limit and args.limit > 0:
        data = limit_data(data, args.limit)
    distractor_messages = load_distractor_messages(Path(args.distractor_json), turns=args.turns)
    distractor_chunks = chunk_messages(distractor_messages, chunk_size=args.chunk_size, stride=args.stride)
    if not distractor_chunks:
        raise ValueError("No distractor chunks built.")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_prefix or default_prefix(args)
    json_path = output_dir / f"{prefix}.json"
    md_path = output_dir / f"{prefix}.md"
    if not args.overwrite:
        existing = [path for path in (json_path, md_path) if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite: {existing}")

    retrievers = [item.strip() for item in args.retrievers.split(",") if item.strip()]
    rows = []
    details: dict[str, Any] = {
        "distractor_preview": distractor_chunks[:2],
        "cells": [dense_cell_to_json(spec) for spec in DEFAULT_CELLS],
    }

    base.log(
        f"PrefEval Stage 2 retrieval-only items={len(data.items)} turns={args.turns} "
        f"chunks={len(distractor_chunks)} retrievers={retrievers}"
    )

    bm25_scores = None
    if any(name in retrievers for name in ("bm25", "k3_bm25")):
        bm25_scores = score_bm25_stage2(data, distractor_chunks)
        rows.append(evaluate_stage2_scores("bm25", "BM25 over target+distractor chunks", bm25_scores, data, len(distractor_chunks)))

    hidden_outputs = None
    if any(name in retrievers for name in ("hidden_singles", "k3_vector_average", "k3_zsum", "k3_bm25")):
        hidden_outputs = score_hidden_stage2(data, distractor_chunks, args)

    if hidden_outputs and "hidden_singles" in retrievers:
        for name, item in hidden_outputs["single_scores"].items():
            rows.append(evaluate_stage2_scores(f"single_{name}", f"Stage 2 single hidden prompt {name}", item, data, len(distractor_chunks)))

    if hidden_outputs and "k3_vector_average" in retrievers:
        rows.append(
            evaluate_stage2_scores(
                "k3_vector_average",
                "K3 vector average over 2-3-1 + 2-5 + 2-1-2",
                hidden_outputs["k3_vector_average"],
                data,
                len(distractor_chunks),
            )
        )

    if hidden_outputs and "k3_zsum" in retrievers:
        rows.append(
            evaluate_stage2_scores(
                "k3_zsum",
                "K3 z-score sum over 2-3-1 + 2-5 + 2-1-2",
                hidden_outputs["k3_zsum"],
                data,
                len(distractor_chunks),
            )
        )

    if hidden_outputs and "k3_bm25" in retrievers:
        if bm25_scores is None:
            bm25_scores = score_bm25_stage2(data, distractor_chunks)
        fused = fuse_stage2_subset_scores(
            hidden_outputs["k3_vector_average"],
            bm25_scores,
            target_count=len(data.items),
            distractor_count=len(distractor_chunks),
            dense_weight=1.0 - args.bm25_weight,
        )
        rows.append(
            evaluate_stage2_scores(
                f"k3_vector_average_bm25_b{args.bm25_weight:.2f}",
                "K3 vector average + BM25 subset z-fusion",
                fused,
                data,
                len(distractor_chunks),
            )
        )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "prefeval_stage2_retrieval_only",
        "inputs": {
            "prepared_jsonl": str(Path(args.prepared_jsonl)),
            "distractor_json": str(Path(args.distractor_json)),
            "distractor_sha1": file_sha1(Path(args.distractor_json)),
            "limit": args.limit,
            "turns": args.turns,
            "chunk_size": args.chunk_size,
            "stride": args.stride,
            "retrievers": retrievers,
            "tensor_dirs": tensor_dirs(args),
            "hidden_model_path": str(args.hidden_model_path),
            "synthetic_smoke": bool(args.synthetic_smoke),
        },
        "task_summary": {
            "items": len(data.items),
            "target_memories_per_query": 1,
            "distractor_chunks_per_query": len(distractor_chunks),
            "candidate_pool_per_query": 1 + len(distractor_chunks),
        },
        "rows": sorted(rows, key=lambda row: (row["summary"]["recall@5"], row["summary"]["mrr"]), reverse=True),
        "details": details,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    base.log(f"wrote {json_path}")
    base.log(f"wrote {md_path}")
    print(render_short_table(payload))
    return 0


def limit_data(data: base.BenchmarkData, limit: int) -> base.BenchmarkData:
    n = min(limit, len(data.items))
    return base.BenchmarkData(
        task=data.task,
        dataset_id=data.dataset_id,
        items=data.items[:n],
        candidate_ids=data.candidate_ids[:n],
        candidate_texts=data.candidate_texts[:n],
        query_ids=data.query_ids[:n],
        query_texts=data.query_texts[:n],
        gold_ids_by_query=data.gold_ids_by_query[:n],
    )


def load_distractor_messages(path: Path, *, turns: int) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    messages = []
    for conversation in payload:
        for message in conversation.get("conversation", []):
            role = base.clean_text(message.get("role", ""))
            content = base.clean_text(message.get("content", ""))
            if role and content:
                messages.append({"role": role, "content": content})
            if len(messages) >= turns * 2:
                return messages
    return messages


def chunk_messages(messages: list[dict[str, str]], *, chunk_size: int, stride: int) -> list[str]:
    if chunk_size <= 0 or stride <= 0:
        raise ValueError("chunk_size and stride must be positive.")
    chunks = []
    for start in range(0, max(len(messages) - chunk_size + 1, 0), stride):
        window = messages[start : start + chunk_size]
        text = "\n".join(f"{item['role']}: {item['content']}" for item in window)
        chunks.append(text)
    if not chunks and messages:
        chunks.append("\n".join(f"{item['role']}: {item['content']}" for item in messages))
    return chunks


def score_bm25_stage2(data: base.BenchmarkData, distractor_chunks: list[str]) -> np.ndarray:
    corpus = data.candidate_texts + distractor_chunks
    tokenized = [text.split(" ") for text in corpus]
    bm25 = BM25Okapi(tokenized)
    scores = np.zeros((len(data.query_texts), len(corpus)), dtype=np.float32)
    for index, query in enumerate(data.query_texts, start=1):
        scores[index - 1] = np.asarray(bm25.get_scores(query.split(" ")), dtype=np.float32)
        if index == 1 or index == len(data.query_texts) or index % 100 == 0:
            base.log(f"  stage2 bm25 {index}/{len(data.query_texts)}")
    return scores


def score_hidden_stage2(data: base.BenchmarkData, distractor_chunks: list[str], args: argparse.Namespace) -> dict[str, Any]:
    raw_distractors = load_or_encode_distractor_hidden(distractor_chunks, args)
    single_scores: dict[str, np.ndarray] = {}
    transformed_specs: list[dict[str, np.ndarray]] = []

    for spec in DEFAULT_CELLS:
        raw_target_candidates = raw_target_candidates_for_spec(spec, args)
        raw_queries = raw_queries_for_spec(spec, args)
        raw_candidates = np.concatenate([raw_target_candidates[: len(data.items)], raw_distractors[spec.storage_label]], axis=0)
        mean, pcs = offline.fit_pcs(raw_candidates, 15)
        candidate_vectors, query_vectors = offline.transform_vectors(raw_candidates, raw_queries[: len(data.items)], mean, pcs, spec.transform, spec.k)
        scores = base.normalize_rows(query_vectors) @ base.normalize_rows(candidate_vectors).T
        single_scores[spec.variant] = scores.astype(np.float32, copy=False)
        transformed_specs.append({"candidates": candidate_vectors, "queries": query_vectors})
        base.log(f"  stage2 hidden scored {spec.name}: scores={scores.shape}")

    k3_vector_average = score_vector_average_stage2(transformed_specs)
    k3_zsum = sum_stage2_subset_zscores(
        [single_scores[spec.variant] for spec in DEFAULT_CELLS],
        target_count=len(data.items),
        distractor_count=len(distractor_chunks),
    )
    return {
        "single_scores": single_scores,
        "k3_vector_average": k3_vector_average.astype(np.float32, copy=False),
        "k3_zsum": k3_zsum.astype(np.float32, copy=False),
    }


def load_or_encode_distractor_hidden(distractor_chunks: list[str], args: argparse.Namespace) -> dict[str, np.ndarray]:
    cells = [
        base.CellConfig(spec.variant, spec.layer, "anti_pca_both_k15", spec.family)
        for spec in DEFAULT_CELLS
    ]
    prompt_hash = base.short_hash(
        [f"{cell.variant}:{base.PROMPT_VARIANTS[cell.variant]}" for cell in cells]
    )
    distractor_hash = base.short_hash(distractor_chunks)
    cache_dir = (
        BENCH_DIR
        / "tensors"
        / (
            f"hidden_stage2_distractors_t{args.turns}_c{args.chunk_size}_s{args.stride}_"
            f"n{len(distractor_chunks)}_{distractor_hash}_"
            f"{base.short_hash([cell.label for cell in cells])}_{prompt_hash}"
        )
    )
    manifest_path = cache_dir / "manifest.json"
    vectors_path = cache_dir / "raw_hidden_vectors.npz"
    expected = {
        "kind": "prefeval_stage2_distractor_hidden_vectors",
        "turns": args.turns,
        "chunk_size": args.chunk_size,
        "stride": args.stride,
        "distractor_text_hash": distractor_hash,
        "distractor_count": len(distractor_chunks),
        "model_path": str(Path(args.hidden_model_path)),
        "cells": [asdict(cell) for cell in cells],
        "prompt_variants": {cell.variant: base.PROMPT_VARIANTS[cell.variant] for cell in cells},
    }
    if manifest_path.exists() and vectors_path.exists() and not args.overwrite:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("expected") == expected:
            base.log(f"loading Stage 2 distractor hidden cache {cache_dir}")
            with np.load(vectors_path) as arrays:
                return {
                    cell.label: np.asarray(arrays[f"{cell.label}::candidates"], dtype=np.float32)
                    for cell in cells
                }
        if not args.resume:
            raise ValueError(
                f"Stage 2 distractor cache exists but manifest does not match current run: {cache_dir}. "
                "Use --overwrite for a fresh cache."
            )

    if args.synthetic_smoke:
        base.log("synthetic smoke: using deterministic pseudo hidden vectors for Stage 2 distractors")
        return {
            cell.label: np.stack(
                [base.hash_vector(f"{cell.label}|stage2-distractor|{text}", 128) for text in distractor_chunks],
                axis=0,
            ).astype(np.float32, copy=False)
            for cell in cells
        }

    from hidden_state.cached_suffix_extractor import CachedSuffixExtractor, clear_mlx_memory

    base.log(f"encoding Stage 2 distractor hidden vectors with {args.hidden_model_path}")
    cache_dir.mkdir(parents=True, exist_ok=True)
    target_layers = sorted({cell.layer for cell in cells})
    target_variants = base.unique_in_order([cell.variant for cell in cells])
    extractor = CachedSuffixExtractor(Path(args.hidden_model_path), clear_metal_cache_after_suffix=False)
    raw_lists: dict[str, list[np.ndarray]] = {cell.label: [] for cell in cells}
    started = time.monotonic()
    for text_index, text in enumerate(distractor_chunks):
        prefix_state = extractor.prefill_prefix(text, target_layers=target_layers, target_positions=["content_end"])
        suffix_vectors: dict[tuple[str, int], np.ndarray] = {}
        for variant in target_variants:
            vectors, _top_logits, _selected_logits = extractor.encode_suffix_with_logit_outputs(
                prefix_state=prefix_state,
                suffix_text=base.PROMPT_VARIANTS[variant],
                target_layers=target_layers,
                target_positions=["last"],
                topk_logits=0,
                selected_logit_token_ids=None,
            )
            for layer in target_layers:
                value = vectors.get((layer, "last"))
                if value is not None:
                    suffix_vectors[(variant, layer)] = value.astype(np.float32, copy=False)
        for cell in cells:
            raw_lists[cell.label].append(suffix_vectors[(cell.variant, cell.layer)])
        if args.clear_cache_every == "text":
            clear_mlx_memory(clear_metal_cache=True)
        done = text_index + 1
        elapsed = time.monotonic() - started
        eta = elapsed / max(done, 1) * (len(distractor_chunks) - done)
        if done == 1 or done == len(distractor_chunks) or done % 10 == 0:
            base.log(f"  stage2 distractor hidden encoded {done}/{len(distractor_chunks)} elapsed={base.fmt_duration(elapsed)} eta={base.fmt_duration(eta)}")
        del prefix_state
    del extractor
    clear_mlx_memory(clear_metal_cache=True)
    raw_by_cell = {
        cell.label: np.stack(raw_lists[cell.label], axis=0).astype(np.float32, copy=False)
        for cell in cells
    }
    np.savez_compressed(
        vectors_path,
        **{
            f"{cell.label}::candidates": raw_by_cell[cell.label].astype(np.float16, copy=False)
            for cell in cells
        },
    )
    manifest_path.write_text(
        json.dumps({"expected": expected, "created_utc": base.now_utc(), "vector_dtype": "float16"}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return raw_by_cell


def raw_target_candidates_for_spec(spec: offline.DenseCellSpec, args: argparse.Namespace) -> np.ndarray:
    return raw_array_for_spec(spec, "::candidates", args)


def raw_queries_for_spec(spec: offline.DenseCellSpec, args: argparse.Namespace) -> np.ndarray:
    return raw_array_for_spec(spec, "::queries", args)


def raw_array_for_spec(spec: offline.DenseCellSpec, suffix: str, args: argparse.Namespace) -> np.ndarray:
    key = f"{spec.storage_label}{suffix}"
    for path in tensor_dirs(args):
        vectors_path = Path(path) / "raw_hidden_vectors.npz"
        if not vectors_path.exists():
            continue
        with np.load(vectors_path) as arrays:
            if key in arrays.files:
                return np.asarray(arrays[key], dtype=np.float32)
    raise KeyError(f"Missing raw hidden array {key} in tensor dirs: {tensor_dirs(args)}")


def tensor_dirs(args: argparse.Namespace) -> list[str]:
    if args.tensor_dir:
        return list(args.tensor_dir)
    return [str(DEFAULT_MAIN_TENSOR), str(DEFAULT_EXTRA_TENSOR)]


def score_vector_average_stage2(items: list[dict[str, np.ndarray]]) -> np.ndarray:
    candidates = []
    queries = []
    for item in items:
        candidates.append(base.normalize_rows(item["candidates"]))
        queries.append(base.normalize_rows(item["queries"]))
    candidate_vectors = base.normalize_rows(np.mean(np.stack(candidates, axis=0), axis=0))
    query_vectors = base.normalize_rows(np.mean(np.stack(queries, axis=0), axis=0))
    return query_vectors @ candidate_vectors.T


def fuse_stage2_subset_scores(
    dense: np.ndarray,
    bm25: np.ndarray,
    *,
    target_count: int,
    distractor_count: int,
    dense_weight: float,
) -> np.ndarray:
    output = np.zeros_like(dense, dtype=np.float32)
    for query_index in range(target_count):
        allowed = stage2_allowed_cols(query_index, target_count, distractor_count)
        output[query_index, allowed] = (
            dense_weight * zscore_1d(dense[query_index, allowed])
            + (1.0 - dense_weight) * zscore_1d(bm25[query_index, allowed])
        )
    return output


def sum_stage2_subset_zscores(
    matrices: list[np.ndarray],
    *,
    target_count: int,
    distractor_count: int,
) -> np.ndarray:
    output = np.zeros_like(matrices[0], dtype=np.float32)
    for query_index in range(target_count):
        allowed = stage2_allowed_cols(query_index, target_count, distractor_count)
        local = np.zeros((len(allowed),), dtype=np.float32)
        for matrix in matrices:
            local += zscore_1d(matrix[query_index, allowed])
        output[query_index, allowed] = local
    return output


def stage2_allowed_cols(query_index: int, target_count: int, distractor_count: int) -> np.ndarray:
    distractor_cols = np.arange(target_count, target_count + distractor_count, dtype=np.int64)
    return np.concatenate([np.asarray([query_index], dtype=np.int64), distractor_cols])


def zscore_1d(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float32)
    std = float(np.std(values))
    if std < 1e-8:
        return np.zeros_like(values, dtype=np.float32)
    return ((values - float(np.mean(values))) / std).astype(np.float32, copy=False)


def evaluate_stage2_scores(
    name: str,
    description: str,
    scores: np.ndarray,
    data: base.BenchmarkData,
    distractor_count: int,
) -> dict[str, Any]:
    target_count = len(data.items)
    ranks = []
    margins = []
    examples = []
    for query_index in range(target_count):
        target_col = query_index
        distractor_cols = np.arange(target_count, target_count + distractor_count, dtype=np.int64)
        allowed = np.concatenate([np.asarray([target_col], dtype=np.int64), distractor_cols])
        local_scores = scores[query_index, allowed]
        order = np.argsort(-local_scores, kind="mergesort")
        rank = int(np.where(order == 0)[0][0]) + 1
        ranks.append(rank)
        best_distractor = float(np.max(local_scores[1:])) if len(local_scores) > 1 else float("-inf")
        margin = float(local_scores[0] - best_distractor)
        margins.append(margin)
        if rank > 5 and len(examples) < 20:
            best_local = int(order[0])
            best_col = int(allowed[best_local])
            examples.append(
                {
                    "query_id": data.query_ids[query_index],
                    "target_rank": rank,
                    "target_score": float(local_scores[0]),
                    "best_score": float(local_scores[best_local]),
                    "best_candidate": "target" if best_col == target_col else f"distractor_{best_col - target_count:04d}",
                    "question": data.query_texts[query_index],
                    "target_memory": data.candidate_texts[query_index],
                }
            )
    rank_arr = np.asarray(ranks, dtype=np.int32)
    summary = {
        "recall@1": float(np.mean(rank_arr <= 1)),
        "recall@3": float(np.mean(rank_arr <= 3)),
        "recall@5": float(np.mean(rank_arr <= 5)),
        "recall@10": float(np.mean(rank_arr <= 10)),
        "recall@20": float(np.mean(rank_arr <= 20)),
        "mrr": float(np.mean(1.0 / rank_arr)),
        "mean_rank": float(np.mean(rank_arr)),
        "median_rank": float(np.median(rank_arr)),
        "mean_target_margin": float(np.mean(margins)),
    }
    return {
        "name": name,
        "description": description,
        "summary": summary,
        "rank_histogram": rank_histogram(rank_arr),
        "examples_rank_gt5": examples,
    }


def rank_histogram(ranks: np.ndarray) -> dict[str, int]:
    buckets = {
        "1": int(np.sum(ranks == 1)),
        "2-3": int(np.sum((2 <= ranks) & (ranks <= 3))),
        "4-5": int(np.sum((4 <= ranks) & (ranks <= 5))),
        "6-10": int(np.sum((6 <= ranks) & (ranks <= 10))),
        "11-20": int(np.sum((11 <= ranks) & (ranks <= 20))),
        ">20": int(np.sum(ranks > 20)),
    }
    return buckets


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# PrefEval Stage 2 Retrieval-Only",
        "",
        f"- Created UTC: `{payload['created_utc']}`",
        f"- Items: `{payload['task_summary']['items']}`",
        f"- Distractor chunks/query: `{payload['task_summary']['distractor_chunks_per_query']}`",
        f"- Candidate pool/query: `{payload['task_summary']['candidate_pool_per_query']}`",
        f"- Turns: `{payload['inputs']['turns']}`",
        f"- Chunk size / stride: `{payload['inputs']['chunk_size']}` / `{payload['inputs']['stride']}`",
        f"- Elapsed: `{base.fmt_duration(payload['elapsed_seconds'])}`",
        "",
        "| rank | retriever | R@1 | R@3 | R@5 | R@10 | R@20 | MRR | mean_rank | margin |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(payload["rows"], start=1):
        s = row["summary"]
        lines.append(
            f"| {rank} | `{row['name']}` | {s['recall@1']:.3f} | {s['recall@3']:.3f} | "
            f"{s['recall@5']:.3f} | {s['recall@10']:.3f} | {s['recall@20']:.3f} | "
            f"{s['mrr']:.3f} | {s['mean_rank']:.1f} | {s['mean_target_margin']:.3f} |"
        )
    lines.extend(["", "## Rank Histograms", ""])
    for row in payload["rows"]:
        lines.append(f"### `{row['name']}`")
        lines.append("")
        lines.append("| bucket | count |")
        lines.append("|---|---:|")
        for bucket, count in row["rank_histogram"].items():
            lines.append(f"| `{bucket}` | {count} |")
        lines.append("")
    return "\n".join(lines) + "\n"


def render_short_table(payload: dict[str, Any]) -> str:
    lines = ["retriever\tR@1\tR@3\tR@5\tMRR\tmean_rank"]
    for row in payload["rows"]:
        s = row["summary"]
        lines.append(
            f"{row['name']}\t{s['recall@1']:.3f}\t{s['recall@3']:.3f}\t"
            f"{s['recall@5']:.3f}\t{s['mrr']:.3f}\t{s['mean_rank']:.1f}"
        )
    return "\n".join(lines)


def default_prefix(args: argparse.Namespace) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    limit = "all" if not args.limit else f"n{args.limit}"
    return f"retrieval_only_{limit}_turn{args.turns}_chunk{args.chunk_size}_stride{args.stride}_{stamp}"


def dense_cell_to_json(spec: offline.DenseCellSpec) -> dict[str, Any]:
    return {
        "name": spec.name,
        "variant": spec.variant,
        "layer": spec.layer,
        "transform": spec.transform,
        "k": spec.k,
        "family": spec.family,
        "storage_label": spec.storage_label,
    }


def file_sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


if __name__ == "__main__":
    raise SystemExit(main())
