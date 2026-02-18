"""Timecode parsing and validation utilities."""

from __future__ import annotations

from typing import Union


def parse_timecode(timecode: Union[str, int, float]) -> float:
    """
    Parse a timecode string into total seconds.

    Supports formats:
    - MM:SS (e.g., "1:30")
    - MM:SS.sss (e.g., "3:25.500")
    - HH:MM:SS (e.g., "0:01:30")
    - Seconds as integer or float (e.g., "90" or "90.5")
    """
    if isinstance(timecode, (int, float)):
        return float(timecode)

    value = timecode.strip()
    try:
        return float(value)
    except ValueError:
        pass

    parts = value.split(":")
    if len(parts) == 2:
        minutes = _parse_int(parts[0], "minutes")
        seconds = _parse_seconds(parts[1])
        if seconds >= 60:
            raise ValueError("Seconds must be less than 60.")
        return minutes * 60 + seconds
    if len(parts) == 3:
        hours = _parse_int(parts[0], "hours")
        minutes = _parse_int(parts[1], "minutes")
        seconds = _parse_seconds(parts[2])
        if minutes >= 60 or seconds >= 60:
            raise ValueError("Minutes and seconds must be less than 60.")
        return hours * 3600 + minutes * 60 + seconds

    raise ValueError(
        f"Invalid timecode format: {timecode}. "
        "Use HH:MM:SS, MM:SS, or seconds."
    )


def _parse_int(value: str, label: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ValueError(f"Invalid {label} value: {value}") from exc
    if parsed < 0:
        raise ValueError(f"{label.capitalize()} must be non-negative.")
    return parsed


def _parse_seconds(value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValueError(f"Invalid seconds value: {value}") from exc
    if parsed < 0:
        raise ValueError("Seconds must be non-negative.")
    return parsed


def format_timecode(seconds: Union[int, float]) -> str:
    """Format seconds into a HH:MM:SS(.sss) timecode string."""
    total_seconds = float(seconds)
    if total_seconds < 0:
        raise ValueError("Seconds must be non-negative.")
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    secs = float(total_seconds - hours * 3600 - minutes * 60)
    if secs.is_integer():
        seconds_str = f"{int(secs):02d}"
    else:
        seconds_str = f"{secs:06.3f}"
    return f"{hours:02d}:{minutes:02d}:{seconds_str}"


def validate_timecode(timecode: str) -> bool:
    """Validate if a timecode string is valid."""
    try:
        parse_timecode(timecode)
        return True
    except ValueError:
        return False


def sanitize_timecode_label(timecode: str) -> str:
    """Sanitize a timecode string for use in filenames."""
    return timecode.strip().replace(":", "-").replace(".", "_")
