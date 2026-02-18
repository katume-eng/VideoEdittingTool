# video-tools

A modular Python CLI toolkit for small, composable video editing utilities powered by ffmpeg and ffprobe. The goal is to collect practical tools for real video-editing workflows (clipping, concatenation, audio extraction, transcoding, thumbnails, and more) and grow the toolbox over time.

## Requirements

- Python 3.11+
- ffmpeg and ffprobe installed and available in PATH

## Installation

```bash
pip install -e .
```

### Installing ffmpeg

Download ffmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and ensure both `ffmpeg` and `ffprobe` are on your PATH.

## Usage

### Cut fixed-duration clips

```bash
video-tools cut-fixed input.mp4 --at 0:00 --at 1:12 --out-dir data/video/processed
```

Use stream copy mode if desired:

```bash
video-tools cut-fixed input.mp4 --at 0:00 --at 1:12 --copy
```

### Cut by start and duration

```bash
video-tools cut input.mp4 --start 1:12 --duration 30 --out clip.mp4
```

### Concatenate videos

```bash
video-tools concat part1.mp4 part2.mp4 --out merged.mp4
```

### Extract audio

```bash
video-tools extract-audio input.mp4 --format mp3 --out audio.mp3
```

### Normalize audio

```bash
video-tools normalize-audio audio.wav --out normalized.wav
```

### Transcode to MP4 (H.264/AAC)

```bash
video-tools transcode input.mov --out output.mp4
```

### Generate a thumbnail

```bash
video-tools thumbnail input.mp4 --at 0:05 --out thumb.png
```

### Probe video metadata

```bash
video-tools probe input.mp4
```

## Timecode formats

Time-based arguments accept any of the following formats:

- Seconds: `90` or `90.5`
- MM:SS: `1:30`
- MM:SS.sss: `3:25.500`
- HH:MM:SS: `0:01:30`

## Project structure

```
src/videotools/
├── __init__.py
├── cli.py           # CLI entry point (Typer)
├── ffmpeg.py        # ffmpeg/ffprobe helpers
├── paths.py         # Default data directories
├── timecode.py      # Timecode parsing utilities
└── ops/             # Individual operations
```

## Extending the toolkit

1. Add a new operation module in `src/videotools/ops/`.
2. Implement a small, focused function that uses `run_ffmpeg` or `run_ffprobe`.
3. Register the command in `cli.py`.

More tools will be added over time as the repository grows.

## License

MIT
