from __future__ import annotations

from pathlib import Path
from videotools.ffmpeg import run_ffmpeg
from videotools.paths import ensure_dir
from videotools.timecode import TimecodeValue, parse_timecode


def cut_clip(
    input_path: Path,
    start: TimecodeValue,
    duration: TimecodeValue,
    output_path: Path,
    copy: bool = False,
) -> Path:
    """Cut a clip from the input video using start and duration."""
    start_seconds = parse_timecode(start)
    duration_seconds = parse_timecode(duration)
    ensure_dir(output_path.parent)

    args = [
        "-y",
        "-i",
        str(input_path),
        "-ss",
        str(start_seconds),
        "-t",
        str(duration_seconds),
    ]
    if copy:
        args.extend(["-c", "copy"])
    args.append(str(output_path))
    run_ffmpeg(args)
    return output_path
