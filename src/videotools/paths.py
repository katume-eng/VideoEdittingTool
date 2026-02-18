"""Path utilities for default video tool directories."""

from __future__ import annotations

from pathlib import Path

DATA_DIR = Path("data")
VIDEO_DIR = DATA_DIR / "video"
RAW_DIR = VIDEO_DIR / "raw"
PROCESSED_DIR = VIDEO_DIR / "processed"
TEMP_DIR = DATA_DIR / "temp"


def ensure_directories() -> None:
    """Ensure default data directories exist."""
    for directory in (DATA_DIR, VIDEO_DIR, RAW_DIR, PROCESSED_DIR, TEMP_DIR):
        directory.mkdir(parents=True, exist_ok=True)
