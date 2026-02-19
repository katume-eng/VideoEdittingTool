"""Tests for operation validation helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

import videotools.ops.cut_fixed as cut_fixed
from videotools.ops.audio_to_video import audio_to_video
from videotools.ops.concat import concat_videos
from videotools.ops.extract_audio import extract_audio
from videotools.ops.probe import _parse_frame_rate
from videotools.ops.thumbnail import extract_thumbnail
from videotools.timecode import format_timecode


def test_format_timecode_rejects_negative() -> None:
    with pytest.raises(ValueError):
        format_timecode(-1)


def test_concat_requires_inputs() -> None:
    with pytest.raises(ValueError):
        concat_videos([])


def test_extract_audio_rejects_invalid_extension(tmp_path: Path) -> None:
    input_file = tmp_path / "input.mp4"
    input_file.write_text("data")
    with pytest.raises(ValueError):
        extract_audio(input_file, output_file=tmp_path / "audio.flac")


def test_thumbnail_rejects_invalid_format(tmp_path: Path) -> None:
    input_file = tmp_path / "input.mp4"
    input_file.write_text("data")
    with pytest.raises(ValueError):
        extract_thumbnail(input_file, "0:00", image_format="gif")


def test_thumbnail_rejects_mismatched_format(tmp_path: Path) -> None:
    input_file = tmp_path / "input.mp4"
    input_file.write_text("data")
    with pytest.raises(ValueError):
        extract_thumbnail(
            input_file,
            "0:00",
            output_file=tmp_path / "thumb.jpg",
            image_format="png",
        )


def test_audio_to_video_rejects_non_mp4_output(tmp_path: Path) -> None:
    audio_file = tmp_path / "input.mp3"
    image_file = tmp_path / "image.jpg"
    audio_file.write_text("data")
    image_file.write_text("data")
    with pytest.raises(ValueError):
        audio_to_video(audio_file, image_file, output_file=tmp_path / "output.mov")


def test_audio_to_video_builds_args(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    audio_file = tmp_path / "input.mp3"
    image_file = tmp_path / "image.jpg"
    audio_file.write_text("data")
    image_file.write_text("data")
    calls: list[list[str]] = []

    def fake_run(args: list[str]) -> None:
        calls.append(args)

    monkeypatch.setattr("videotools.ops.audio_to_video.run_ffmpeg", fake_run)

    output_path = audio_to_video(
        audio_file=audio_file,
        image_file=image_file,
        output_dir=tmp_path,
        video_codec="libx264",
        audio_codec="aac",
        audio_bitrate="256k",
        pixel_format="yuv420p",
    )
    assert output_path.suffix == ".mp4"
    assert calls
    assert "-loop" in calls[0]
    assert "-shortest" in calls[0]
    assert "stillimage" in calls[0]


def test_parse_frame_rate_invalid_values() -> None:
    assert _parse_frame_rate("10/0") == 0.0
    assert _parse_frame_rate("bad") == 0.0


def test_cut_fixed_handles_float_duration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    input_file = tmp_path / "input.mp4"
    input_file.write_text("data")
    calls: list[list[str]] = []

    def fake_run(args: list[str]) -> None:
        calls.append(args)

    monkeypatch.setattr(cut_fixed, "run_ffmpeg", fake_run)

    outputs = cut_fixed.cut_fixed_clips(
        input_file=input_file,
        timestamps=["0:00"],
        duration=30.5,
        output_dir=tmp_path,
        copy_streams=False,
    )
    assert outputs
    assert "30.5" in calls[0]
    assert "-c" not in calls[0]


def test_cut_fixed_handles_copy_streams(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    input_file = tmp_path / "input.mp4"
    input_file.write_text("data")
    calls: list[list[str]] = []

    def fake_run(args: list[str]) -> None:
        calls.append(args)

    monkeypatch.setattr(cut_fixed, "run_ffmpeg", fake_run)

    cut_fixed.cut_fixed_clips(
        input_file=input_file,
        timestamps=["0:10"],
        duration=20,
        output_dir=tmp_path,
        copy_streams=True,
    )
    assert "-c" in calls[0]
    assert "copy" in calls[0]
