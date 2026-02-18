from __future__ import annotations

from typing import Union

TimecodeValue = Union[str, float, int]


def parse_timecode(value: TimecodeValue) -> float:
    """Parse a timecode like '1:12' or seconds as float and return seconds."""
    if isinstance(value, (int, float)):
        return float(value)

    text = value.strip()
    if not text:
        raise ValueError("Timecode cannot be empty.")

    if ":" not in text:
        try:
            return float(text)
        except ValueError as exc:
            raise ValueError(f"Invalid timecode: {value}") from exc

    parts = text.split(":")
    if len(parts) > 3:
        raise ValueError(f"Invalid timecode: {value}")

    try:
        seconds = float(parts[-1])
        minutes = int(parts[-2]) if len(parts) >= 2 else 0
        hours = int(parts[-3]) if len(parts) == 3 else 0
    except ValueError as exc:
        raise ValueError(f"Invalid timecode: {value}") from exc

    if seconds < 0 or minutes < 0 or hours < 0:
        raise ValueError(f"Invalid timecode: {value}")

    return hours * 3600 + minutes * 60 + seconds
