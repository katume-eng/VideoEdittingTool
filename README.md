# Video Tools

Video Tools is a growing CLI toolkit of small, composable video editing utilities powered by
`ffmpeg` and `ffprobe`. The goal is to capture practical workflows for clipping, splitting,
extracting audio, transcoding, and generating thumbnails.

## Requirements

- Python 3.11+
- `ffmpeg` and `ffprobe` available in your PATH

### Installing ffmpeg

- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **Windows (Chocolatey)**: `choco install ffmpeg`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Usage

```bash
# Cut 60-second clips from multiple timestamps
video-tools cut-fixed input.mp4 --at 0:00 --at 1:12 --out-dir data/video/processed

# Cut a single clip
video-tools cut input.mp4 --start 1:12 --duration 30 --out data/video/processed/clip.mp4

# Concatenate videos
video-tools concat clip1.mp4 clip2.mp4 --out data/video/processed/combined.mp4

# Extract audio
video-tools extract-audio input.mp4 --out data/video/processed/audio.wav

# Normalize audio
video-tools normalize-audio audio.wav --out data/video/processed/audio_normalized.wav

# Transcode to MP4 (H.264/AAC)
video-tools transcode input.mov --out data/video/processed/output.mp4

# Generate a thumbnail
video-tools thumbnail input.mp4 --at 0:05 --out data/video/processed/thumbnail.png

# Probe metadata
video-tools probe input.mp4
```

More examples are available in `examples/demo_commands.md`.

## Repository structure

- `src/videotools`: Python package and CLI entry point
- `data/video/raw`: Place raw input files here
- `data/video/processed`: Output assets are written here by default
- `data/video/temp`: Temporary files

More tools will be added over time as workflows grow.
