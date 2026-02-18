from __future__ import annotations

from pathlib import Path

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import ensure_dir


def normalize_audio(input_path: Path, output_path: Path) -> Path:
    """Normalize loudness using ffmpeg loudnorm filter."""
    ensure_dir(output_path.parent)
    args = [
        "-y",
        "-i",
        str(input_path),
        "-filter:a",
        "loudnorm",
        str(output_path),
    ]
    run_ffmpeg(args)
    return output_path
