from enum import Enum


class Emotion(Enum):

    CALM = 0

    THINKING = 1

    LISTENING = 2

    SPEAKING = 3

    ERROR = 4


class EmotionEngine:

    def __init__(self):

        self.state = Emotion.CALM

    # ----------------------

    def setState(self, state):

        self.state = state

    # ----------------------

    def color(self):

        if self.state == Emotion.CALM:

            return (0, 255, 255)

        if self.state == Emotion.THINKING:

            return (150, 0, 255)

        if self.state == Emotion.LISTENING:

            return (255, 255, 0)

        if self.state == Emotion.SPEAKING:

            return (255, 255, 255)

        return (255, 0, 0)