from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from videotools.ffmpeg import run_ffprobe


def _parse_fps(value: str | None) -> str | None:
    if not value:
        return None
    if "/" in value:
        numerator, denominator = value.split("/", maxsplit=1)
        try:
            return f"{float(numerator) / float(denominator):.3f}"
        except ValueError:
            return value
    return value


def probe_file(input_path: Path) -> dict[str, Any]:
    """Return metadata about the video using ffprobe."""
    output = run_ffprobe(
        [
            "-v",
            "error",
            "-show_entries",
            "stream=index,codec_type,codec_name,width,height,avg_frame_rate",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(input_path),
        ]
    )
    data = json.loads(output)

    streams = data.get("streams", [])
    video_stream = next(
        (stream for stream in streams if stream.get("codec_type") == "video"),
        None,
    )
    audio_stream = next(
        (stream for stream in streams if stream.get("codec_type") == "audio"),
        None,
    )

    duration = data.get("format", {}).get("duration")
    resolution = None
    fps = None
    video_codec = None
    audio_codec = None

    if video_stream:
        width = video_stream.get("width")
        height = video_stream.get("height")
        if width and height:
            resolution = f"{width}x{height}"
        fps = _parse_fps(video_stream.get("avg_frame_rate"))
        video_codec = video_stream.get("codec_name")

    if audio_stream:
        audio_codec = audio_stream.get("codec_name")

    return {
        "duration": duration,
        "resolution": resolution,
        "fps": fps,
        "video_codec": video_codec,
        "audio_codec": audio_codec,
    }
