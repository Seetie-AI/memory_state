"""Download Phase 0 models into repo-local ./models directories.

The user explicitly requested that model weights live inside this repository
rather than HuggingFace's default cache. That makes disk usage visible and
cleanup simple: remove ./models/ to delete the downloaded checkpoints.

Downloads:

- mlx-community/Qwen3.5-2B-bf16 -> ./models/Qwen3.5-2B-bf16/
  Expected size: about 4.4 GB.
- Qwen/Qwen3.5-2B -> ./models/Qwen3.5-2B-hf/
  Expected size: about 4.5 GB.
- facebook/contriever -> ./models/contriever/
  Expected size: about 440 MB.
- Qwen/Qwen3-Embedding-0.6B -> ./models/qwen3-embedding-0.6b/
  Expected size: about 1.2 GB.

The script is reentrant. A completed directory gets a .download_complete marker
and is skipped on later runs. If a prior download was interrupted, running the
script again lets huggingface_hub resume into the same local_dir.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from huggingface_hub import snapshot_download


ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


@dataclass(frozen=True)
class ModelDownload:
    repo_id: str
    local_name: str
    expected_size: str

    @property
    def local_dir(self) -> Path:
        return MODELS_DIR / self.local_name

    @property
    def marker(self) -> Path:
        return self.local_dir / ".download_complete"


DOWNLOADS = [
    ModelDownload(
        repo_id="mlx-community/Qwen3.5-2B-bf16",
        local_name="Qwen3.5-2B-bf16",
        expected_size="about 4.4 GB",
    ),
    ModelDownload(
        repo_id="Qwen/Qwen3.5-2B",
        local_name="Qwen3.5-2B-hf",
        expected_size="about 4.5 GB",
    ),
    ModelDownload(
        repo_id="facebook/contriever",
        local_name="contriever",
        expected_size="about 440 MB",
    ),
    ModelDownload(
        repo_id="Qwen/Qwen3-Embedding-0.6B",
        local_name="qwen3-embedding-0.6b",
        expected_size="about 1.2 GB",
    ),
]


def download_one(item: ModelDownload) -> None:
    if item.marker.exists():
        print(f"skip: {item.repo_id} already downloaded at {item.local_dir}")
        return

    item.local_dir.mkdir(parents=True, exist_ok=True)
    print(f"download: {item.repo_id} -> {item.local_dir} ({item.expected_size})")

    try:
        snapshot_download(
            repo_id=item.repo_id,
            local_dir=str(item.local_dir),
        )
    except Exception as exc:  # pragma: no cover - depends on network/HF state
        raise RuntimeError(
            f"Failed to download {item.repo_id} into {item.local_dir}. "
            "Check network access and available disk space, then rerun this script."
        ) from exc

    item.marker.write_text("ok\n", encoding="utf-8")
    print(f"done: {item.repo_id}")


def main() -> int:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    for item in DOWNLOADS:
        download_one(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
