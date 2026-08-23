class ShortMemory:

    def __init__(self):

        self.messages = []

    def add(self, role, text):

        self.messages.append({

            "role": role,

            "text": text

        })

        if len(self.messages) > 30:

            self.messages.pop(0)

    def history(self):

        return self.messages