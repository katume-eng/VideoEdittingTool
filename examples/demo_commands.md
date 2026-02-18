# Demo commands

```bash
# Cut 60-second clips starting at specific timestamps
video-tools cut-fixed input.mp4 --at 0:00 --at 1:12 --out-dir data/video/processed

# Cut a single clip
video-tools cut input.mp4 --start 1:12 --duration 30 --out data/video/processed/clip.mp4

# Concatenate clips
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
