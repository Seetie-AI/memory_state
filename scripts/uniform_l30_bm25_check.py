"""Temporary uniform-L30 BM25 check for the product K=3 prompt set."""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SRC = ROOT / "src"
for path in [SCRIPTS, SRC]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import stage2_offline_analyze as offline
import stage3_prompt_fusion_analyze as fusion
import stage3_prompt_fusion_bm25_sweep as bm25_sweep
import tmp_union_top20_prompt_bm25_fusion as union_helpers
from eval.longmemeval_metrics import evaluate


DEFAULT_OUTPUT_DIR = ROOT / "results" / "stage3" / "step3_bm25_fusion" / "second_stage"
DEFAULT_OUTPUT_PREFIX = "tmp_uniform_l30_bm25"


@dataclass(frozen=True)
class UniformConfig:
    name: str
    description: str
    cells: tuple[fusion.CellConfig, ...]
    scorer: str = "vertical_concat_norm_weighted"


def cell(variant: str, layer: int) -> fusion.CellConfig:
    return fusion.CellConfig(variant, layer, "anti_pca_both_k15", f"uniform_l{layer}")


def make_config(layer: int) -> UniformConfig:
    return UniformConfig(
        name=f"concat_k3_norm_weighted_uniform_l{layer}_both_userword_tag_assoc",
        description=(
            "Same three product prompts, all forced to "
            f"L{layer} + anti_pca_both_k15."
        ),
        cells=(
            cell("2-4-1_user_word", layer),
            cell("1-3", layer),
            cell("2-5", layer),
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dump-dir", default=str(fusion.DEFAULT_DUMP_DIR))
    parser.add_argument("--data", default=str(fusion.DEFAULT_DATA))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=DEFAULT_OUTPUT_PREFIX)
    parser.add_argument("--layer", type=int, default=30)
    parser.add_argument("--alphas", default="0.75,1.0")
    parser.add_argument("--scopes", default="vector_top20,vector_top50")
    parser.add_argument("--bootstrap-samples", type=int, default=1000)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    started = time.perf_counter()
    config = make_config(args.layer)
    alphas = parse_float_list(args.alphas)
    scopes = parse_csv(args.scopes)
    dump_dir = Path(args.dump_dir)
    manifest = offline.load_manifest(dump_dir)
    offline.validate_manifest(manifest)
    records = offline.load_records(dump_dir, manifest, Path(args.data))
    buckets = offline.group_by_instance(records)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{args.output_prefix}.json"
    md_path = output_dir / f"{args.output_prefix}.md"
    if not args.overwrite:
        existing = [path for path in [json_path, md_path] if path.exists()]
        if existing:
            raise FileExistsError(f"Output exists; pass --overwrite to replace: {existing}")

    print(f"records={len(records)} config={config.name}")
    reprs = union_helpers.build_config_reprs_cpu(dump_dir, manifest, records, config)  # type: ignore[arg-type]
    rows = []
    for scope in scopes:
        score_rows = bm25_sweep.score_config_records(
            records,
            buckets,
            config,  # type: ignore[arg-type]
            reprs,
            bm25_scope=scope,
        )
        for alpha in alphas:
            predictions = bm25_sweep.predictions_from_scores(
                score_rows,
                alpha=alpha,
                top_k=50,
                scope=scope,
            )
            metrics = evaluate(predictions, skip_abstention=True, bootstrap_samples=args.bootstrap_samples)
            session = offline.session_retrieval_metrics(predictions)
            rank = offline.rank_metrics(predictions)
            summary = bm25_sweep.summarize_metrics(metrics, session, rank)
            rows.append(
                {
                    "config": config_to_json(config),
                    "bm25_scope": scope,
                    "alpha": alpha,
                    "metrics": metrics,
                    "session_metrics": session,
                    "rank_metrics": rank,
                    "summary": summary,
                }
            )

    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "analysis": "tmp_uniform_l30_bm25_check",
        "inputs": {
            "dump_dir": str(dump_dir),
            "data": str(Path(args.data)),
            "config": config_to_json(config),
            "alphas": alphas,
            "scopes": scopes,
            "bootstrap_samples": args.bootstrap_samples,
        },
        "rows": rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    json_path.write_text(json.dumps(offline.to_jsonable(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


def config_to_json(config: UniformConfig) -> dict[str, Any]:
    return {
        "name": config.name,
        "description": config.description,
        "scorer": config.scorer,
        "cells": [fusion.cell_to_json(cell) for cell in config.cells],
    }


def parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not values:
        raise ValueError("No alpha values parsed.")
    return values


def parse_csv(value: str) -> list[str]:
    values = [item.strip() for item in value.split(",") if item.strip()]
    if not values:
        raise ValueError("No CSV values parsed.")
    return values


def render_markdown(payload: dict[str, Any]) -> str:
    rows = sorted(
        payload["rows"],
        key=lambda row: (
            row["summary"]["recall_all@5"],
            row["summary"]["ndcg_any@5"],
            row["summary"]["mrr"],
        ),
        reverse=True,
    )
    lines = [
        "# Temporary uniform-layer BM25 check",
        "",
        "Same three product prompts, all forced to one layer and `anti_pca_both_k15`.",
        "",
        "| rank | scope | alpha | R@3 | NDCG@3 | R@5 | NDCG@5 | MRR | session_hit@5 | n |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(rows, start=1):
        summary = row["summary"]
        lines.append(
            f"| {index} | `{row['bm25_scope']}` | {row['alpha']:.2f} | "
            f"{summary['recall_all@3']:.3f} | {summary['ndcg_any@3']:.3f} | "
            f"{summary['recall_all@5']:.3f} | {summary['ndcg_any@5']:.3f} | "
            f"{summary['mrr']:.3f} | {summary['session_hit@5']:.3f} | {summary['n_scored']} |"
        )
    lines.extend(["", "## Config", ""])
    for cell_item in payload["inputs"]["config"]["cells"]:
        lines.append(
            f"- `{cell_item['variant']}` L{cell_item['layer']} `{cell_item['score_mode']}`"
        )
    lines.append("")
    lines.append(f"elapsed_seconds: {payload['elapsed_seconds']:.1f}")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
