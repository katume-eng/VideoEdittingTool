"""Transcode videos into a standard MP4 format."""

from __future__ import annotations

from pathlib import Path

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import PROCESSED_DIR, ensure_directories


def transcode_video(
    input_file: Path,
    output_file: Path | None = None,
    output_dir: Path | None = None,
) -> Path:
    """Convert a video to H.264 video + AAC audio in an MP4 container."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    ensure_directories()
    if output_file is None:
        if output_dir is None:
            output_dir = PROCESSED_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{input_file.stem}_transcoded.mp4"

    args = [
        "-i",
        str(input_file),
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        "-y",
        str(output_file),
    ]
    run_ffmpeg(args)
    return output_file
