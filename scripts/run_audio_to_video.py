#!/usr/bin/env python3
"""Run the audio-to-video operation using a preset file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from videotools.ops.audio_to_video import (
    audio_to_video,
    load_audio_to_video_preset,
    resolve_preset_path,
)


def _get_required_preset_path(preset: dict[str, Any], key: str, preset_path: Path) -> Path:
    value = preset.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Preset field '{key}' is required.")
    return resolve_preset_path(preset_path, value)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a video from audio and an image.")
    parser.add_argument("--preset", required=True, help="Preset JSON/YAML file")
    args = parser.parse_args()

    preset_path = Path(args.preset)
    try:
        preset_data = load_audio_to_video_preset(preset_path)
        audio_path = _get_required_preset_path(preset_data, "audio_path", preset_path)
        image_path = _get_required_preset_path(preset_data, "image_path", preset_path)
        output_value = preset_data.get("output_path")
        output_path = (
            resolve_preset_path(preset_path, output_value)
            if isinstance(output_value, str)
            else None
        )

        output_file = audio_to_video(
            audio_file=audio_path,
            image_file=image_path,
            output_file=output_path,
            video_codec=str(preset_data.get("video_codec", "libx264")),
            audio_codec=str(preset_data.get("audio_codec", "aac")),
            audio_bitrate=str(preset_data.get("audio_bitrate", "192k")),
            pixel_format=str(preset_data.get("pixel_format", "yuv420p")),
        )
    except Exception as exc:  # noqa: BLE001 - script output
        print(f"Error ({exc.__class__.__name__}): {exc}", file=sys.stderr)
        sys.exit(1)

    print("✓ Successfully created video:")
    print(f"  {output_file}")


if __name__ == "__main__":
    main()
