import io
import os
import tempfile
import threading
import time
import wave
from pathlib import Path

import requests

try:
    import sounddevice as sd
except ImportError:
    sd = None


class VoiceService:
    """
    ElevenLabs voice layer for JARVIS.

    Flow:
        microphone -> local WAV -> ElevenLabs STT -> text
        text -> JARVIS Brain -> reply
        reply -> ElevenLabs TTS -> PCM -> speakers

    The service is intentionally explicit: listening starts only when
    start_listening() is called.
    """

    API_BASE = "https://api.elevenlabs.io/v1"

    def __init__(
        self,
        api_key=None,
        voice_id=None,
        tts_model="eleven_multilingual_v2",
        stt_model="scribe_v2",
        sample_rate=48000,
        channels=1,
        record_seconds=6,
    ):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY", "")
        self.voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID", "")
        self.tts_model = os.getenv("ELEVENLABS_TTS_MODEL", tts_model)
        self.stt_model = os.getenv("ELEVENLABS_STT_MODEL", stt_model)
        self.sample_rate = int(os.getenv("JARVIS_VOICE_SAMPLE_RATE", sample_rate))
        self.channels = int(os.getenv("JARVIS_VOICE_CHANNELS", channels))
        self.record_seconds = float(
            os.getenv("JARVIS_VOICE_RECORD_SECONDS", record_seconds)
        )
        self._stop_event = threading.Event()

    def _headers(self):
        if not self.api_key:
            raise RuntimeError(
                "Missing ELEVENLABS_API_KEY. Set it in the current PowerShell session."
            )
        return {"xi-api-key": self.api_key}

    def is_configured(self):
        return bool(self.api_key and self.voice_id)

    def record_wav(self, seconds=None):
        if sd is None:
            raise RuntimeError(
                "sounddevice is not installed. Run: pip install sounddevice"
            )

        seconds = float(seconds or self.record_seconds)
        frames = int(seconds * self.sample_rate)

        audio = sd.rec(
            frames,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="int16",
            device=20,
        )
        sd.wait()

        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio.tobytes())

        return buffer.getvalue()

    def transcribe_wav(self, wav_bytes):
        files = {
            "file": ("jarvis_mic.wav", wav_bytes, "audio/wav"),
        }
        data = {
            "model_id": self.stt_model,
            "language_code": "vi",
        }

        response = requests.post(
            f"{self.API_BASE}/speech-to-text",
            headers=self._headers(),
            files=files,
            data=data,
            timeout=90,
        )
        response.raise_for_status()
        payload = response.json()
        return (payload.get("text") or "").strip()

    def listen_once(self, seconds=None):
        wav = self.record_wav(seconds)
        return self.transcribe_wav(wav)

    def synthesize_pcm(self, text):
        text = (text or "").strip()
        if not text:
            return b""

        response = requests.post(
            f"{self.API_BASE}/text-to-speech/{self.voice_id}",
            params={"output_format": "pcm_44100"},
            headers={
                **self._headers(),
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "model_id": self.tts_model,
            },
            timeout=90,
        )
        response.raise_for_status()
        return response.content

    def speak(self, text):
        if sd is None:
            raise RuntimeError(
                "sounddevice is not installed. Run: pip install sounddevice"
            )

        pcm = self.synthesize_pcm(text)
        if not pcm:
            return

        # pcm_44100 from ElevenLabs is signed 16-bit mono PCM.
        audio = memoryview(pcm).cast("h")
        sd.play(audio, samplerate=44100, blocking=True)

    def stop(self):
        self._stop_event.set()
        if sd is not None:
            try:
                sd.stop()
            except Exception:
                pass

    def reset_stop(self):
        self._stop_event.clear()

    def run_voice_turn(self, brain, seconds=None):
        """
        One complete voice turn.

        Returns:
            {
                "text": user_text,
                "reply": assistant_reply,
            }
        """
        user_text = self.listen_once(seconds)
        if not user_text:
            return {"text": "", "reply": ""}

        result = brain.process(user_text)

        if isinstance(result, dict):
            reply = (
                result.get("response")
                or result.get("reply")
                or result.get("message")
                or ""
            )
        else:
            reply = str(result)

        reply = reply.strip()

        if reply:
            self.speak(reply)

        return {"text": user_text, "reply": reply}
