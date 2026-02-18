# Demo Commands

```bash
# Cut fixed 60-second clips
video-tools cut-fixed input.mp4 --at 0:00 --at 1:12 --out-dir data/video/processed

# Cut a clip by start and duration
video-tools cut input.mp4 --start 1:12 --duration 30 --out clip.mp4

# Concatenate video files
video-tools concat intro.mp4 main.mp4 outro.mp4 --out merged.mp4

# Extract audio to WAV
video-tools extract-audio input.mp4 --format wav --out audio.wav

# Normalize audio loudness
video-tools normalize-audio audio.wav --out normalized.wav

# Transcode to MP4 (H.264/AAC)
video-tools transcode input.mov --out output.mp4

# Generate a thumbnail
video-tools thumbnail input.mp4 --at 0:05 --out thumb.png

# Probe metadata
video-tools probe input.mp4
```
