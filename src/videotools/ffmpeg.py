"""FFmpeg subprocess wrapper utilities."""

import subprocess
from pathlib import Path
from typing import List, Optional


class FFmpegError(Exception):
    """Exception raised when ffmpeg command fails."""
    pass


def check_ffmpeg_installed() -> bool:
    """
    Check if ffmpeg is installed and available.
    
    Returns:
        True if ffmpeg is installed, False otherwise
    """
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def run_ffmpeg(args: List[str], capture_output: bool = False) -> Optional[str]:
    """
    Run an ffmpeg command with the given arguments.
    
    Args:
        args: List of ffmpeg arguments (without 'ffmpeg' command itself)
        capture_output: If True, capture and return output
        
    Returns:
        Command output if capture_output is True, None otherwise
        
    Raises:
        FFmpegError: If the ffmpeg command fails
    """
    cmd = ["ffmpeg"] + args
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=True
        )
        if capture_output:
            return result.stdout
        return None
    except subprocess.CalledProcessError as e:
        error_msg = f"FFmpeg command failed: {' '.join(cmd)}"
        if e.stderr:
            error_msg += f"\nError: {e.stderr}"
        raise FFmpegError(error_msg) from e
    except FileNotFoundError:
        raise FFmpegError(
            "ffmpeg not found. Please ensure ffmpeg is installed and in PATH."
        )


def cut_video(
    input_file: Path,
    output_file: Path,
    start_time: int,
    duration: Optional[int] = None,
    end_time: Optional[int] = None,
    overwrite: bool = True
) -> None:
    """
    Cut a video segment using ffmpeg.
    
    Args:
        input_file: Path to input video file
        output_file: Path to output video file
        start_time: Start time in seconds
        duration: Duration in seconds (mutually exclusive with end_time)
        end_time: End time in seconds (mutually exclusive with duration)
        overwrite: If True, overwrite output file if it exists
        
    Raises:
        ValueError: If both duration and end_time are provided or neither is provided
        FFmpegError: If the ffmpeg command fails
    """
    if duration is None and end_time is None:
        raise ValueError("Either duration or end_time must be provided")
    
    if duration is not None and end_time is not None:
        raise ValueError("Cannot specify both duration and end_time")
    
    if end_time is not None:
        if end_time <= start_time:
            raise ValueError("end_time must be greater than start_time")
        duration = end_time - start_time
    
    args = [
        "-ss", str(start_time),
        "-i", str(input_file),
        "-t", str(duration),
        "-c", "copy",  # Copy codec for fast processing
    ]
    
    if overwrite:
        args.append("-y")
    
    args.append(str(output_file))
    
    run_ffmpeg(args)
