import threading

from .microphone import Microphone
from .recognizer import Recognizer
from .wake_word import WakeWord
from .provider_manager import VoiceProviderManager


class VoiceEngine:
    def __init__(self, brain):
        self.brain = brain

        self.microphone = Microphone()
        self.recognizer = Recognizer()
        self.wake_word = WakeWord()
        self.tts = VoiceProviderManager()

        self._stop = threading.Event()
        self._started = False

    def run(self):
        if self._started:
            return

        self._started = True
        self._stop.clear()

        print("[JARVIS voice] Voice Engine running.")

        try:
            while not self._stop.is_set():
                try:
                    # --------------------------------------------------
                    # 1. MICROPHONE
                    # --------------------------------------------------
                    audio = self.microphone.listen()

                    if audio is None:
                        continue

                    # --------------------------------------------------
                    # 2. STT
                    # --------------------------------------------------
                    text = self.recognizer.recognize(audio)

                    if not text:
                        continue

                    print(
                        f"[JARVIS voice] Heard: {text}"
                    )

                    # --------------------------------------------------
                    # 3. WAKE WORD
                    # --------------------------------------------------
                    command = self.wake_word.extract_command(text)

                    if command is None:
                        print(
                            "[JARVIS voice] "
                            "Wake word not detected."
                        )
                        continue

                    print(
                        f"[JARVIS voice] Command: {command}"
                    )

                    # --------------------------------------------------
                    # 4. BRAIN
                    # --------------------------------------------------
                    print(
                        "[JARVIS voice] "
                        "Sending command to Brain..."
                    )

                    reply = self.brain.process(command)

                    print(
                        f"[JARVIS voice] Brain reply: "
                        f"{reply!r}"
                    )

                    # --------------------------------------------------
                    # 5. TTS
                    # --------------------------------------------------
                    if reply:
                        print(
                            "[JARVIS voice] "
                            "Speaking reply..."
                        )

                        self.speak(str(reply))

                        print(
                            "[JARVIS voice] "
                            "TTS finished."
                        )
                    else:
                        print(
                            "[JARVIS voice] "
                            "Brain returned empty reply."
                        )

                except Exception as exc:
                    print(
                        "[JARVIS voice] "
                        f"Loop error: "
                        f"{type(exc).__name__}: {exc}"
                    )

        finally:
            self._started = False

            print(
                "[JARVIS voice] Voice Engine stopped."
            )

    def speak(self, text):
        if not text:
            return None

        print(
            f"[JARVIS TTS] Text: {text}"
        )

        result = self.tts.speak(str(text))

        print(
            f"[JARVIS TTS] Result: {result!r}"
        )

        return result

    def stop(self):
        self._stop.set()

        try:
            self.microphone.close()
        except Exception:
            pass

        try:
            self.tts.stop()
        except Exception:
            pass