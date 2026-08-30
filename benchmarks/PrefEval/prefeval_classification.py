"""Prepare and score PrefEval multiple-choice classification prompts.

This script does not run an LLM. It follows PrefEval's automatic
classification direction by converting rows with answer options into JSONL
prompts and by scoring model predictions afterward. The intended first target
is `implicit_choice`, because that dataset contains `options` and `aligned_op`
fields. `implicit_persona` does not provide official multiple-choice options in
the HuggingFace rows we currently cache, so this script refuses to synthesize
unofficial choices for it.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BENCH_DIR = Path(__file__).resolve().parent
DATASETS = {
    "explicit": "siyanzhao/prefeval_explicit",
    "implicit_choice": "siyanzhao/prefeval_implicit_choice",
    "implicit_persona": "siyanzhao/prefeval_implicit_persona",
}
DEFAULT_OUTPUT_DIR = BENCH_DIR / "classification"
LETTER_RE = re.compile(r"\b([A-Z])\b", re.I)

os.environ.setdefault("HF_HOME", str(BENCH_DIR / ".hf_home"))
os.environ.setdefault("HF_DATASETS_CACHE", str(BENCH_DIR / ".hf_home" / "datasets"))
os.environ.setdefault("HF_HUB_CACHE", str(BENCH_DIR / ".hf_home" / "hub"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["prepare", "score"], default="prepare")
    parser.add_argument("--task", choices=sorted(DATASETS), default="implicit_choice")
    parser.add_argument("--split", default="train")
    parser.add_argument("--limit", type=int, default=0, help="0 means all rows.")
    parser.add_argument("--shuffle-seed", type=int, default=0)
    parser.add_argument(
        "--turn-limit",
        type=int,
        default=300,
        help="Maximum conversation turns to include when a row has conversation turns.",
    )
    parser.add_argument(
        "--reminder",
        choices=["with", "without", "both"],
        default="both",
        help="Whether to include an explicit preference reminder in the prompt.",
    )
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--output-prefix", default=None)
    parser.add_argument("--input-jsonl", default=None, help="Prepared JSONL to score.")
    parser.add_argument("--predictions-jsonl", default=None, help="JSONL with id plus prediction fields.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "prepare":
        path = prepare(args)
        print(f"wrote {path}")
        return 0
    score(args)
    return 0


def prepare(args: argparse.Namespace) -> Path:
    from datasets import load_dataset

    dataset_id = DATASETS[args.task]
    print(f"loading {dataset_id} split={args.split} cache={os.environ['HF_DATASETS_CACHE']}")
    dataset = load_dataset(dataset_id, split=args.split, cache_dir=os.environ["HF_DATASETS_CACHE"])
    if args.shuffle_seed >= 0:
        dataset = dataset.shuffle(seed=args.shuffle_seed)
    if args.limit and args.limit > 0:
        dataset = dataset.select(range(min(args.limit, len(dataset))))

    modes = ["with", "without"] if args.reminder == "both" else [args.reminder]
    items: list[dict[str, Any]] = []
    skipped = 0
    for row_index, row in enumerate(dataset):
        row_dict = dict(row)
        try:
            choices, answer_index = extract_choices(row_dict)
        except ValueError:
            skipped += 1
            continue
        for reminder_mode in modes:
            item_id = f"{args.task}:{row_index:04d}:{reminder_mode}_reminder"
            items.append(
                {
                    "id": item_id,
                    "task": args.task,
                    "dataset": dataset_id,
                    "reminder_mode": reminder_mode,
                    "turn_limit": args.turn_limit,
                    "prompt": build_prompt(row_dict, choices, reminder_mode=reminder_mode, turn_limit=args.turn_limit),
                    "choices": choices,
                    "answer_index": answer_index,
                    "answer_letter": index_to_letter(answer_index),
                    "answer": choices[answer_index],
                    "metadata": {
                        "topic": clean_text(row_dict.get("topic", "")),
                        "preference_type": clean_text(row_dict.get("preference_type", args.task)),
                    },
                }
            )

    if not items:
        raise ValueError(
            f"No multiple-choice rows found for task={args.task}. "
            "Use `implicit_choice` unless the official dataset adds options for this task."
        )

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_prefix or default_prefix(args)
    path = output_dir / f"{prefix}.jsonl"
    with path.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"prepared={len(items)} skipped_no_options={skipped}")
    return path


def score(args: argparse.Namespace) -> None:
    if not args.input_jsonl:
        raise ValueError("--input-jsonl is required for --mode score")
    if not args.predictions_jsonl:
        raise ValueError("--predictions-jsonl is required for --mode score")

    items = {item["id"]: item for item in read_jsonl(Path(args.input_jsonl))}
    predictions = {item["id"]: item for item in read_jsonl(Path(args.predictions_jsonl))}
    totals: dict[str, int] = defaultdict(int)
    correct: dict[str, int] = defaultdict(int)
    missing = 0
    for item_id, item in items.items():
        prediction = predictions.get(item_id)
        if prediction is None:
            missing += 1
            continue
        pred_index = parse_prediction_index(prediction, item["choices"])
        mode = item.get("reminder_mode", "unknown")
        totals[mode] += 1
        correct[mode] += int(pred_index == item["answer_index"])

    rows = []
    for mode in sorted(totals):
        rows.append({"reminder_mode": mode, "n": totals[mode], "accuracy": correct[mode] / max(totals[mode], 1)})
    rows.append(
        {
            "reminder_mode": "all",
            "n": sum(totals.values()),
            "accuracy": sum(correct.values()) / max(sum(totals.values()), 1),
            "missing": missing,
        }
    )
    payload = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "input_jsonl": args.input_jsonl,
        "predictions_jsonl": args.predictions_jsonl,
        "rows": rows,
    }
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.output_prefix or f"classification_score_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    json_path = output_dir / f"{prefix}.json"
    md_path = output_dir / f"{prefix}.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_score_markdown(payload), encoding="utf-8")
    print(render_score_markdown(payload), end="")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


def extract_choices(row: dict[str, Any]) -> tuple[list[str], int]:
    raw_options = row.get("options")
    aligned = clean_text(row.get("aligned_op", ""))
    if raw_options is None:
        raise ValueError("row has no options")
    if isinstance(raw_options, str):
        try:
            parsed = json.loads(raw_options)
        except json.JSONDecodeError:
            parsed = [part.strip() for part in re.split(r"\n+|\s*\|\s*", raw_options) if part.strip()]
        raw_options = parsed
    if not isinstance(raw_options, list):
        raise ValueError("options is not a list")
    choices = [clean_text(option.get("text", option) if isinstance(option, dict) else option) for option in raw_options]
    choices = [choice for choice in choices if choice]
    if len(choices) < 2:
        raise ValueError("need at least two choices")
    answer_index = find_answer_index(choices, aligned)
    return choices, answer_index


def find_answer_index(choices: list[str], aligned: str) -> int:
    aligned_key = normalize(aligned)
    for index, choice in enumerate(choices):
        if normalize(choice) == aligned_key:
            return index
    for index, choice in enumerate(choices):
        if aligned_key and (aligned_key in normalize(choice) or normalize(choice) in aligned_key):
            return index
    raise ValueError("aligned_op does not match options")


def build_prompt(row: dict[str, Any], choices: list[str], *, reminder_mode: str, turn_limit: int) -> str:
    parts = [
        "Choose the option that best respects the user's preference.",
        "Return only the option letter.",
        "",
    ]
    if reminder_mode == "with":
        parts.extend(["Reminder:", clean_text(row.get("preference", "")), ""])
    conversation = format_conversation(row.get("conversation"), turn_limit=turn_limit)
    if conversation:
        parts.extend(["Conversation:", conversation, ""])
    implicit_query = clean_text(row.get("implicit_query", ""))
    if implicit_query:
        parts.extend(["Preference-revealing query:", implicit_query, ""])
    question = clean_text(row.get("question", ""))
    if question:
        parts.extend(["Current user request:", question, ""])
    parts.append("Options:")
    for index, choice in enumerate(choices):
        parts.append(f"{index_to_letter(index)}. {choice}")
    return "\n".join(parts).strip() + "\n"


def format_conversation(raw: Any, *, turn_limit: int) -> str:
    if raw is None:
        return ""
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return clean_text(raw)
    if not isinstance(raw, dict):
        return clean_text(raw)
    if any(key in raw for key in ("query", "assistant_options", "user_selection", "assistant_acknowledgment")):
        ordered = [
            ("User", raw.get("query")),
            ("Assistant", raw.get("assistant_options")),
            ("User", raw.get("user_selection")),
            ("Assistant", raw.get("assistant_acknowledgment")),
        ]
        return "\n".join(f"{role}: {clean_text(text)}" for role, text in ordered if clean_text(text))
    lines: list[str] = []
    for key in sorted(raw, key=turn_sort_key):
        if len(lines) // 2 >= turn_limit:
            break
        turn = raw[key]
        if not turn:
            continue
        if isinstance(turn, dict):
            user = clean_text(turn.get("user") or turn.get("query") or turn.get("user_selection") or "")
            assistant = clean_text(turn.get("assistant") or turn.get("assistant_options") or turn.get("assistant_acknowledgment") or "")
            if user:
                lines.append(f"User: {user}")
            if assistant:
                lines.append(f"Assistant: {assistant}")
        else:
            text = clean_text(turn)
            if text:
                lines.append(text)
    return "\n".join(lines)


def turn_sort_key(value: Any) -> tuple[int, str]:
    text = str(value)
    match = re.search(r"\d+", text)
    return (int(match.group(0)) if match else 10_000, text)


def parse_prediction_index(prediction: dict[str, Any], choices: list[str]) -> int | None:
    for key in ("prediction_index", "answer_index", "choice_index"):
        if key in prediction:
            try:
                return int(prediction[key])
            except (TypeError, ValueError):
                pass
    text = clean_text(
        prediction.get("prediction")
        or prediction.get("answer")
        or prediction.get("choice")
        or prediction.get("output")
        or ""
    )
    match = LETTER_RE.search(text)
    if match:
        index = ord(match.group(1).upper()) - ord("A")
        if 0 <= index < len(choices):
            return index
    key = normalize(text)
    for index, choice in enumerate(choices):
        if normalize(choice) == key:
            return index
    return None


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def render_score_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# PrefEval Classification Score",
        "",
        f"- Created UTC: `{payload['created_utc']}`",
        f"- Input: `{payload['input_jsonl']}`",
        f"- Predictions: `{payload['predictions_jsonl']}`",
        "",
        "| reminder_mode | n | accuracy | missing |",
        "|---|---:|---:|---:|",
    ]
    for row in payload["rows"]:
        lines.append(
            f"| `{row['reminder_mode']}` | {row['n']} | {row['accuracy']:.3f} | {row.get('missing', '')} |"
        )
    return "\n".join(lines) + "\n"


def index_to_letter(index: int) -> str:
    return chr(ord("A") + index)


def clean_text(value: Any) -> str:
    return "" if value is None else " ".join(str(value).split())


def normalize(value: Any) -> str:
    return clean_text(value).casefold()


def default_prefix(args: argparse.Namespace) -> str:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    limit = "all" if not args.limit else f"n{args.limit}"
    return f"{args.task}_classification_{limit}_{args.reminder}_turn{args.turn_limit}_{stamp}"


if __name__ == "__main__":
    raise SystemExit(main())
