from gui.ai.core_state import CoreState
from gui.ai.emotion_engine import EmotionEngine


class AIBrain:

    def __init__(self):

        self.state = CoreState.IDLE

        self.emotion = EmotionEngine()

    # --------------------------

    def setState(self, state):

        self.state = state

        self.emotion.setState(state)

    # --------------------------

    def getState(self):

        return self.state

    # --------------------------

    def getColor(self):

        return self.emotion.color()