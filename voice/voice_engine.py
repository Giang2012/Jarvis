from voice.microphone import Microphone
from voice.recognizer import Recognizer
from voice.tts import TTS
from voice.wake_word import WakeWord


class VoiceEngine:

    def __init__(self, brain):

        self.brain = brain

        self.microphone = Microphone()

        self.recognizer = Recognizer()

        self.tts = TTS()

        self.wake = WakeWord()

    def run(self):

        while True:

            audio = self.microphone.listen()

            text = self.recognizer.recognize(audio)

            if not text:

                continue

            print(text)

            if not self.wake.detect(text):

                continue

            command = text.lower()

            command = command.replace(

                "hey jarvis",

                ""

            )

            command = command.replace(

                "jarvis",

                ""

            )

            command = command.strip()

            if not command:

                self.tts.speak("Tôi đây.")

                continue

            reply = self.brain.process(command)

            self.tts.speak(reply)