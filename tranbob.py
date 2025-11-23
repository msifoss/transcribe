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
        print("Usage: python tranbob.py <file> [-w]")
        print("Default is MP4, use -w if input is already WAV")
        sys.exit(1)

    input_file = sys.argv[1]
    is_wav = "-w" in sys.argv

    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    if is_wav:
        wav_file = input_file
    else:
        base_name = os.path.splitext(input_file)[0]
        wav_file = f"{base_name}_temp.wav"
        extract_audio_from_mp4(input_file, wav_file)

    # Run transcription with speaker labeling
    labeled_transcript = transcribe_and_label(wav_file)

    # Save transcript
    output_file = os.path.splitext(input_file)[0] + "_transcript.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(labeled_transcript)

    print(f"✅ Transcript saved to {output_file}")

    # Cleanup temp WAV if created
    if not is_wav and os.path.exists(wav_file):
        os.remove(wav_file)
        print("🧹 Temp file removed")
