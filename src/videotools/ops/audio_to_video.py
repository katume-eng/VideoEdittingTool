"""Create an MP4 video from an audio file and a still image."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import PROCESSED_DIR, ensure_directories

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


def resolve_preset_path(preset_path: Path, value: str) -> Path:
    """Resolve preset paths relative to the preset file location."""
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (preset_path.parent / path).resolve()
    return path


def load_audio_to_video_preset(preset_path: Path) -> dict[str, Any]:
    """Load audio-to-video preset data from JSON or YAML."""
    if not preset_path.exists():
        raise FileNotFoundError(f"Preset file not found: {preset_path}")

    suffix = preset_path.suffix.lower()
    if suffix == ".json":
        data = json.loads(preset_path.read_text(encoding="utf-8"))
    elif suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise ValueError("YAML presets require PyYAML to be installed.")
        data = yaml.safe_load(preset_path.read_text(encoding="utf-8"))
    else:
        raise ValueError("Preset file must be .json or .yaml/.yml.")

    if not isinstance(data, dict):
        raise ValueError("Preset data must be a JSON/YAML object.")
    return data


def audio_to_video(
    audio_file: Path,
    image_file: Path,
    output_file: Path | None = None,
    output_dir: Path | None = None,
    video_codec: str = "libx264",
    audio_codec: str = "aac",
    audio_bitrate: str = "192k",
    pixel_format: str = "yuv420p",
) -> Path:
    """Combine a still image with audio to create an MP4 video."""
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")
    if not image_file.exists():
        raise FileNotFoundError(f"Image file not found: {image_file}")

    ensure_directories()
    if output_file is None:
        if output_dir is None:
            output_dir = PROCESSED_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{audio_file.stem}_video.mp4"

    if output_file.suffix.lower() != ".mp4":
        raise ValueError("Output video file must end with .mp4.")

    args = [
        "-loop",
        "1",
        "-i",
        str(image_file),
        "-i",
        str(audio_file),
        "-c:v",
        video_codec,
        "-tune",
        "stillimage",
        "-c:a",
        audio_codec,
        "-b:a",
        audio_bitrate,
        "-pix_fmt",
        pixel_format,
        "-shortest",
        "-y",
        str(output_file),
    ]
    run_ffmpeg(args)
    return output_file
