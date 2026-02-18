from __future__ import annotations

from pathlib import Path
import tempfile
from typing import Iterable

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import ensure_dir


def concat_videos(inputs: Iterable[Path], output_path: Path) -> Path:
    """Concatenate input videos into a single output file."""
    input_list = list(inputs)
    if not input_list:
        raise ValueError("At least one input file is required for concat.")

    ensure_dir(output_path.parent)

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as temp_file:
            temp_path = Path(temp_file.name)
            for item in input_list:
                temp_file.write(f"file '{item.as_posix()}'\n")

        args = [
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(temp_path),
            "-c",
            "copy",
            str(output_path),
        ]
        run_ffmpeg(args)
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()

    return output_path
