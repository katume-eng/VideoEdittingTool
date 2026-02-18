from __future__ import annotations

from pathlib import Path
from typing import Union

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import ensure_dir
from videotools.timecode import parse_timecode

TimecodeValue = Union[str, float, int]


def create_thumbnail(
    input_path: Path,
    timestamp: TimecodeValue,
    output_path: Path,
) -> Path:
    """Extract a single frame at the timestamp."""
    ensure_dir(output_path.parent)
    seconds = parse_timecode(timestamp)
    args = [
        "-y",
        "-ss",
        str(seconds),
        "-i",
        str(input_path),
        "-frames:v",
        "1",
        str(output_path),
    ]
    run_ffmpeg(args)
    return output_path
