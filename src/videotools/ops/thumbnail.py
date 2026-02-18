"""Extract a thumbnail image from a video."""

from __future__ import annotations

from pathlib import Path

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import PROCESSED_DIR, ensure_directories
from videotools.timecode import parse_timecode


def extract_thumbnail(
    input_file: Path,
    timestamp: str,
    output_file: Path | None = None,
    output_dir: Path | None = None,
    image_format: str = "png",
) -> Path:
    """Extract a single frame at a specified timestamp."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    ensure_directories()
    if output_file is None:
        if output_dir is None:
            output_dir = PROCESSED_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{input_file.stem}_thumb.{image_format.lower()}"

    suffix = output_file.suffix.lower()
    if suffix not in {".png", ".jpg", ".jpeg"}:
        raise ValueError("Thumbnail output must be .png or .jpg/.jpeg.")

    timestamp_seconds = parse_timecode(timestamp)
    args = [
        "-i",
        str(input_file),
        "-ss",
        str(timestamp_seconds),
        "-frames:v",
        "1",
        "-y",
        str(output_file),
    ]
    run_ffmpeg(args)
    return output_file
