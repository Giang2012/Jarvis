import pyttsx3


class WindowsTTS:
    def __init__(self, voice_name=None, rate=0):
        self.voice_name = voice_name
        self.rate = rate
        self.engine = None

    def _ensure_engine(self):
        if self.engine is not None:
            return self.engine

        self.engine = pyttsx3.init("sapi5")

        self.engine.setProperty("rate", self.rate or 170)
        self.engine.setProperty("volume", 1.0)

        if self.voice_name:
            for voice in self.engine.getProperty("voices"):
                if self.voice_name.lower() in voice.name.lower():
                    self.engine.setProperty("voice", voice.id)
                    break

        return self.engine

    def speak(self, text):
        text = str(text).strip()

        if not text:
            return None

        engine = self._ensure_engine()

        engine.say(text)
        engine.runAndWait()

        return True

    def stop(self):
        if self.engine is not None:
            try:
                self.engine.stop()
            except Exception:
                pass