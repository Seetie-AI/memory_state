"""Stage 3 Phase 1 oracle union-hit combo sweep.

This is a small companion script for prompt-fusion exploration. It reuses the
Stage 3 prompt-fusion Phase 1 loader, then ranks prompt combinations by oracle
union hit@k: a query scores once if any prompt in the combo retrieves all gold
evidence within top-k.

This is intentionally an oracle diagnostic, not a deployment metric. It uses
gold labels to find prompt pairs with complementary hits on the same evaluation
set, so any downstream pair selected from this output must be marked as
same-set selected / overfit risk.

The script is intentionally read-only with respect to tensors; it only writes a
JSON/Markdown summary under results/stage3/prompt_fusion/.
"""

from __future__ import annotations

import argparse
import itertools
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

import stage3_prompt_fusion_analyze as fusion


DEFAULT_OUTPUT_PREFIX = "phase1_union_r3_combo_sweep"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(fusion.DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(fusion.DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(fusion.DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--top-k", type=int, default=50)
    parser.add_argument("--combo-sizes", default="2,3")
    parser.add_argument("--limit-audit-cells", type=int, default=None)
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()

    dump_dir = Path(args.dump_dir)
    manifest = fusion.offline.load_manifest(dump_dir)
    fusion.offline.validate_manifest(manifest)
    records = fusion.offline.load_records(dump_dir, manifest, Path(args.data))

    cells = fusion.BEST_CELLS[: args.limit_audit_cells] if args.limit_audit_cells else list(fusion.BEST_CELLS)
    combo_sizes = parse_int_list(args.combo_sizes)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in [json_path, md_path] if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    phase1 = fusion.run_phase1_audit(
        dump_dir,
        manifest,
        records,
        cells,
        max(args.top_k, args.k),
        args.bootstrap_samples,
    )
    runs = phase1["runs"]
    singles = single_rows(runs, args.k)
    combos = combo_rows(runs, combo_sizes, args.k)
    pairs = [row for row in combos if row["size"] == 2]

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "tmp_phase1_union_combo_sweep",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "k": args.k,
            "top_k": args.top_k,
            "combo_sizes": combo_sizes,
            "limit_audit_cells": args.limit_audit_cells,
            "bootstrap_samples": args.bootstrap_samples,
        },
        "single_cells": singles,
        "pairs_by_union_hit": sorted(pairs, key=union_sort_key, reverse=True),
        "pairs_by_gain": sorted(pairs, key=gain_sort_key, reverse=True),
        "combos": sorted(combos, key=union_sort_key, reverse=True),
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(fusion.offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(f"elapsed {fusion.format_seconds(payload['elapsed_seconds'])}")
    return 0


def parse_int_list(value: str) -> list[int]:
    output = []
    for item in value.split(","):
        item = item.strip()
        if item:
            output.append(int(item))
    return sorted(set(output))


def single_rows(runs: list[fusion.CellRun], k: int) -> list[dict[str, Any]]:
    rows = []
    for run in runs:
        scored = [item for item in run.items if fusion.is_scored(item)]
        hits = [hit_all(item, k) for item in scored]
        rows.append(
            {
                "label": run.cell.label,
                "variant": run.cell.variant,
                "family": run.cell.family,
                f"hit@{k}": safe_mean(hits),
                "hit_count": int(sum(hits)),
                "n_scored": len(scored),
            }
        )
    return sorted(rows, key=lambda row: (row[f"hit@{k}"], row["hit_count"]), reverse=True)


def combo_rows(runs: list[fusion.CellRun], combo_sizes: list[int], k: int) -> list[dict[str, Any]]:
    single_hit_by_label = {row["label"]: row[f"hit@{k}"] for row in single_rows(runs, k)}
    rows = []
    for size in combo_sizes:
        if size < 2:
            continue
        for combo in itertools.combinations(runs, size):
            scored_items = scored_items_by_question(combo)
            union_hits = []
            all_hits = []
            neither_hits = []
            jaccards = []
            for items in scored_items.values():
                hit_values = [hit_all(item, k) for item in items]
                union_hits.append(any(hit_values))
                all_hits.append(all(hit_values))
                neither_hits.append(not any(hit_values))
                jaccards.extend(pairwise_jaccards(items, k))
            labels = [run.cell.label for run in combo]
            best_single = max(single_hit_by_label[label] for label in labels)
            union_hit = safe_mean(union_hits)
            rows.append(
                {
                    "size": size,
                    "labels": labels,
                    "families": [run.cell.family for run in combo],
                    "combo": " + ".join(labels),
                    f"union_hit@{k}": union_hit,
                    "union_hit_count": int(sum(union_hits)),
                    "gain_vs_best_single": union_hit - best_single,
                    "gain_count_vs_best_single": int(round((union_hit - best_single) * len(union_hits))),
                    "best_single_hit": best_single,
                    "cell_hits": [single_hit_by_label[label] for label in labels],
                    "all_hit": safe_mean(all_hits),
                    "neither_hit": safe_mean(neither_hits),
                    f"avg_pairwise_top{k}_jaccard": safe_mean(jaccards),
                    "n_scored": len(union_hits),
                }
            )
    return rows


def scored_items_by_question(combo: tuple[fusion.CellRun, ...]) -> dict[str, list[fusion.ScoredItem]]:
    by_run = []
    for run in combo:
        by_run.append({item.question_id: item for item in run.items if fusion.is_scored(item)})
    common_qids = set(by_run[0])
    for mapping in by_run[1:]:
        common_qids &= set(mapping)
    return {qid: [mapping[qid] for mapping in by_run] for qid in sorted(common_qids)}


def hit_all(item: fusion.ScoredItem, k: int) -> bool:
    return set(item.gold_ids).issubset(set(item.ranked_ids[:k])) if item.gold_ids else False


def pairwise_jaccards(items: list[fusion.ScoredItem], k: int) -> list[float]:
    output = []
    for left, right in itertools.combinations(items, 2):
        left_ids = set(left.ranked_ids[:k])
        right_ids = set(right.ranked_ids[:k])
        union = left_ids | right_ids
        output.append((len(left_ids & right_ids) / len(union)) if union else 0.0)
    return output


def union_sort_key(row: dict[str, Any]) -> tuple[float, float, float]:
    union_key = next(key for key in row if key.startswith("union_hit@"))
    jaccard_key = next(key for key in row if key.startswith("avg_pairwise_top"))
    return (float(row[union_key]), float(row["gain_vs_best_single"]), -float(row[jaccard_key]))


def gain_sort_key(row: dict[str, Any]) -> tuple[float, float, float]:
    union_key = next(key for key in row if key.startswith("union_hit@"))
    return (float(row["gain_vs_best_single"]), float(row[union_key]), float(row["best_single_hit"]))


def safe_mean(values: Any) -> float:
    vals = [float(value) for value in values]
    return float(np.mean(vals)) if vals else float("nan")


def render_markdown(payload: dict[str, Any]) -> str:
    k = payload["inputs"]["k"]
    lines = [
        f"# Temporary Phase 1 union-hit combo sweep @ {k}",
        "",
        "A combination scores a question once if any prompt retrieves all gold evidence in the top-k.",
        "",
        f"Elapsed: {fusion.format_seconds(payload['elapsed_seconds'])}",
        "",
        "## Single Cells",
        "",
        f"| rank | cell | family | hit@{k} | count | n |",
        "|---:|---|---|---:|---:|---:|",
    ]
    for index, row in enumerate(payload["single_cells"], start=1):
        lines.append(
            f"| {index} | `{row['label']}` | {row['family']} | "
            f"{row[f'hit@{k}']:.3f} | {row['hit_count']} | {row['n_scored']} |"
        )
    lines.extend(render_combo_table(f"## Size 2 Combos Sorted By Union Hit@{k}", payload["pairs_by_union_hit"], k))
    lines.extend(render_combo_table("## Size 2 Combos Sorted By Gain Over Best Single", payload["pairs_by_gain"], k))
    for size in payload["inputs"]["combo_sizes"]:
        if size == 2:
            continue
        rows = [row for row in payload["combos"] if row["size"] == size]
        lines.extend(render_combo_table(f"## Size {size} Combos Sorted By Union Hit@{k}", rows, k))
    lines.append("")
    return "\n".join(lines)


def render_combo_table(title: str, rows: list[dict[str, Any]], k: int, limit: int = 136) -> list[str]:
    union_key = f"union_hit@{k}"
    jaccard_key = f"avg_pairwise_top{k}_jaccard"
    lines = [
        "",
        title,
        "",
        f"| rank | combo | union@{k} | gain | best_single | all_hit | neither | avg_pair_jaccard@{k} |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(rows[:limit], start=1):
        lines.append(
            f"| {index} | `{row['combo']}` | {row[union_key]:.3f} | "
            f"{row['gain_vs_best_single']:.3f} | {row['best_single_hit']:.3f} | "
            f"{row['all_hit']:.3f} | {row['neither_hit']:.3f} | {row[jaccard_key]:.3f} |"
        )
    return lines


if __name__ == "__main__":
    raise SystemExit(main())
