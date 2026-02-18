"""Main CLI application for video-tools."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, List, Optional

import typer

from videotools.ffmpeg import FFmpegError, ensure_ffmpeg_exists
from videotools.ops.concat import concat_videos
from videotools.ops.cut_duration import cut_by_duration
from videotools.ops.cut_fixed import cut_fixed_clips
from videotools.ops.extract_audio import extract_audio
from videotools.ops.normalize_audio import normalize_audio
from videotools.ops.probe import probe_video
from videotools.ops.thumbnail import extract_thumbnail
from videotools.ops.transcode import transcode_video

app = typer.Typer(
    name="video-tools",
    help="A CLI toolkit for video editing utilities using ffmpeg",
    add_completion=False,
)


@app.callback()
def callback() -> None:
    """Video editing toolkit powered by ffmpeg."""
    try:
        ensure_ffmpeg_exists()
    except FFmpegError as exc:
        typer.echo(f"Error: {exc}", err=True)
        typer.echo("Please install ffmpeg: https://ffmpeg.org/download.html", err=True)
        raise typer.Exit(1)


@app.command("cut-fixed")
def cut_fixed(
    input_file: Annotated[Path, typer.Argument(help="Input video file", exists=True, dir_okay=False)],
    timestamps: Annotated[
        List[str],
        typer.Option(..., "--at", help="Start timestamps (e.g., --at 0:00 --at 1:12)"),
    ],
    duration: Annotated[
        float,
        typer.Option(60.0, "--duration", "-d", help="Duration of each clip in seconds"),
    ] = 60.0,
    output_dir: Annotated[
        Optional[Path],
        typer.Option(None, "--out-dir", help="Output directory for clips"),
    ] = None,
    copy_streams: Annotated[
        bool,
        typer.Option(False, "--copy", help="Use stream copy mode instead of re-encoding"),
    ] = False,
) -> None:
    """Cut fixed-duration clips from specified timestamps."""
    if not timestamps:
        typer.echo("Error: At least one --at timestamp is required.", err=True)
        raise typer.Exit(1)

    try:
        output_files = cut_fixed_clips(
            input_file=input_file,
            timestamps=timestamps,
            duration=duration,
            output_dir=output_dir,
            copy_streams=copy_streams,
        )
    except Exception as exc:  # noqa: BLE001 - CLI output
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo("\n✓ Successfully created clips:")
    for output_file in output_files:
        typer.echo(f"  - {output_file}")


@app.command("cut")
def cut(
    input_file: Annotated[Path, typer.Argument(help="Input video file", exists=True, dir_okay=False)],
    start_time: Annotated[str, typer.Option(..., "--start", help="Start time (e.g., 1:12)")],
    duration: Annotated[str, typer.Option(..., "--duration", help="Duration (e.g., 30 or 1:00)")],
    output_file: Annotated[
        Optional[Path],
        typer.Option(None, "--out", "-o", help="Output file"),
    ]
    = None,
    output_dir: Annotated[
        Optional[Path],
        typer.Option(None, "--out-dir", help="Output directory"),
    ]
    = None,
) -> None:
    """Cut a clip using start time and duration."""
    try:
        output_path = cut_by_duration(
            input_file=input_file,
            start_time=start_time,
            duration=duration,
            output_file=output_file,
            output_dir=output_dir,
        )
    except Exception as exc:  # noqa: BLE001 - CLI output
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo("\n✓ Successfully created clip:")
    typer.echo(f"  {output_path}")


@app.command("concat")
def concat(
    input_files: Annotated[
        List[Path],
        typer.Argument(help="Input video files", exists=True, dir_okay=False),
    ],
    output_file: Annotated[
        Optional[Path],
        typer.Option(None, "--out", "-o", help="Output file"),
    ]
    = None,
    output_dir: Annotated[
        Optional[Path],
        typer.Option(None, "--out-dir", help="Output directory"),
    ]
    = None,
) -> None:
    """Concatenate multiple videos into one output file."""
    try:
        output_path = concat_videos(input_files, output_file=output_file, output_dir=output_dir)
    except Exception as exc:  # noqa: BLE001 - CLI output
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo("\n✓ Successfully created concatenated video:")
    typer.echo(f"  {output_path}")


@app.command("extract-audio")
def extract_audio_cmd(
    input_file: Annotated[Path, typer.Argument(help="Input video file", exists=True, dir_okay=False)],
    output_file: Annotated[
        Optional[Path],
        typer.Option(None, "--out", "-o", help="Output audio file"),
    ]
    = None,
    output_dir: Annotated[
        Optional[Path],
        typer.Option(None, "--out-dir", help="Output directory"),
    ]
    = None,
    audio_format: Annotated[
        str,
        typer.Option("wav", "--format", help="Output format: wav or mp3"),
    ] = "wav",
) -> None:
    """Extract audio track from a video file."""
    try:
        output_path = extract_audio(
            input_file=input_file,
            output_file=output_file,
            output_dir=output_dir,
            audio_format=audio_format,
        )
    except Exception as exc:  # noqa: BLE001 - CLI output
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo("\n✓ Successfully extracted audio:")
    typer.echo(f"  {output_path}")


@app.command("normalize-audio")
def normalize_audio_cmd(
    input_file: Annotated[Path, typer.Argument(help="Input audio/video file", exists=True, dir_okay=False)],
    output_file: Annotated[
        Optional[Path],
        typer.Option(None, "--out", "-o", help="Output file"),
    ]
    = None,
    output_dir: Annotated[
        Optional[Path],
        typer.Option(None, "--out-dir", help="Output directory"),
    ]
    = None,
) -> None:
    """Normalize audio loudness using ffmpeg loudnorm."""
    try:
        output_path = normalize_audio(
            input_file=input_file,
            output_file=output_file,
            output_dir=output_dir,
        )
    except Exception as exc:  # noqa: BLE001 - CLI output
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo("\n✓ Successfully normalized audio:")
    typer.echo(f"  {output_path}")


@app.command("transcode")
def transcode(
    input_file: Annotated[Path, typer.Argument(help="Input video file", exists=True, dir_okay=False)],
    output_file: Annotated[
        Optional[Path],
        typer.Option(None, "--out", "-o", help="Output file"),
    ]
    = None,
    output_dir: Annotated[
        Optional[Path],
        typer.Option(None, "--out-dir", help="Output directory"),
    ]
    = None,
) -> None:
    """Transcode a video to H.264/AAC MP4."""
    try:
        output_path = transcode_video(
            input_file=input_file,
            output_file=output_file,
            output_dir=output_dir,
        )
    except Exception as exc:  # noqa: BLE001 - CLI output
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo("\n✓ Successfully transcoded video:")
    typer.echo(f"  {output_path}")


@app.command("thumbnail")
def thumbnail(
    input_file: Annotated[Path, typer.Argument(help="Input video file", exists=True, dir_okay=False)],
    timestamp: Annotated[str, typer.Option(..., "--at", help="Timestamp for thumbnail (e.g., 0:05)")],
    output_file: Annotated[
        Optional[Path],
        typer.Option(None, "--out", "-o", help="Output image file"),
    ]
    = None,
    output_dir: Annotated[
        Optional[Path],
        typer.Option(None, "--out-dir", help="Output directory"),
    ]
    = None,
    image_format: Annotated[
        str,
        typer.Option("png", "--format", help="Image format: png or jpg"),
    ] = "png",
) -> None:
    """Extract a thumbnail image from a video."""
    try:
        output_path = extract_thumbnail(
            input_file=input_file,
            timestamp=timestamp,
            output_file=output_file,
            output_dir=output_dir,
            image_format=image_format,
        )
    except Exception as exc:  # noqa: BLE001 - CLI output
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo("\n✓ Successfully created thumbnail:")
    typer.echo(f"  {output_path}")


@app.command("probe")
def probe(
    input_file: Annotated[Path, typer.Argument(help="Input video file", exists=True, dir_okay=False)],
) -> None:
    """Display metadata about a video file."""
    try:
        metadata = probe_video(input_file)
    except Exception as exc:  # noqa: BLE001 - CLI output
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(1)

    typer.echo("\n✓ Video metadata:")
    typer.echo(f"  Duration: {metadata['duration']:.2f} seconds")
    typer.echo(f"  Resolution: {metadata['resolution']}")
    typer.echo(f"  FPS: {metadata['fps']:.2f}")
    typer.echo(f"  Video codec: {metadata['video_codec']}")
    typer.echo(f"  Audio codec: {metadata['audio_codec']}")


if __name__ == "__main__":
    app()
