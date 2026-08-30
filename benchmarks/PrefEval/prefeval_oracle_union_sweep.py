"""PrefEval oracle union-hit prompt combo sweep.

This is the PrefEval equivalent of Stage 3's LongMemEval
`stage3_prompt_fusion_oracle_union_sweep.py`.

It does not run any model. It loads the saved n=1000 hidden tensor cache and
the prompt-sweep result table, chooses one best layer per prompt variant, then
computes oracle union hit@k:

- all prompt pairs
- fixed base pair `2-3-1 + 2-5` plus every other prompt as a third prompt

The metric is an oracle diagnostic, not a deployable retriever. A combo scores
a query once if any source's top-k contains a gold preference memory.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

import prefeval_benchmark as base
import prefeval_stage1_offline as offline


BENCH_DIR = Path(__file__).resolve().parent
DEFAULT_RESULTS_DIR = BENCH_DIR / "results" / "prefeval_stage1"
DEFAULT_PROMPT_SWEEP_JSON = (
    BENCH_DIR
    / "results"
    / "implicit_persona_n1000_pruned_hidden_l28_l29_l30_l31_logits256_promptreps128_20260512.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared-jsonl", default=str(offline.DEFAULT_PREPARED_JSONL))
    parser.add_argument(
        "--tensor-dir",
        action="append",
        default=None,
        help="Saved hidden tensor dir. May be passed multiple times. Defaults to latest cache.",
    )
    parser.add_argument(
        "--prompt-sweep-json",
        action="append",
        default=None,
        help="Prompt sweep result JSON. May be passed multiple times. Defaults to the main n=1000 sweep.",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_RESULTS_DIR))
    parser.add_argument("--output-prefix", default=f"oracle_union_prompt_pairs_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    parser.add_argument("--ks", default="3,5")
    parser.add_argument("--select-k", type=int, default=3, help="Metric k used to choose the representative layer per prompt.")
    parser.add_argument("--base-pair", default="2-3-1,2-5")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    prepared_jsonl = Path(args.prepared_jsonl)
    tensor_dirs = [Path(path) for path in args.tensor_dir] if args.tensor_dir else [offline.latest_hidden_tensor_dir()]
    prompt_sweep_jsons = (
        [Path(path) for path in args.prompt_sweep_json]
        if args.prompt_sweep_json
        else [DEFAULT_PROMPT_SWEEP_JSON]
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in (json_path, md_path) if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite: {existing}")

    ks = parse_ints(args.ks)
    base_pair = tuple(item.strip() for item in args.base_pair.split(",") if item.strip())
    if len(base_pair) != 2:
        raise ValueError(f"--base-pair must have exactly two prompt names, got {base_pair}")

    data = offline.load_prepared_jsonl(prepared_jsonl)
    validate_tensor_dirs(data, tensor_dirs)
    specs = choose_best_prompt_specs(prompt_sweep_jsons, select_k=args.select_k)
    missing_base = sorted(set(base_pair) - {spec.variant for spec in specs.values()})
    if missing_base:
        raise ValueError(f"Base pair prompts are unavailable in selected specs: {missing_base}")

    base.log(
        f"PrefEval oracle union sweep: prompts={len(specs)} pairs={len(specs) * (len(specs) - 1) // 2} "
        f"ks={ks} base_pair={base_pair}"
    )
    loaded = load_dense_specs_from_tensor_dirs(tensor_dirs, {spec.name: spec for spec in specs.values()})
    by_prompt = {spec.variant: loaded[spec.name] for spec in specs.values()}

    single_rows = single_prompt_rows(data, by_prompt, ks)
    pair_rows = combo_rows(data, by_prompt, itertools.combinations(by_prompt, 2), ks, single_rows)
    base_triples = [tuple([*base_pair, prompt]) for prompt in by_prompt if prompt not in base_pair]
    fixed_triple_rows = combo_rows(data, by_prompt, base_triples, ks, single_rows)
    base_pair_row = combo_rows(data, by_prompt, [base_pair], ks, single_rows)[0]

    primary_key = f"union_hit@{args.select_k}"
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "prefeval_oracle_union_prompt_pairs",
        "inputs": {
            "prepared_jsonl": str(prepared_jsonl),
            "tensor_dirs": [str(path) for path in tensor_dirs],
            "prompt_sweep_jsons": [str(path) for path in prompt_sweep_jsons],
            "ks": ks,
            "select_k": args.select_k,
            "base_pair": list(base_pair),
        },
        "task_summary": {
            "task": data.task,
            "dataset_id": data.dataset_id,
            "items": len(data.items),
            "candidate_count": len(data.candidate_ids),
            "query_count": len(data.query_ids),
        },
        "selected_specs": [dense_cell_to_json(spec) for spec in specs.values()],
        "single_prompts": sorted(single_rows, key=lambda row: (row.get(f"hit@{args.select_k}", 0.0), row.get("prompt", "")), reverse=True),
        "pairs_by_union_hit": sorted(pair_rows, key=lambda row: combo_sort_key(row, args.select_k), reverse=True),
        "pairs_by_gain": sorted(pair_rows, key=lambda row: gain_sort_key(row, args.select_k), reverse=True),
        "base_pair": base_pair_row,
        "fixed_base_triples": sorted(fixed_triple_rows, key=lambda row: combo_sort_key(row, args.select_k), reverse=True),
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    base.log(f"wrote {json_path}")
    base.log(f"wrote {md_path}")
    return 0


def validate_tensor_dirs(data: base.BenchmarkData, tensor_dirs: list[Path]) -> None:
    item_ids = [item.item_id for item in data.items]
    for tensor_dir in tensor_dirs:
        manifest = offline.load_manifest(tensor_dir)
        if manifest.get("item_ids") != item_ids:
            raise ValueError(f"Prepared JSONL item ids do not match tensor manifest item ids: {tensor_dir}")
        vectors_path = tensor_dir / "raw_hidden_vectors.npz"
        if not vectors_path.exists():
            raise FileNotFoundError(f"Missing raw hidden vectors: {vectors_path}")


def choose_best_prompt_specs(paths: list[Path], *, select_k: int) -> dict[str, offline.DenseCellSpec]:
    best: dict[str, dict[str, Any]] = {}
    pattern = re.compile(r"^sweep_(.+)_L(\d+)_both_k15$")
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for row in data.get("rows", []):
            name = row.get("name", "")
            match = pattern.match(name)
            if not match:
                continue
            variant = match.group(1)
            layer = int(match.group(2))
            summary = row.get("summary") or summarize_metrics(row["metrics"])
            sort_key = (
                float(summary.get(f"recall_all@{select_k}", 0.0)),
                float(summary.get(f"ndcg_any@{select_k}", 0.0)),
                float(summary.get("recall_all@5", 0.0)),
                float(summary.get("ndcg_any@5", 0.0)),
            )
            candidate = {
                "variant": variant,
                "layer": layer,
                "name": f"{variant}_L{layer}_both_k15",
                "sort_key": sort_key,
                "summary": summary,
            }
            if variant not in best or sort_key > best[variant]["sort_key"]:
                best[variant] = candidate
    return {
        variant: offline.DenseCellSpec(
            item["name"],
            variant,
            item["layer"],
            "anti_pca_both",
            15,
            "prompt-sweep-best",
        )
        for variant, item in sorted(best.items(), key=lambda pair: pair[1]["sort_key"], reverse=True)
    }


def load_dense_specs_from_tensor_dirs(
    tensor_dirs: list[Path],
    specs: dict[str, offline.DenseCellSpec],
) -> dict[str, dict[str, Any]]:
    loaded: dict[str, dict[str, Any]] = {}
    remaining = dict(specs)
    for tensor_dir in tensor_dirs:
        if not remaining:
            break
        vectors_path = tensor_dir / "raw_hidden_vectors.npz"
        with np.load(vectors_path) as arrays:
            available_keys = set(arrays.files)
            available = {
                name: spec
                for name, spec in remaining.items()
                if f"{spec.storage_label}::candidates" in available_keys
                and f"{spec.storage_label}::queries" in available_keys
            }
            if not available:
                continue
            base.log(f"loading {len(available)} dense spec(s) from {tensor_dir}")
            loaded.update(offline.load_dense_specs(arrays, available))
            for name in available:
                remaining.pop(name, None)
    if remaining:
        missing = {
            name: {
                "variant": spec.variant,
                "layer": spec.layer,
                "storage_label": spec.storage_label,
            }
            for name, spec in remaining.items()
        }
        raise KeyError(f"Missing dense tensor arrays for selected specs: {missing}")
    return loaded


def summarize_metrics(metrics: dict[str, Any]) -> dict[str, float]:
    return {name: float(value["mean"]) for name, value in metrics["metrics"].items()}


def single_prompt_rows(data: base.BenchmarkData, by_prompt: dict[str, dict[str, Any]], ks: list[int]) -> list[dict[str, Any]]:
    rows = []
    for prompt, loaded in by_prompt.items():
        row: dict[str, Any] = {"prompt": prompt}
        for k in ks:
            hits = [hit_for_scores(data, loaded["scores"], query_index, k) for query_index in range(len(data.query_ids))]
            row[f"hit@{k}"] = safe_mean(hits)
            row[f"hit_count@{k}"] = int(sum(hits))
        rows.append(row)
    return rows


def combo_rows(
    data: base.BenchmarkData,
    by_prompt: dict[str, dict[str, Any]],
    combos: Any,
    ks: list[int],
    single_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    single_by_prompt = {row["prompt"]: row for row in single_rows}
    rows = []
    for combo in combos:
        combo = tuple(combo)
        row: dict[str, Any] = {"size": len(combo), "prompts": list(combo), "combo": " + ".join(combo)}
        for k in ks:
            union_hits = []
            all_hits = []
            hit_counts_when_found = []
            jaccards = []
            for query_index in range(len(data.query_ids)):
                gold = set(data.gold_ids_by_query[query_index])
                prompt_sets = []
                prompt_hits = []
                for prompt in combo:
                    ids = top_ids(data.candidate_ids, by_prompt[prompt]["scores"][query_index], k)
                    prompt_sets.append(ids)
                    prompt_hits.append(bool(gold & ids))
                union_hit = any(prompt_hits)
                union_hits.append(union_hit)
                all_hits.append(all(prompt_hits))
                if union_hit:
                    hit_counts_when_found.append(sum(prompt_hits))
                for left, right in itertools.combinations(prompt_sets, 2):
                    jaccards.append(jaccard(left, right))
            best_single = max(single_by_prompt[prompt][f"hit@{k}"] for prompt in combo)
            union_hit = safe_mean(union_hits)
            row[f"union_hit@{k}"] = union_hit
            row[f"union_hit_count@{k}"] = int(sum(union_hits))
            row[f"best_single_hit@{k}"] = best_single
            row[f"gain_vs_best_single@{k}"] = union_hit - best_single
            row[f"gain_count_vs_best_single@{k}"] = int(round((union_hit - best_single) * len(data.query_ids)))
            row[f"all_hit@{k}"] = safe_mean(all_hits)
            row[f"neither_hit@{k}"] = 1.0 - union_hit
            row[f"avg_pairwise_jaccard@{k}"] = safe_mean(jaccards)
            row[f"mean_source_hits_when_found@{k}"] = safe_mean(hit_counts_when_found)
        rows.append(row)
    return rows


def hit_for_scores(data: base.BenchmarkData, scores: np.ndarray, query_index: int, k: int) -> bool:
    gold = set(data.gold_ids_by_query[query_index])
    return bool(gold & top_ids(data.candidate_ids, scores[query_index], k))


def top_ids(candidate_ids: list[str], scores: np.ndarray, k: int) -> set[str]:
    order = np.argsort(scores)[::-1][: min(k, len(scores))]
    return {candidate_ids[int(index)] for index in order}


def jaccard(left: set[str], right: set[str]) -> float:
    denom = len(left | right)
    return 0.0 if denom == 0 else len(left & right) / denom


def safe_mean(values: Any) -> float:
    vals = [float(value) for value in values]
    return float(np.mean(vals)) if vals else 0.0


def combo_sort_key(row: dict[str, Any], k: int) -> tuple[float, float, float]:
    return (
        float(row[f"union_hit@{k}"]),
        float(row[f"gain_vs_best_single@{k}"]),
        -float(row[f"avg_pairwise_jaccard@{k}"]),
    )


def gain_sort_key(row: dict[str, Any], k: int) -> tuple[float, float, float]:
    return (
        float(row[f"gain_vs_best_single@{k}"]),
        float(row[f"union_hit@{k}"]),
        float(row[f"best_single_hit@{k}"]),
    )


def parse_ints(value: str) -> list[int]:
    return sorted({int(item.strip()) for item in value.split(",") if item.strip()})


def dense_cell_to_json(cell: offline.DenseCellSpec) -> dict[str, Any]:
    return {
        "name": cell.name,
        "variant": cell.variant,
        "layer": cell.layer,
        "transform": cell.transform,
        "k": cell.k,
        "family": cell.family,
    }


def render_markdown(payload: dict[str, Any]) -> str:
    ks = payload["inputs"]["ks"]
    primary_k = payload["inputs"]["select_k"]
    lines = [
        f"# PrefEval Oracle Union Prompt Sweep @ {', '.join(str(k) for k in ks)}",
        "",
        "A combo scores a query once if any prompt in the combo retrieves a gold preference memory within top-k.",
        "",
        f"- Created UTC: `{payload['created_utc']}`",
        f"- Items: `{payload['task_summary']['items']}`",
        f"- Prompts: `{len(payload['selected_specs'])}`",
        f"- Elapsed: `{format_seconds(payload['elapsed_seconds'])}`",
        "",
        "## Selected Prompt Specs",
        "",
        "| prompt | config |",
        "|---|---|",
    ]
    for spec in payload["selected_specs"]:
        lines.append(f"| `{spec['variant']}` | L{spec['layer']} {spec['transform']}_k{spec['k']} |")
    lines.extend(["", "## Single Prompts", "", *render_single_table(payload["single_prompts"], ks)])
    lines.extend(
        [
            "",
            f"## All Pairs Sorted By Union Hit@{primary_k}",
            "",
            *render_combo_table(payload["pairs_by_union_hit"], ks, limit=120),
        ]
    )
    lines.extend(
        [
            "",
            f"## All Pairs Sorted By Gain@{primary_k}",
            "",
            *render_combo_table(payload["pairs_by_gain"], ks, limit=30),
        ]
    )
    lines.extend(
        [
            "",
            "## Fixed Base Pair",
            "",
            *render_combo_table([payload["base_pair"]], ks, limit=1),
            "",
            f"## Fixed `{' + '.join(payload['inputs']['base_pair'])}` Plus One Prompt",
            "",
            *render_combo_table(payload["fixed_base_triples"], ks, limit=120),
        ]
    )
    return "\n".join(lines) + "\n"


def render_single_table(rows: list[dict[str, Any]], ks: list[int]) -> list[str]:
    columns = ["rank", "prompt"] + [f"hit@{k}" for k in ks] + [f"count@{k}" for k in ks]
    lines = ["| " + " | ".join(columns) + " |", "|" + "|".join("---:" if col == "rank" or col.startswith(("hit", "count")) else "---" for col in columns) + "|"]
    primary = ks[0]
    sorted_rows = sorted(rows, key=lambda row: (row[f"hit@{primary}"], row["prompt"]), reverse=True)
    for index, row in enumerate(sorted_rows, start=1):
        values = [str(index), f"`{row['prompt']}`"]
        values.extend(f"{row[f'hit@{k}']:.3f}" for k in ks)
        values.extend(str(row[f"hit_count@{k}"]) for k in ks)
        lines.append("| " + " | ".join(values) + " |")
    return lines


def render_combo_table(rows: list[dict[str, Any]], ks: list[int], *, limit: int) -> list[str]:
    primary = ks[0]
    header = [
        "rank",
        "combo",
        f"union@{primary}",
        f"gain@{primary}",
        f"count@{primary}",
        f"jaccard@{primary}",
    ]
    for k in ks[1:]:
        header.extend([f"union@{k}", f"gain@{k}", f"count@{k}", f"jaccard@{k}"])
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---:" if item != "combo" else "---" for item in header) + "|"]
    for index, row in enumerate(rows[:limit], start=1):
        values = [
            str(index),
            f"`{row['combo']}`",
            f"{row[f'union_hit@{primary}']:.3f}",
            f"{row[f'gain_vs_best_single@{primary}']:.3f}",
            str(row[f"union_hit_count@{primary}"]),
            f"{row[f'avg_pairwise_jaccard@{primary}']:.3f}",
        ]
        for k in ks[1:]:
            values.extend(
                [
                    f"{row[f'union_hit@{k}']:.3f}",
                    f"{row[f'gain_vs_best_single@{k}']:.3f}",
                    str(row[f"union_hit_count@{k}"]),
                    f"{row[f'avg_pairwise_jaccard@{k}']:.3f}",
                ]
            )
        lines.append("| " + " | ".join(values) + " |")
    return lines


def format_seconds(seconds: float) -> str:
    seconds_int = int(round(seconds))
    minutes, secs = divmod(seconds_int, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minutes:02d}m{secs:02d}s"
    if minutes:
        return f"{minutes}m{secs:02d}s"
    return f"{secs}s"


def to_jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


if __name__ == "__main__":
    raise SystemExit(main())
