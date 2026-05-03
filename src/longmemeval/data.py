"""LongMemEval cleaned JSON loading and text views.

This module implements the dataset interface described in MVP_Plan.md sections
4 and 5.3. The Phase 1a objective is to replicate official retrieval baselines
before testing the hidden-state method, so the loader preserves official field
names and exposes the same user-only session text view used by the LongMemEval
retrieval script.

Why user-only text exists: MVP_Plan.md section 5.3 records that official
Contriever/BM25 retrieval indexes only user turns for each session. We keep that
view for official-anchor replication and also expose full session text for later
fair hidden-state / long-context embedding comparisons.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


Turn = dict[str, Any]
Session = list[Turn]


@dataclass(frozen=True)
class Instance:
    question_id: str
    question: str
    answer: str
    question_type: str
    haystack_sessions: list[Session]
    answer_session_ids: list[str]
    is_abstention: bool
    haystack_session_ids: list[str]
    haystack_dates: list[str]
    question_date: str | None = None


def load_instances(path: str | Path) -> list[Instance]:
    """Load LongMemEval cleaned JSON into typed instances."""
    data_path = Path(path)
    with data_path.open("r", encoding="utf-8") as handle:
        raw_items = json.load(handle)

    if not isinstance(raw_items, list):
        raise ValueError(f"Expected list in {data_path}, got {type(raw_items)!r}")

    instances = [_parse_instance(item, data_path, index) for index, item in enumerate(raw_items)]
    return instances


def session_text_user_only(session: Session) -> str:
    """Return the official retrieval view: user turns joined by spaces."""
    return " ".join(
        str(turn.get("content", ""))
        for turn in session
        if turn.get("role") == "user" and turn.get("content") is not None
    )


def session_text_full(session: Session) -> str:
    """Return all user and assistant turns joined by spaces."""
    return " ".join(
        str(turn.get("content", ""))
        for turn in session
        if turn.get("content") is not None
    )


def has_user_side_answer_label(instance: Instance) -> bool:
    """Match official retrieval reporting: require a user turn with has_answer."""
    for session in instance.haystack_sessions:
        for turn in session:
            if turn.get("role") == "user" and bool(turn.get("has_answer", False)):
                return True
    return False


def _parse_instance(item: dict[str, Any], source: Path, index: int) -> Instance:
    required = [
        "question_id",
        "question",
        "answer",
        "question_type",
        "haystack_sessions",
        "answer_session_ids",
        "haystack_session_ids",
        "haystack_dates",
    ]
    missing = [key for key in required if key not in item]
    if missing:
        raise ValueError(f"{source}:{index} missing required fields: {missing}")

    haystack_sessions = item["haystack_sessions"]
    haystack_session_ids = item["haystack_session_ids"]
    haystack_dates = item["haystack_dates"]
    if not (
        isinstance(haystack_sessions, list)
        and isinstance(haystack_session_ids, list)
        and isinstance(haystack_dates, list)
    ):
        raise ValueError(f"{source}:{index} haystack fields must be lists")
    if not (len(haystack_sessions) == len(haystack_session_ids) == len(haystack_dates)):
        raise ValueError(
            f"{source}:{index} haystack_sessions/session_ids/dates length mismatch: "
            f"{len(haystack_sessions)} vs {len(haystack_session_ids)} vs {len(haystack_dates)}"
        )

    # Sanity check: official LongMemEval derives gold session IDs from
    # haystack_session_ids containing "answer". Cleaned data should already
    # have answer_session_ids populated to match. Catch schema drift early.
    expected_gold = {sid for sid in haystack_session_ids if "answer" in sid}
    declared_gold = {str(value) for value in item["answer_session_ids"]}
    if not declared_gold.issubset(expected_gold):
        raise ValueError(
            f"{source}:{index} answer_session_ids {declared_gold - expected_gold} "
            f"not present in haystack_session_ids containing 'answer': {expected_gold}"
        )

    question_id = str(item["question_id"])
    return Instance(
        question_id=question_id,
        question=str(item["question"]),
        answer=str(item["answer"]),
        question_type=str(item["question_type"]),
        haystack_sessions=haystack_sessions,
        answer_session_ids=[str(value) for value in item["answer_session_ids"]],
        is_abstention="_abs" in question_id,
        haystack_session_ids=[str(value) for value in haystack_session_ids],
        haystack_dates=[str(value) for value in haystack_dates],
        question_date=str(item["question_date"]) if item.get("question_date") is not None else None,
    )
