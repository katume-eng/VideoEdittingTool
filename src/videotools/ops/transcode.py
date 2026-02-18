from __future__ import annotations

from pathlib import Path

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import ensure_dir


def transcode(input_path: Path, output_path: Path) -> Path:
    """Transcode to H.264/AAC in MP4 container."""
    ensure_dir(output_path.parent)
    args = [
        "-y",
        "-i",
        str(input_path),
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        str(output_path),
    ]
    run_ffmpeg(args)
    return output_path
