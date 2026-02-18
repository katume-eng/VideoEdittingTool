"""Cut a clip using start time and duration."""

from pathlib import Path

from videotools.timecode import parse_timecode, format_timecode
from videotools.ffmpeg import cut_video


def cut_by_duration(
    input_file: Path,
    start_time: str,
    duration: str,
    output_file: Path = None,
    output_dir: Path = None
) -> Path:
    """
    Cut a clip using start time and duration.
    
    Args:
        input_file: Path to input video file
        start_time: Start time (e.g., "1:12" or "0:01:12")
        duration: Duration (e.g., "30" for 30 seconds, "1:00" for 1 minute)
        output_file: Path to output file (optional)
        output_dir: Directory for output file (used if output_file not specified)
        
    Returns:
        Path to created clip file
        
    Raises:
        ValueError: If timestamps are invalid
        FFmpegError: If ffmpeg command fails
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Parse timecodes
    start_seconds = parse_timecode(start_time)
    duration_seconds = parse_timecode(duration)
    
    # Generate output filename if not provided
    if output_file is None:
        if output_dir is None:
            output_dir = input_file.parent
        else:
            output_dir.mkdir(parents=True, exist_ok=True)
        
        input_stem = input_file.stem
        input_ext = input_file.suffix
        start_formatted = format_timecode(start_seconds).replace(':', '-')
        duration_formatted = format_timecode(duration_seconds).replace(':', '-')
        output_filename = f"{input_stem}_clip_{start_formatted}_dur_{duration_formatted}{input_ext}"
        output_file = output_dir / output_filename
    
    # Cut the video
    cut_video(
        input_file=input_file,
        output_file=output_file,
        start_time=start_seconds,
        duration=duration_seconds
    )
    
    return output_file
