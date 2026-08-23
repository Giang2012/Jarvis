class StateEngine:

    READY = "READY"

    LISTENING = "LISTENING"

    THINKING = "THINKING"

    EXECUTING = "EXECUTING"

    SPEAKING = "SPEAKING"

    ERROR = "ERROR"

    SLEEP = "SLEEP"

    def __init__(self):

        self.current = StateEngine.READY

    def set(self, state):

        self.current = state

    def get(self):

        return self.current