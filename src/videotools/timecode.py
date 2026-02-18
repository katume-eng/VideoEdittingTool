"""Timecode parsing and validation utilities."""

import re
from typing import Union


def parse_timecode(timecode: str) -> int:
    """
    Parse a timecode string into total seconds.
    
    Supports formats:
    - MM:SS (e.g., "1:30")
    - HH:MM:SS (e.g., "0:01:30")
    - Seconds as integer or float (e.g., "90" or "90.5")
    
    Args:
        timecode: The timecode string to parse
        
    Returns:
        Total seconds as integer
        
    Raises:
        ValueError: If timecode format is invalid
    """
    if isinstance(timecode, (int, float)):
        return int(timecode)
    
    timecode = timecode.strip()
    
    # Check if it's a plain number (seconds)
    try:
        return int(float(timecode))
    except ValueError:
        pass
    
    # Parse HH:MM:SS or MM:SS format
    pattern = r'^(\d+):([0-5]\d)(?::([0-5]\d))?$'
    match = re.match(pattern, timecode)
    
    if not match:
        raise ValueError(
            f"Invalid timecode format: {timecode}. "
            "Use HH:MM:SS, MM:SS, or seconds."
        )
    
    hours_or_minutes = int(match.group(1))
    minutes_or_seconds = int(match.group(2))
    seconds = match.group(3)
    
    if seconds is not None:
        # HH:MM:SS format
        hours = hours_or_minutes
        minutes = minutes_or_seconds
        seconds = int(seconds)
        return hours * 3600 + minutes * 60 + seconds
    else:
        # MM:SS format
        minutes = hours_or_minutes
        seconds = minutes_or_seconds
        return minutes * 60 + seconds


def format_timecode(seconds: Union[int, float]) -> str:
    """
    Format seconds into HH:MM:SS timecode string.
    
    Args:
        seconds: Total seconds
        
    Returns:
        Formatted timecode string (HH:MM:SS)
    """
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def validate_timecode(timecode: str) -> bool:
    """
    Validate if a timecode string is valid.
    
    Args:
        timecode: The timecode string to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        parse_timecode(timecode)
        return True
    except ValueError:
        return False
