"""Download LongMemEval cleaned datasets into ./data/.

MVP_Plan.md sections 4 and 8 use LongMemEval-M for official baseline
replication and LongMemEval-S for local method evaluation. The official cleaned
dataset is hosted at `xiaowu0162/longmemeval-cleaned` on HuggingFace and the
files are exposed through HF/Xet resolve URLs.

Downloads:

- longmemeval_s_cleaned.json: about 277 MB.
- longmemeval_m_cleaned.json: about 2.74 GB.

Why: Phase 1a must validate the local retrieval pipeline against public
LongMemEval anchors before the hidden-state method is evaluated.
"""

from __future__ import annotations

import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@dataclass(frozen=True)
class DataFile:
    name: str
    url: str
    expected_size: str

    @property
    def path(self) -> Path:
        return DATA_DIR / self.name


FILES = [
    DataFile(
        name="longmemeval_s_cleaned.json",
        url="https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_s_cleaned.json",
        expected_size="about 277 MB",
    ),
    DataFile(
        name="longmemeval_m_cleaned.json",
        url="https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_m_cleaned.json",
        expected_size="about 2.74 GB",
    ),
]


def download_file(item: DataFile) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if item.path.exists() and item.path.stat().st_size > 0:
        print(f"skip: {item.path} already exists")
        return

    tmp_path = item.path.with_suffix(item.path.suffix + ".part")
    print(f"download: {item.url} -> {item.path} ({item.expected_size})")
    try:
        with urllib.request.urlopen(item.url) as response, tmp_path.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024 * 8)
                if not chunk:
                    break
                output.write(chunk)
    except Exception as exc:  # pragma: no cover - depends on network/HF state
        raise RuntimeError(
            f"Failed to download {item.name}. Remove {tmp_path} if it is incomplete, "
            "check network access, and rerun this script."
        ) from exc

    tmp_path.replace(item.path)
    print(f"done: {item.path}")


def main() -> int:
    for item in FILES:
        download_file(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
