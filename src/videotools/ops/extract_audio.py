"""Extract audio from a video file."""

from __future__ import annotations

from pathlib import Path

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import PROCESSED_DIR, ensure_directories


def extract_audio(
    input_file: Path,
    output_file: Path | None = None,
    output_dir: Path | None = None,
    audio_format: str = "wav",
) -> Path:
    """Extract audio track from a video file into WAV or MP3."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    ensure_directories()
    if output_file is None:
        if output_dir is None:
            output_dir = PROCESSED_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{input_file.stem}.{audio_format.lower()}"

    suffix = output_file.suffix.lower()
    if suffix == ".mp3":
        audio_args = ["-vn", "-acodec", "libmp3lame", "-q:a", "2"]
    elif suffix == ".wav":
        audio_args = ["-vn", "-acodec", "pcm_s16le"]
    else:
        raise ValueError("Output audio file must end with .wav or .mp3.")

    args = ["-i", str(input_file), *audio_args, "-y", str(output_file)]
    run_ffmpeg(args)
    return output_file
