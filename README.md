# Tranbob - Audio/Video Transcription Tool

A Python-based transcription tool that uses OpenAI's Whisper API for speech-to-text conversion with automatic speaker labeling. Includes optional post-processing with custom AI instructions.

## Features

- **Multi-format support**: Transcribe MP3, WAV, M4A, WEBM, and MP4 files
- **Automatic speaker labeling**: Identifies and labels different speakers in the transcript
- **Custom post-processing**: Process transcripts with custom AI instructions using `--tink`
- **Simple workflow**: Drop files in `input/`, get transcripts in `output/`

## Requirements

- Python 3.7+
- OpenAI API key
- ffmpeg (only required for MP4 video files)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/msifoss/transcribe.git
   cd transcribe
   ```

2. Install dependencies:
   ```bash
   pip install openai python-dotenv
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   MODEL=whisper-1
   ```

4. (Optional) Install ffmpeg for MP4 support:
   - **Windows**: `winget install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

## Usage

### Basic Transcription

Place your audio/video file in the `input/` folder, then run:

```bash
python tranbob.py recording.mp3
```

The transcript will be saved to `output/recording_transcript.txt`

### Supported Formats

| Format | Type | Notes |
|--------|------|-------|
| `.mp3` | Audio | Direct upload to Whisper API |
| `.wav` | Audio | Direct upload to Whisper API |
| `.m4a` | Audio | Direct upload to Whisper API |
| `.webm` | Audio | Direct upload to Whisper API |
| `.mpga` | Audio | Direct upload to Whisper API |
| `.mpeg` | Audio | Direct upload to Whisper API |
| `.mp4` | Video | Requires ffmpeg for audio extraction |

### Post-Processing with Tink

Use the `--tink` flag to process transcripts with custom AI instructions:

```bash
python tranbob.py meeting.mp3 --tink instructions.md
```

This creates two output files:
- `output/meeting_transcript.txt` - The speaker-labeled transcript
- `output/meeting_transcript-tink.txt` - The processed result

### Creating Instruction Files

Instruction files are markdown files containing a system prompt for the AI. The entire file content is sent as instructions.

See `sample_instructions.md` for an example, or create your own:

```markdown
# Meeting Summary Instructions

Analyze this transcript and provide:

1. **Executive Summary** - 2-3 sentence overview
2. **Key Decisions** - Bullet list of decisions made
3. **Action Items** - Tasks with owners if mentioned
4. **Next Steps** - What happens next

Keep the summary concise and actionable.
```

## Project Structure

```
transcribe/
├── input/                  # Place audio/video files here
├── output/                 # Transcripts are saved here
├── tranbob.py              # Main transcription script
├── sample_instructions.md  # Example tink instruction file
├── .env                    # API credentials (create this)
└── README.md
```

## Configuration

Environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `MODEL` | Whisper model to use | `whisper-1` |

### Model Options

- `whisper-1` - Standard Whisper model, recommended for most use cases
- `gpt-4o-mini-transcribe` - Newer model, may have output length limits

## Limitations

- Maximum file size: 25MB (OpenAI API limit)
- For larger files, consider splitting the audio before transcription
- Speaker labeling is AI-generated and may not be 100% accurate

## License

MIT
