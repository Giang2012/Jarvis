from skills.chat import ChatSkill
from skills.open_app import OpenAppSkill


class Planner:

    def __init__(self):
        self.chat = ChatSkill()
        self.open_app = OpenAppSkill()

    def execute(self, intent, text):

        if intent == "OPEN_APP":
            return self.open_app.run(text)

        return self.chat.run(text)