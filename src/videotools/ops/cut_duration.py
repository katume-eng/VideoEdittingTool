"""Cut a clip using start time and duration."""

from __future__ import annotations

from pathlib import Path

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import PROCESSED_DIR, ensure_directories
from videotools.timecode import format_timecode, parse_timecode


def cut_by_duration(
    input_file: Path,
    start_time: str,
    duration: str,
    output_file: Path | None = None,
    output_dir: Path | None = None,
) -> Path:
    """Cut a clip using start time and duration."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    start_seconds = parse_timecode(start_time)
    duration_seconds = parse_timecode(duration)

    if output_file is None:
        ensure_directories()
        if output_dir is None:
            output_dir = PROCESSED_DIR
        output_dir.mkdir(parents=True, exist_ok=True)

        input_stem = input_file.stem
        input_ext = input_file.suffix
        start_formatted = format_timecode(start_seconds).replace(":", "-").replace(".", "_")
        duration_formatted = format_timecode(duration_seconds).replace(":", "-").replace(".", "_")
        output_filename = f"{input_stem}_cut_{start_formatted}_dur_{duration_formatted}{input_ext}"
        output_file = output_dir / output_filename

    args = [
        "-i",
        str(input_file),
        "-ss",
        str(start_seconds),
        "-t",
        str(duration_seconds),
        "-y",
        str(output_file),
    ]
    run_ffmpeg(args)
    return output_file
