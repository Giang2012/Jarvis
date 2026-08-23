class ActionManager:

    def __init__(self):

        self.actions = {}

    # -----------------------

    def register(self, name, callback):

        self.actions[name] = callback

    # -----------------------

    def execute(self, action):

        if action.name in self.actions:

            self.actions[action.name](action.data)