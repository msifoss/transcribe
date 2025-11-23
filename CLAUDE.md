# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based audio/video transcription tool that uses OpenAI's Whisper API for transcription and GPT-4o-mini for speaker diarization (labeling different speakers in the transcript).

## Architecture

The main script `tranbob.py` follows a two-stage pipeline:

1. **Audio Extraction** (optional): Uses ffmpeg to extract audio from MP4 files and convert to 16kHz mono WAV format
2. **Transcription**: Sends audio to OpenAI's Whisper API (via `client.audio.transcriptions.create()`)
3. **Speaker Labeling**: Sends raw transcript text to GPT-4o-mini via chat completion API to identify and label different speakers

## Environment Setup

Required dependencies:
- `openai` - OpenAI Python SDK (not currently installed)
- `python-dotenv` - Environment variable management
- `ffmpeg` - External binary for audio extraction (must be in PATH)

Configuration in `.env`:
- `OPENAI_API_KEY` - Required for API access
- `MODEL` - Transcription model (defaults to "gpt-4o-mini-transcribe")

## Common Commands

**Run transcription on MP4 file:**
```bash
python tranbob.py <video.mp4>
```

**Run transcription on WAV file (skip extraction):**
```bash
python tranbob.py <audio.wav> -w
```

**Install missing dependencies:**
```bash
pip install openai
```

## Important Notes

- The script expects ffmpeg to be installed and available in PATH for MP4 processing
- Output is saved as `<input_filename>_transcript.txt` in the same directory as input
- Temporary WAV files are automatically cleaned up after MP4 processing
- The `.env` file contains sensitive API credentials and should never be committed to version control
