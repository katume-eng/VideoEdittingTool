"""Normalize audio loudness using ffmpeg."""

from __future__ import annotations

from pathlib import Path

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import PROCESSED_DIR, ensure_directories


def normalize_audio(
    input_file: Path,
    output_file: Path | None = None,
    output_dir: Path | None = None,
) -> Path:
    """Normalize audio loudness using ffmpeg loudnorm filter."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    ensure_directories()
    if output_file is None:
        if output_dir is None:
            output_dir = PROCESSED_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{input_file.stem}_normalized{input_file.suffix}"

    args = ["-i", str(input_file), "-af", "loudnorm", "-y", str(output_file)]
    run_ffmpeg(args)
    return output_file
