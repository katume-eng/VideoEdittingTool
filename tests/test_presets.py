"""Tests for preset utilities."""

from __future__ import annotations

from pathlib import Path

import pytest

import videotools.presets as presets
from videotools.presets import (
    get_optional_preset_path,
    get_optional_preset_string,
    get_required_preset_path,
    load_audio_to_video_preset,
    resolve_preset_path,
)


def test_resolve_preset_path_relative(tmp_path: Path) -> None:
    preset_path = tmp_path / "preset.json"
    resolved = resolve_preset_path(preset_path, "media/audio.mp3")
    assert resolved == (tmp_path / "media/audio.mp3").resolve()


def test_get_optional_preset_string_rejects_non_string() -> None:
    with pytest.raises(ValueError):
        get_optional_preset_string({"audio_path": 123}, "audio_path")


def test_get_optional_preset_path_resolves_relative(tmp_path: Path) -> None:
    preset_path = tmp_path / "preset.json"
    resolved = get_optional_preset_path({"audio_path": "audio.mp3"}, "audio_path", preset_path)
    assert resolved == (tmp_path / "audio.mp3").resolve()


def test_get_required_preset_path_missing(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        get_required_preset_path({}, "audio_path", tmp_path / "preset.json")


def test_load_preset_rejects_invalid_extension(tmp_path: Path) -> None:
    preset_path = tmp_path / "preset.txt"
    preset_path.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError):
        load_audio_to_video_preset(preset_path)


def test_load_preset_rejects_non_object(tmp_path: Path) -> None:
    preset_path = tmp_path / "preset.json"
    preset_path.write_text("[1, 2]", encoding="utf-8")
    with pytest.raises(ValueError):
        load_audio_to_video_preset(preset_path)


def test_load_preset_yaml_support(tmp_path: Path) -> None:
    preset_path = tmp_path / "preset.yaml"
    preset_path.write_text("audio_path: audio.mp3\nimage_path: image.jpg\n", encoding="utf-8")
    if presets.yaml is None:
        with pytest.raises(ValueError):
            load_audio_to_video_preset(preset_path)
    else:
        data = load_audio_to_video_preset(preset_path)
        assert data["audio_path"] == "audio.mp3"
