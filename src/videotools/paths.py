from __future__ import annotations

from pathlib import Path

BASE_DATA_DIR = Path("data")
VIDEO_DIR = BASE_DATA_DIR / "video"
RAW_DIR = VIDEO_DIR / "raw"
PROCESSED_DIR = VIDEO_DIR / "processed"
TEMP_DIR = VIDEO_DIR / "temp"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path
