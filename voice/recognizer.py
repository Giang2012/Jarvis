import speech_recognition as sr


class Recognizer:

    def __init__(self):

        self.recognizer = sr.Recognizer()

    def recognize(self, audio):

        try:

            return self.recognizer.recognize_google(

                audio,

                language="vi-VN"

            )

        except Exception:

            return ""