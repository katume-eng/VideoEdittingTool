# video-tools

A Python CLI toolkit for small video editing utilities using ffmpeg.

## Features

- **Cut Fixed Clips**: Cut 1-minute clips (or custom duration) from specified timestamps
- **Cut by Duration**: Cut a clip using start time and duration
- Extensible architecture for adding new video operations

## Prerequisites

- Python 3.8 or higher
- ffmpeg installed and available in PATH

## Installation

```bash
pip install -e .
```

## Usage

### Cut Fixed-Duration Clips

Cut multiple 1-minute clips from specified timestamps:

```bash
video-tools cut-fixed video.mp4 0:00 1:12 3:25
```

Cut clips with custom duration (30 seconds):

```bash
video-tools cut-fixed video.mp4 0:00 1:12 3:25 --duration 30
```

Specify output directory and filename prefix:

```bash
video-tools cut-fixed video.mp4 0:00 1:12 --output-dir ./clips --prefix segment
```

### Cut Clip by Duration

Cut a single clip starting at 1:12 for 30 seconds:

```bash
video-tools cut-duration video.mp4 1:12 30
```

Cut a clip with custom output file:

```bash
video-tools cut-duration video.mp4 0:01:12 1:00 --output my_clip.mp4
```

### Timecode Formats

Timestamps support multiple formats:
- Seconds: `90` (90 seconds)
- MM:SS: `1:30` (1 minute 30 seconds)
- HH:MM:SS: `0:01:30` (1 minute 30 seconds)

## Project Structure

```
src/videotools/
├── __init__.py
├── cli.py           # Main CLI application (Typer)
├── timecode.py      # Timecode parsing utilities
├── ffmpeg.py        # FFmpeg subprocess wrapper
└── ops/
    ├── __init__.py
    ├── cut_fixed.py     # Cut fixed-duration clips
    └── cut_duration.py  # Cut by duration
```

## Development

The project uses a src layout for better package organization and follows best practices for CLI tool development.

### Adding New Operations

To add new video operations:

1. Create a new module in `src/videotools/ops/`
2. Implement your operation function
3. Add a new command in `cli.py` using Typer decorators

## License

MIT
