# src/services/audio_service.py
import os
from faster_whisper import WhisperModel

print("Loading local Faster-Whisper model into memory...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
print("Local Faster-Whisper model ready!")

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes audio files locally using faster-whisper with VAD filtering.
    """
    if not audio_path or not os.path.exists(audio_path):
        return ""

    try:
        # Enable Voice Activity Detection (vad_filter=True) to ignore static hiss
        segments, info = whisper_model.transcribe(
            audio_path,
            beam_size=5,
            vad_filter=True,  # Ignores pure background noise
            vad_parameters=dict(min_silence_duration_ms=500),
            initial_prompt="Patient health consultation describing symptoms, pain, fever, duration, and medical history."
        )

        transcribed_text = " ".join([segment.text for segment in segments]).strip()

        # Debug print in terminal to see raw result
        print(f"[Audio Transcription Debug]: '{transcribed_text}'")

        if not transcribed_text or transcribed_text in [".", "...", "Thank you.", "Bye.", "Subtitles by Amara.org"]:
            return "⚠️ No clear voice detected. Please check your browser microphone settings and speak louder."

        return transcribed_text

    except Exception as e:
        return f"❌ Local Audio Transcription Error: {str(e)}"