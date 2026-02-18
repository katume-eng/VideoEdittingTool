"""Cut fixed-duration clips from specified timestamps."""

from pathlib import Path
from typing import List

from videotools.timecode import parse_timecode, format_timecode
from videotools.ffmpeg import cut_video


def cut_fixed_clips(
    input_file: Path,
    timestamps: List[str],
    duration: int = 60,
    output_dir: Path = None,
    output_prefix: str = "clip"
) -> List[Path]:
    """
    Cut fixed-duration clips from specified timestamps.
    
    Args:
        input_file: Path to input video file
        timestamps: List of start timestamps (e.g., ["0:00", "1:12", "3:25"])
        duration: Duration of each clip in seconds (default: 60)
        output_dir: Directory for output files (default: same as input file)
        output_prefix: Prefix for output filenames (default: "clip")
        
    Returns:
        List of paths to created clip files
        
    Raises:
        ValueError: If timestamps are invalid
        FFmpegError: If ffmpeg command fails
    """
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    if output_dir is None:
        output_dir = input_file.parent
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
    
    output_files = []
    
    for i, timestamp in enumerate(timestamps, start=1):
        # Parse the timestamp
        start_seconds = parse_timecode(timestamp)
        
        # Generate output filename
        input_stem = input_file.stem
        input_ext = input_file.suffix
        output_filename = f"{output_prefix}_{i:03d}_{format_timecode(start_seconds).replace(':', '-')}{input_ext}"
        output_file = output_dir / output_filename
        
        # Cut the video
        cut_video(
            input_file=input_file,
            output_file=output_file,
            start_time=start_seconds,
            duration=duration
        )
        
        output_files.append(output_file)
    
    return output_files
