# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based audio/video transcription tool that uses OpenAI's Whisper API for transcription and GPT-4o-mini for speaker diarization (labeling different speakers in the transcript).

## Project Structure

```
transcribe/
├── input/          # Place audio/video files here (gitignored)
├── output/         # Transcripts are saved here (gitignored)
├── tranbob.py      # Main transcription script
├── .env            # API credentials (gitignored)
└── CLAUDE.md       # This file
```

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
python tranbob.py video.mp4
```

**Run transcription on WAV file (skip extraction):**
```bash
python tranbob.py audio.wav -w
```

**Install missing dependencies:**
```bash
pip install openai
```

## Important Notes

- All input files must be placed in the `input/` folder
- The script expects only the filename as argument, not the full path
- Output transcripts are saved to `output/` folder as `<filename>_transcript.txt`
- The script expects ffmpeg to be installed and available in PATH for MP4 processing
- Temporary WAV files are created in the `input/` folder and automatically cleaned up after processing
- The `.env` file contains sensitive API credentials and should never be committed to version control
- Both `input/` and `output/` folders are gitignored to prevent committing media files and transcripts
