import speech_recognition as sr


class Recognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize(self, audio):
        if audio is None:
            print("[JARVIS STT] No audio.")
            return ""

        try:
            text = self.recognizer.recognize_google(
                audio,
                language="vi-VN",
            )

            text = text.strip()

            if text:
                print(f"[JARVIS STT] Recognized: {text}")
            else:
                print("[JARVIS STT] Google returned empty text.")

            return text

        except sr.UnknownValueError:
            print(
                "[JARVIS STT] Không nhận diện được lời nói."
            )
            return ""

        except sr.RequestError as exc:
            print(
                f"[JARVIS STT] Google Speech API error: {exc}"
            )
            return ""

        except Exception as exc:
            print(
                f"[JARVIS STT] Unexpected error: "
                f"{type(exc).__name__}: {exc}"
            )
            return ""