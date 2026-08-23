class SkillRegistry:

    def __init__(self):

        self.skills = {}

    def register(self, skill):

        self.skills[skill.name.upper()] = skill

    def find(self, intent):

        if not intent:
            return None

        return self.skills.get(intent.upper())

    def all(self):

        return list(self.skills.values())

    def clear(self):

        self.skills.clear()