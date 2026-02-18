"""Probe video metadata using ffprobe."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from videotools.ffmpeg import run_ffprobe


def probe_video(input_file: Path) -> Dict[str, Any]:
    """Return metadata for a video file."""
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    output = run_ffprobe(
        [
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate",
            "-of",
            "json",
            str(input_file),
        ],
        capture_output=True,
    )
    data = json.loads(output or "{}")
    streams = data.get("streams", [])
    format_info = data.get("format", {})

    video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})

    duration = float(format_info.get("duration", 0.0))
    width = video_stream.get("width", 0)
    height = video_stream.get("height", 0)
    fps = _parse_frame_rate(video_stream.get("r_frame_rate", "0"))

    return {
        "duration": duration,
        "resolution": f"{width}x{height}",
        "fps": fps,
        "video_codec": video_stream.get("codec_name", "unknown"),
        "audio_codec": audio_stream.get("codec_name", "unknown"),
    }


def _parse_frame_rate(rate: str) -> float:
    if not rate:
        return 0.0
    if "/" in rate:
        numerator, denominator = rate.split("/", maxsplit=1)
        try:
            return float(numerator) / float(denominator)
        except (ValueError, ZeroDivisionError):
            return 0.0
    try:
        return float(rate)
    except ValueError:
        return 0.0
