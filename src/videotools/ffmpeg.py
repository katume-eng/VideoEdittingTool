"""FFmpeg subprocess wrapper utilities."""

from __future__ import annotations

import subprocess
from typing import List, Optional


class FFmpegError(Exception):
    """Exception raised when ffmpeg or ffprobe command fails."""


def _run_command(command: List[str], capture_output: bool) -> Optional[str]:
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            check=True,
        )
        if capture_output:
            return result.stdout
        return None
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed: {' '.join(command)}"
        if e.stderr:
            error_msg += f"\nError: {e.stderr.strip()}"
        raise FFmpegError(error_msg) from e
    except FileNotFoundError as exc:
        raise FFmpegError(
            f"{command[0]} not found. Please ensure it is installed and in PATH."
        ) from exc


def ensure_ffmpeg_exists() -> None:
    """Ensure ffmpeg and ffprobe are installed and available."""
    for tool in ("ffmpeg", "ffprobe"):
        _run_command([tool, "-version"], capture_output=True)


def check_ffmpeg_installed() -> bool:
    """Return True if ffmpeg and ffprobe are installed, False otherwise."""
    try:
        ensure_ffmpeg_exists()
        return True
    except FFmpegError:
        return False


def run_ffmpeg(args: List[str], capture_output: bool = False) -> Optional[str]:
    """
    Run an ffmpeg command with the given arguments.

    Args:
        args: List of ffmpeg arguments (without the ffmpeg command itself)
        capture_output: If True, capture and return output

    Returns:
        Command output if capture_output is True, None otherwise
    """
    return _run_command(["ffmpeg"] + args, capture_output=capture_output)


def run_ffprobe(args: List[str], capture_output: bool = True) -> Optional[str]:
    """
    Run an ffprobe command with the given arguments.

    Args:
        args: List of ffprobe arguments (without the ffprobe command itself)
        capture_output: If True, capture and return output

    Returns:
        Command output if capture_output is True, None otherwise
    """
    return _run_command(["ffprobe"] + args, capture_output=capture_output)
