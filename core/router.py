from core.skill_manager import SkillManager


class Router:

    def __init__(self):

        self.manager = SkillManager()

    def execute(self, command):

        skill = self.manager.get(
            command.intent.value
        )

        if skill is None:

            return None

        return skill.run(command)