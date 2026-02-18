"""Cut fixed-duration clips from specified timestamps."""

from __future__ import annotations

from pathlib import Path
from typing import List

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import PROCESSED_DIR, ensure_directories
from videotools.timecode import parse_timecode, sanitize_timecode_label


def cut_fixed_clips(
    input_file: Path,
    timestamps: List[str],
    duration: float = 60.0,
    output_dir: Path | None = None,
    copy_streams: bool = False,
) -> List[Path]:
    """Cut fixed-duration clips from specified timestamps."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    ensure_directories()
    if output_dir is None:
        output_dir = PROCESSED_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    output_files: List[Path] = []
    for timestamp in timestamps:
        start_seconds = parse_timecode(timestamp)
        timestamp_label = sanitize_timecode_label(timestamp)
        output_file = output_dir / f"{input_file.stem}_clip_{timestamp_label}{input_file.suffix}"

        args = ["-i", str(input_file), "-ss", str(start_seconds), "-t", str(duration)]
        if copy_streams:
            args += ["-c", "copy"]
        args += ["-y", str(output_file)]
        run_ffmpeg(args)
        output_files.append(output_file)

    return output_files
