---
name: obs-recording-setup
description: Configure OBS Studio for recording webinars, demos, and content via command-line and config files
tool: Video
product: Studio
difficulty: Setup
---

# Set Up OBS for Recording

## Prerequisites
- OBS Studio installed (download from obsproject.com, free and open-source)
- Microphone and optionally a webcam connected

## Steps

1. **Install OBS.** On macOS: `brew install --cask obs`. On Linux: `sudo apt install obs-studio`. On Windows: download the installer from obsproject.com.

2. **Configure recording settings.** Edit the OBS profile config or use the `--profile` flag. Set recording output:
   - Format: MKV (crash-safe, can be remuxed to MP4 later)
   - Encoder: x264 (CPU) or NVENC (NVIDIA GPU)
   - Quality: CRF 18-23 for high quality with reasonable file size
   - Resolution: 1920x1080 (1080p)

3. **Set up scenes and sources.** Create a scene configuration with sources:
   - **Display Capture** or **Window Capture** for screen recording
   - **Video Capture Device** for webcam overlay
   - **Audio Input Capture** for microphone
   Configure via OBS scene collection JSON or the `obs-websocket` API for programmatic control.

4. **Configure audio.** Add your microphone as an audio input source. Apply noise suppression filter (RNNoise recommended) and gain filter if needed. Set audio bitrate to 160kbps for clear speech.

5. **Set up hotkeys.** Configure Start/Stop Recording hotkeys in the OBS settings so recording can be controlled without switching windows. Alternatively, use the `obs-websocket` API for programmatic recording control:
   ```
   ws://localhost:4455 -> {"op": 6, "d": {"requestType": "StartRecord"}}
   ```

6. **Test recording.** Record 1 minute, play it back, and verify video quality, audio levels, and webcam positioning. Remux MKV to MP4 after recording: `ffmpeg -i recording.mkv -c copy recording.mp4`.
