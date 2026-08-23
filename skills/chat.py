from skills.base_skill import BaseSkill


class ChatSkill(BaseSkill):

    name = "CHAT"

    def can_handle(self, text):
        return False

    def execute(self, text):
        return None