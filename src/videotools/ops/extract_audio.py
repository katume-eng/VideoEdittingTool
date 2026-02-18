from __future__ import annotations

from pathlib import Path

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import ensure_dir


def extract_audio(input_path: Path, output_path: Path) -> Path:
    """Extract the audio track into a standalone audio file."""
    ensure_dir(output_path.parent)
    suffix = output_path.suffix.lower()
    codec_args: list[str] = []

    if suffix == ".wav":
        codec_args = ["-acodec", "pcm_s16le"]
    elif suffix == ".mp3":
        codec_args = ["-acodec", "libmp3lame"]

    args = ["-y", "-i", str(input_path), "-vn", *codec_args, str(output_path)]
    run_ffmpeg(args)
    return output_path
