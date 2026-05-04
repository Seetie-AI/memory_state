"""Dump reusable hidden-state tensors for multi-angle analysis.

This script implements the post-Phase-2 diagnostic plan. MVP_Plan.md originally
listed mean pooling and sentinel-token pooling as backburner items; this dump is
broader and intentionally saves raw layer/position tensors so those ideas and
layer-selection experiments can be analyzed offline without rerunning Qwen3.5.

Storage design:

- Tier A covers many prompts and stores only prompt-final vectors for every
  layer plus final post-norm output. It is chunked safetensors to keep memory
  stable and resumable.
- Tier B covers a small deep subset and stores all positions for all layers.
  It is per-prompt safetensors because each file can be skipped independently
  after an interrupted run.

Why: full hidden tensors for all S/round prompts would exceed the user's 30GB
budget. The Tier A/Tier B split maximizes reusable signal under that limit.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import mlx.core as mx


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from hidden_state.mlx_wrapper import MLXHiddenStateExtractor
from longmemeval.data import Instance, iter_round_candidates, load_instances
from method.hidden_state import memory_prompt, query_prompt


BYTES_PER_DTYPE = {"bf16": 2, "fp16": 2, "fp32": 4}


@dataclass(frozen=True)
class PromptItem:
    prompt_id: str
    instance_index: int
    question_id: str
    role: str
    text: str
    candidate_id: str | None
    is_gold: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(ROOT / "data" / "longmemeval_s_cleaned.json"))
    parser.add_argument("--granularity", choices=["round"], default="round")
    parser.add_argument("--tier-a-instances", type=int, default=100)
    parser.add_argument("--tier-b-instances", type=int, default=2)
    parser.add_argument("--tier-b-prompt-budget", type=int, default=500)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--chunk-size", type=int, default=2000)
    parser.add_argument("--storage-dtype", choices=["bf16", "fp16", "fp32"], default="bf16")
    parser.add_argument("--model-path", default=str(ROOT / "models" / "Qwen3.5-2B-bf16"))
    parser.add_argument("--output-dir", default=str(ROOT / "tensors" / "dump_v1"))
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--budget-gb", type=float, default=30.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    instances = load_instances(args.data)
    if args.preview:
        args.tier_a_instances = 1
        args.tier_b_instances = 1
        args.tier_b_prompt_budget = 500

    tier_a_items = build_prompt_items(instances[: args.tier_a_instances])
    tier_b_items = build_tier_b_prompt_items(
        instances[: args.tier_b_instances],
        prompt_budget=args.tier_b_prompt_budget,
    )
    estimate = estimate_bytes(
        tier_a_prompts=len(tier_a_items),
        tier_b_prompts=len(tier_b_items),
        max_tokens=args.max_tokens,
        storage_dtype=args.storage_dtype,
    )
    if estimate["total_gb"] > args.budget_gb and not args.force:
        raise SystemExit(
            f"Estimated dump size {estimate['total_gb']:.2f}GB exceeds "
            f"budget {args.budget_gb:.2f}GB. Lower Tier B or pass --force."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = load_manifest(output_dir)
    manifest.setdefault("config", vars(args) | {"estimate": estimate})
    manifest.setdefault("prompts", {})
    manifest.setdefault("tier_a_chunks", [])
    progress_log(output_dir, f"start dump estimate={estimate}")

    extractor = MLXHiddenStateExtractor(args.model_path)
    run_tier_a(args, output_dir, manifest, extractor, tier_a_items)
    save_manifest(output_dir, manifest)
    run_tier_b(args, output_dir, manifest, extractor, tier_b_items)
    save_manifest(output_dir, manifest)
    progress_log(output_dir, "finish dump")
    return 0


def build_prompt_items(instances: list[Instance]) -> list[PromptItem]:
    items: list[PromptItem] = []
    for instance_index, instance in enumerate(instances):
        items.extend(build_prompt_items_for_instance(instance_index, instance))
    return items


def build_prompt_items_for_instance(instance_index: int, instance: Instance) -> list[PromptItem]:
    items = [
        PromptItem(
            prompt_id=f"inst{instance_index:04d}_query",
            instance_index=instance_index,
            question_id=instance.question_id,
            role="query",
            text=instance.question,
            candidate_id=None,
            is_gold=False,
        )
    ]
    for candidate_index, (candidate_id, text, is_gold) in enumerate(iter_round_candidates(instance)):
        items.append(
            PromptItem(
                prompt_id=f"inst{instance_index:04d}_cand{candidate_index:04d}",
                instance_index=instance_index,
                question_id=instance.question_id,
                role="candidate",
                text=text,
                candidate_id=candidate_id,
                is_gold=is_gold,
            )
        )
    return items


def build_tier_b_prompt_items(instances: list[Instance], prompt_budget: int) -> list[PromptItem]:
    """Select complete instances for Tier B without cutting a candidate set.

    Tier B position/diagonal analyses can run retrieval only when a query and
    all candidate turns for an instance are present. If the prompt budget is too
    small, prefer fewer complete instances over a partially dumped one.
    """
    selected: list[PromptItem] = []
    for instance_index, instance in enumerate(instances):
        next_instance = build_prompt_items_for_instance(instance_index, instance)
        if selected and len(selected) + len(next_instance) > prompt_budget:
            break
        if not selected and len(next_instance) > prompt_budget:
            raise ValueError(
                f"tier_b_prompt_budget={prompt_budget} is too small for one complete "
                f"instance ({len(next_instance)} prompts)."
            )
        selected.extend(next_instance)
    return selected


def estimate_bytes(
    tier_a_prompts: int,
    tier_b_prompts: int,
    max_tokens: int,
    storage_dtype: str,
    num_layers: int = 24,
    hidden_dim: int = 2048,
) -> dict[str, float]:
    bytes_per_value = BYTES_PER_DTYPE[storage_dtype]
    tier_a = tier_a_prompts * ((num_layers * hidden_dim) + hidden_dim) * bytes_per_value
    tier_b = tier_b_prompts * num_layers * max_tokens * hidden_dim * bytes_per_value
    total = tier_a + tier_b
    return {
        "tier_a_gb": tier_a / 1e9,
        "tier_b_gb": tier_b / 1e9,
        "total_gb": total / 1e9,
    }


def run_tier_a(
    args: argparse.Namespace,
    output_dir: Path,
    manifest: dict[str, Any],
    extractor: MLXHiddenStateExtractor,
    items: list[PromptItem],
) -> None:
    tier_dir = output_dir / "tier_a"
    tier_dir.mkdir(parents=True, exist_ok=True)
    completed = {
        prompt_id
        for prompt_id, record in manifest["prompts"].items()
        if record.get("tier_a_file")
    }
    buffer: list[tuple[PromptItem, Any]] = []
    chunk_index = len(manifest["tier_a_chunks"])

    for item in items:
        if item.prompt_id in completed:
            continue
        prompt = query_prompt(item.text) if item.role == "query" else memory_prompt(item.text)
        dump = extractor.dump_prompt_layers(
            prompt,
            max_tokens=None,
            capture_all_positions=False,
            storage_dtype=args.storage_dtype,
        )
        buffer.append((item, dump))
        progress_log(output_dir, f"tier_a encoded {item.prompt_id}")
        if len(buffer) >= args.chunk_size:
            chunk_index = flush_tier_a_chunk(tier_dir, manifest, buffer, chunk_index, output_dir)
            buffer = []

    if buffer:
        flush_tier_a_chunk(tier_dir, manifest, buffer, chunk_index, output_dir)


def flush_tier_a_chunk(
    tier_dir: Path,
    manifest: dict[str, Any],
    buffer: list[tuple[PromptItem, Any]],
    chunk_index: int,
    output_dir: Path,
) -> int:
    path = tier_dir / f"chunk_{chunk_index:04d}.safetensors"
    last_by_layer = mx.stack([dump.last_by_layer for _item, dump in buffer], axis=0)
    final_post_norm = mx.stack([dump.final_post_norm for _item, dump in buffer], axis=0)
    mx.save_safetensors(str(path), {"last_by_layer": last_by_layer, "final_post_norm": final_post_norm})

    prompt_ids = []
    for local_index, (item, dump) in enumerate(buffer):
        prompt_ids.append(item.prompt_id)
        manifest["prompts"][item.prompt_id] = prompt_record(item) | {
            "token_count": dump.token_count,
            "truncated_to": dump.truncated_to,
            "tier_a_file": str(path.relative_to(output_dir)),
            "tier_a_index": local_index,
        }
    manifest["tier_a_chunks"].append(
        {"file": str(path.relative_to(output_dir)), "prompt_ids": prompt_ids}
    )
    save_manifest(output_dir, manifest)
    progress_log(output_dir, f"tier_a flushed {path.name} n={len(buffer)}")
    return chunk_index + 1


def run_tier_b(
    args: argparse.Namespace,
    output_dir: Path,
    manifest: dict[str, Any],
    extractor: MLXHiddenStateExtractor,
    items: list[PromptItem],
) -> None:
    tier_dir = output_dir / "tier_b"
    tier_dir.mkdir(parents=True, exist_ok=True)
    for item in items:
        record = manifest["prompts"].get(item.prompt_id, prompt_record(item))
        if record.get("tier_b_file"):
            continue

        prompt = query_prompt(item.text) if item.role == "query" else memory_prompt(item.text)
        dump = extractor.dump_prompt_layers(
            prompt,
            max_tokens=args.max_tokens,
            capture_all_positions=True,
            storage_dtype=args.storage_dtype,
        )
        if dump.all_by_layer is None:
            raise RuntimeError("Tier B requested all positions but dump returned none.")
        path = tier_dir / f"{item.prompt_id}.safetensors"
        mx.save_safetensors(
            str(path),
            {
                "all_by_layer": dump.all_by_layer,
                "last_by_layer": dump.last_by_layer,
                "final_post_norm": dump.final_post_norm,
            },
        )
        manifest["prompts"][item.prompt_id] = record | {
            "token_count": dump.token_count,
            "truncated_to": dump.truncated_to,
            "tier_b_file": str(path.relative_to(output_dir)),
        }
        save_manifest(output_dir, manifest)
        progress_log(output_dir, f"tier_b saved {item.prompt_id}")


def prompt_record(item: PromptItem) -> dict[str, Any]:
    return asdict(item)


def load_manifest(output_dir: Path) -> dict[str, Any]:
    path = output_dir / "manifest.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_manifest(output_dir: Path, manifest: dict[str, Any]) -> None:
    path = output_dir / "manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def progress_log(output_dir: Path, message: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    with (output_dir / "progress.log").open("a", encoding="utf-8") as handle:
        handle.write(f"{now}\t{message}\n")


if __name__ == "__main__":
    raise SystemExit(main())
