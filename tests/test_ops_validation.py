"""Tests for operation validation helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

import videotools.ops.cut_fixed as cut_fixed
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
