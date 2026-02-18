"""Concatenate multiple video files using ffmpeg."""

from __future__ import annotations

from pathlib import Path
from typing import List

from videotools.ffmpeg import run_ffmpeg
from videotools.paths import PROCESSED_DIR, TEMP_DIR, ensure_directories


def concat_videos(
    input_files: List[Path],
    output_file: Path | None = None,
    output_dir: Path | None = None,
) -> Path:
    """Concatenate multiple video files into a single output file."""
    if not input_files:
        raise ValueError("At least one input file is required.")

    for file in input_files:
        if not file.exists():
            raise FileNotFoundError(f"Input file not found: {file}")

    ensure_directories()
    if output_file is None:
        if output_dir is None:
            output_dir = PROCESSED_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        first_file = input_files[0]
        output_file = output_dir / f"{first_file.stem}_concat{first_file.suffix}"

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    list_path = TEMP_DIR / "concat_list.txt"
    list_contents = "\n".join(
        f"file '{_escape_concat_path(file.resolve())}'" for file in input_files
    )
    list_path.write_text(list_contents, encoding="utf-8")

    args = [
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_path),
        "-c",
        "copy",
        "-y",
        str(output_file),
    ]
    try:
        run_ffmpeg(args)
    finally:
        if list_path.exists():
            list_path.unlink()
    return output_file


def _escape_concat_path(path: Path) -> str:
    path_str = str(path)
    replacements = {
        "\\": "\\\\",
        "'": "\\'",
        "\n": "\\n",
        "\r": "",
    }
    for old, new in replacements.items():
        path_str = path_str.replace(old, new)
    return path_str
