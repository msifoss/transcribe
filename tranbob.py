import os
import sys
import subprocess
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL", "gpt-4o-mini-transcribe")

if not api_key:
    print("❌ OPENAI_API_KEY missing from .env")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Define folder paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Ensure directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_audio_from_mp4(mp4_path, wav_path):
    """Extracts audio from MP4 and saves as WAV (16kHz mono)"""
    print(f"🎥 Extracting audio from {mp4_path} ...")
    cmd = [
        "ffmpeg", "-i", mp4_path,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        wav_path, "-y"
    ]
    subprocess.run(cmd, check=True)
    print(f"🎵 Audio extracted to {wav_path}")

def transcribe_and_label(audio_path):
    # Step 1: Transcribe the audio
    print(f"🎙 Transcribing {audio_path} ...")
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=model,
            file=audio_file
        )

    raw_text = transcript.text.strip()

    # Step 2: Add speaker labels
    print("🗣 Adding speaker labels...")
    speaker_labeled = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a transcription editor. "
                    "Identify changes in who is speaking and label them as "
                    "'Speaker 1:', 'Speaker 2:', etc. "
                    "Keep the text accurate and in the original order."
                )
            },
            {"role": "user", "content": raw_text}
        ]
    )

    return speaker_labeled.choices[0].message.content.strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tranbob.py <filename> [-w]")
        print("Place input files in the 'input/' folder")
        print("Use -w flag if input is already WAV, otherwise assumes MP4")
        sys.exit(1)

    filename = sys.argv[1]
    is_wav = "-w" in sys.argv

    # Construct full input path
    input_file = os.path.join(INPUT_DIR, filename)

    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        print(f"💡 Make sure the file is in the '{INPUT_DIR}/' folder")
        sys.exit(1)

    if is_wav:
        wav_file = input_file
    else:
        base_name = os.path.splitext(filename)[0]
        wav_file = os.path.join(INPUT_DIR, f"{base_name}_temp.wav")
        extract_audio_from_mp4(input_file, wav_file)

    # Run transcription with speaker labeling
    labeled_transcript = transcribe_and_label(wav_file)

    # Save transcript to output folder
    base_name = os.path.splitext(filename)[0]
    output_file = os.path.join(OUTPUT_DIR, f"{base_name}_transcript.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(labeled_transcript)

    print(f"✅ Transcript saved to {output_file}")

    # Cleanup temp WAV if created
    if not is_wav and os.path.exists(wav_file):
        os.remove(wav_file)
        print("🧹 Temp file removed")
