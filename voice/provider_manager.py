import os

from .providers.elevenlabs import ElevenLabsTTS
from .providers.windows_tts import WindowsTTS


DEFAULT_VOICES = {
    "voice_1": "hNe03uL2BbiU3txTclei.",
    "voice_2": "ev2kMR9ZJZZsemuogS5u.",
}


class VoiceProviderManager:
    def __init__(self):
        self.provider_name = os.getenv(
            "JARVIS_TTS_PROVIDER",
            "windows"
        ).strip().lower()

        self.voice_id = os.getenv(
            "JARVIS_VOICE_ID",
            DEFAULT_VOICES["voice_1"]
        ).strip()

        self.model_id = os.getenv(
            "ELEVENLABS_MODEL_ID",
            "eleven_multilingual_v2"
        ).strip()

        self.provider = None

    def _build(self):
        if self.provider_name == "windows":
            return WindowsTTS()

        if self.provider_name == "elevenlabs":
            return ElevenLabsTTS(
                self.voice_id,
                self.model_id
            )

        raise ValueError(
            f"Unsupported TTS provider: {self.provider_name}"
        )

    def _ensure_provider(self):
        if self.provider is None:
            self.provider = self._build()

        return self.provider

    def speak(self, text):
        return self._ensure_provider().speak(text)

    def stop(self):
        if self.provider is not None:
            try:
                self.provider.stop()
            except Exception:
                pass