#!/usr/bin/env python3
"""Run the audio-to-video operation using a preset file."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from videotools.ops.audio_to_video import (
    audio_to_video,
    get_optional_preset_string,
    get_required_preset_path,
    load_audio_to_video_preset,
    resolve_preset_path,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a video from audio and an image.")
    parser.add_argument("--preset", required=True, help="Preset JSON/YAML file")
    args = parser.parse_args()

    preset_path = Path(args.preset)
    try:
        preset_data = load_audio_to_video_preset(preset_path)
        audio_path = get_required_preset_path(preset_data, "audio_path", preset_path)
        image_path = get_required_preset_path(preset_data, "image_path", preset_path)
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
            video_codec=get_optional_preset_string(preset_data, "video_codec") or "libx264",
            audio_codec=get_optional_preset_string(preset_data, "audio_codec") or "aac",
            audio_bitrate=get_optional_preset_string(preset_data, "audio_bitrate") or "192k",
            pixel_format=get_optional_preset_string(preset_data, "pixel_format") or "yuv420p",
        )
    except Exception as exc:  # noqa: BLE001 - script output
        print(f"Error ({exc.__class__.__name__}): {exc}", file=sys.stderr)
        sys.exit(1)

    print("✓ Successfully created video:")
    print(f"  {output_file}")


if __name__ == "__main__":
    main()
