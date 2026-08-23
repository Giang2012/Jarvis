import speech_recognition as sr


class Microphone:

    def __init__(self):

        self.recognizer = sr.Recognizer()

        self.microphone = sr.Microphone()

    def listen(self):

        with self.microphone as source:

            self.recognizer.adjust_for_ambient_noise(source)

            audio = self.recognizer.listen(source)

        return audio