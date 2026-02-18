from __future__ import annotations

import shutil
import subprocess
from typing import Sequence


def ensure_ffmpeg_exists() -> None:
    """Ensure ffmpeg and ffprobe are available in PATH."""
    if shutil.which("ffmpeg") is None:
        raise RuntimeError("ffmpeg was not found in PATH.")
    if shutil.which("ffprobe") is None:
        raise RuntimeError("ffprobe was not found in PATH.")


def run_ffmpeg(args: Sequence[str]) -> None:
    """Run an ffmpeg command with the provided arguments."""
    ensure_ffmpeg_exists()
    subprocess.run(["ffmpeg", *args], check=True)


def run_ffprobe(args: Sequence[str]) -> str:
    """Run an ffprobe command and return stdout."""
    ensure_ffmpeg_exists()
    result = subprocess.run(
        ["ffprobe", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()
