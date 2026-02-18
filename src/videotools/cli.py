"""Main CLI application for video-tools."""

from pathlib import Path
from typing import List, Optional

import typer
from typing_extensions import Annotated

from videotools.ffmpeg import check_ffmpeg_installed
from videotools.ops.cut_fixed import cut_fixed_clips
from videotools.ops.cut_duration import cut_by_duration

app = typer.Typer(
    name="video-tools",
    help="A CLI toolkit for video editing utilities using ffmpeg",
    add_completion=False
)


@app.callback()
def callback():
    """
    Video editing toolkit powered by ffmpeg.
    """
    if not check_ffmpeg_installed():
        typer.echo(
            "Error: ffmpeg is not installed or not found in PATH.",
            err=True
        )
        typer.echo(
            "Please install ffmpeg: https://ffmpeg.org/download.html",
            err=True
        )
        raise typer.Exit(1)


@app.command()
def cut_fixed(
    input_file: Annotated[Path, typer.Argument(help="Input video file", exists=True, dir_okay=False)],
    timestamps: Annotated[List[str], typer.Argument(help="Start timestamps (e.g., 0:00 1:12 3:25)")],
    duration: Annotated[int, typer.Option("--duration", "-d", help="Duration of each clip in seconds")] = 60,
    output_dir: Annotated[Optional[Path], typer.Option("--output-dir", "-o", help="Output directory")] = None,
    output_prefix: Annotated[str, typer.Option("--prefix", "-p", help="Output filename prefix")] = "clip"
):
    """
    Cut fixed-duration clips from specified timestamps.
    
    Example:
        video-tools cut-fixed video.mp4 0:00 1:12 3:25
        video-tools cut-fixed video.mp4 0:00 1:12 --duration 30
    """
    typer.echo(f"Processing: {input_file}")
    typer.echo(f"Cutting {len(timestamps)} clip(s) of {duration} seconds each...")
    
    try:
        output_files = cut_fixed_clips(
            input_file=input_file,
            timestamps=timestamps,
            duration=duration,
            output_dir=output_dir,
            output_prefix=output_prefix
        )
        
        typer.echo(f"\n✓ Successfully created {len(output_files)} clip(s):")
        for output_file in output_files:
            typer.echo(f"  - {output_file}")
            
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def cut_duration(
    input_file: Annotated[Path, typer.Argument(help="Input video file", exists=True, dir_okay=False)],
    start_time: Annotated[str, typer.Argument(help="Start time (e.g., 1:12 or 0:01:12)")],
    duration: Annotated[str, typer.Argument(help="Duration (e.g., 30 or 1:00)")],
    output_file: Annotated[Optional[Path], typer.Option("--output", "-o", help="Output file path")] = None,
    output_dir: Annotated[Optional[Path], typer.Option("--output-dir", help="Output directory")] = None
):
    """
    Cut a clip using start time and duration.
    
    Example:
        video-tools cut-duration video.mp4 1:12 30
        video-tools cut-duration video.mp4 0:01:12 1:00 --output clip.mp4
    """
    typer.echo(f"Processing: {input_file}")
    typer.echo(f"Cutting clip from {start_time} with duration {duration}...")
    
    try:
        output = cut_by_duration(
            input_file=input_file,
            start_time=start_time,
            duration=duration,
            output_file=output_file,
            output_dir=output_dir
        )
        
        typer.echo(f"\n✓ Successfully created clip:")
        typer.echo(f"  {output}")
        
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
