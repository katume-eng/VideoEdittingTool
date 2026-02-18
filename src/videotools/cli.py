from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer

from videotools import paths
from videotools.ops import (
    concat,
    cut_duration,
    cut_fixed,
    extract_audio,
    normalize_audio,
    probe,
    thumbnail,
    transcode,
)

app = typer.Typer(help="Modular video tools powered by ffmpeg.")


def _default_output(input_path: Path, suffix: str, out_dir: Path) -> Path:
    return out_dir / f"{input_path.stem}{suffix}"


@app.command("cut-fixed")
def cut_fixed_command(
    input_path: Path = typer.Argument(
        ..., help="Input video file.", exists=True, dir_okay=False
    ),
    at: List[str] = typer.Option(
        ..., "--at", help="Timestamp to start each clip.", show_default=False
    ),
    duration: str = typer.Option(
        "60", help="Clip duration (seconds or timecode)."
    ),
    out_dir: Path = typer.Option(
        paths.PROCESSED_DIR,
        "--out-dir",
        help="Directory for output clips.",
        file_okay=False,
    ),
    copy: bool = typer.Option(
        False, "--copy", help="Use stream copy mode instead of re-encode."
    ),
) -> None:
    outputs = cut_fixed.cut_fixed(
        input_path=input_path,
        timestamps=at,
        duration=duration,
        out_dir=out_dir,
        copy=copy,
    )
    for output in outputs:
        typer.echo(f"Created {output}")


@app.command("cut")
def cut_command(
    input_path: Path = typer.Argument(
        ..., help="Input video file.", exists=True, dir_okay=False
    ),
    start: str = typer.Option(
        ..., "--start", help="Start time (seconds or timecode)."
    ),
    duration: str = typer.Option(
        ..., "--duration", help="Clip duration (seconds or timecode)."
    ),
    out: Optional[Path] = typer.Option(
        None, "--out", help="Output clip path.", dir_okay=False
    ),
    copy: bool = typer.Option(
        False, "--copy", help="Use stream copy mode instead of re-encode."
    ),
) -> None:
    output_path = out or _default_output(
        input_path, "_clip" + input_path.suffix, paths.PROCESSED_DIR
    )
    output = cut_duration.cut_clip(
        input_path=input_path,
        start=start,
        duration=duration,
        output_path=output_path,
        copy=copy,
    )
    typer.echo(f"Created {output}")


@app.command("concat")
def concat_command(
    inputs: List[Path] = typer.Argument(
        ..., help="Input video files.", exists=True, dir_okay=False
    ),
    out: Path = typer.Option(
        ..., "--out", help="Output video file.", dir_okay=False
    ),
) -> None:
    output = concat.concat_videos(inputs, out)
    typer.echo(f"Created {output}")


@app.command("extract-audio")
def extract_audio_command(
    input_path: Path = typer.Argument(
        ..., help="Input video file.", exists=True, dir_okay=False
    ),
    out: Optional[Path] = typer.Option(
        None,
        "--out",
        help="Output audio file (wav or mp3).",
        dir_okay=False,
    ),
) -> None:
    output_path = out or _default_output(input_path, ".wav", paths.PROCESSED_DIR)
    output = extract_audio.extract_audio(input_path, output_path)
    typer.echo(f"Created {output}")


@app.command("normalize-audio")
def normalize_audio_command(
    input_path: Path = typer.Argument(
        ..., help="Input audio file.", exists=True, dir_okay=False
    ),
    out: Optional[Path] = typer.Option(
        None, "--out", help="Output audio file.", dir_okay=False
    ),
) -> None:
    output_path = out or _default_output(
        input_path, "_normalized" + input_path.suffix, paths.PROCESSED_DIR
    )
    output = normalize_audio.normalize_audio(input_path, output_path)
    typer.echo(f"Created {output}")


@app.command("transcode")
def transcode_command(
    input_path: Path = typer.Argument(
        ..., help="Input video file.", exists=True, dir_okay=False
    ),
    out: Optional[Path] = typer.Option(
        None, "--out", help="Output mp4 file.", dir_okay=False
    ),
) -> None:
    output_path = out or _default_output(input_path, ".mp4", paths.PROCESSED_DIR)
    output = transcode.transcode(input_path, output_path)
    typer.echo(f"Created {output}")


@app.command("thumbnail")
def thumbnail_command(
    input_path: Path = typer.Argument(
        ..., help="Input video file.", exists=True, dir_okay=False
    ),
    at: str = typer.Option(
        ..., "--at", help="Timestamp for thumbnail (seconds or timecode)."
    ),
    out: Optional[Path] = typer.Option(
        None, "--out", help="Output image file.", dir_okay=False
    ),
) -> None:
    output_path = out or _default_output(input_path, "_thumb.png", paths.PROCESSED_DIR)
    output = thumbnail.create_thumbnail(input_path, at, output_path)
    typer.echo(f"Created {output}")


@app.command("probe")
def probe_command(
    input_path: Path = typer.Argument(
        ..., help="Input video file.", exists=True, dir_okay=False
    ),
) -> None:
    info = probe.probe_file(input_path)
    typer.echo(f"Duration: {info.get('duration') or 'unknown'} seconds")
    typer.echo(f"Resolution: {info.get('resolution') or 'unknown'}")
    typer.echo(f"FPS: {info.get('fps') or 'unknown'}")
    typer.echo(
        f"Codecs: video={info.get('video_codec') or 'unknown'}, audio={info.get('audio_codec') or 'unknown'}"
    )


def main() -> None:
    app()


if __name__ == "__main__":
    main()
