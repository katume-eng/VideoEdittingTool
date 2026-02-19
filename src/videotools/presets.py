"""Preset loading utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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


def get_optional_preset_string(preset: dict[str, Any], key: str) -> str | None:
    """Return an optional string value from preset data."""
    value = preset.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Preset field '{key}' must be a string.")
    return value


def get_optional_preset_path(preset: dict[str, Any], key: str, preset_path: Path) -> Path | None:
    """Return an optional preset path value, resolving relative paths."""
    value = get_optional_preset_string(preset, key)
    if value is None:
        return None
    return resolve_preset_path(preset_path, value)


def get_required_preset_path(preset: dict[str, Any], key: str, preset_path: Path) -> Path:
    """Return a required preset path value, raising if missing."""
    value = get_optional_preset_path(preset, key, preset_path)
    if value is None:
        raise ValueError(f"Preset field '{key}' is required.")
    return value


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
