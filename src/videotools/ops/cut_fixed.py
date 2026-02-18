from __future__ import annotations

from pathlib import Path
from typing import Iterable

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import ensure_dir
from videotools.timecode import TimecodeValue, parse_timecode


def _label_for_timestamp(raw_value: str, seconds: float) -> str:
    label = raw_value.strip() if raw_value.strip() else f"{seconds:.3f}"
    return label.replace(":", "-").replace(".", "_")


def cut_fixed(
    input_path: Path,
    timestamps: Iterable[str],
    duration: TimecodeValue,
    out_dir: Path,
    copy: bool = False,
) -> list[Path]:
    """Cut fixed-duration clips starting at each timestamp."""
    duration_seconds = parse_timecode(duration)
    ensure_dir(out_dir)
    outputs: list[Path] = []

    for timestamp in timestamps:
        start_seconds = parse_timecode(timestamp)
        label = _label_for_timestamp(timestamp, start_seconds)
        output_path = out_dir / f"{input_path.stem}_{label}{input_path.suffix}"
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
        outputs.append(output_path)

    return outputs
