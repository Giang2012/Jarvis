from ai.intent import IntentRecognizer
from ai.planner import Planner


class Brain:
    def __init__(self):
        self.intent = IntentRecognizer()
        self.planner = Planner()

    def process(self, text):
        intent = self.intent.detect(text)
        result = self.planner.execute(intent, text)
        return result