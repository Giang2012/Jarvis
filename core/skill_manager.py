import importlib
import pkgutil

import skills


class SkillManager:

    def __init__(self):

        self.skills = {}

        self.load()

    def load(self):

        self.skills.clear()

        for _, module_name, _ in pkgutil.iter_modules(
            skills.__path__
        ):

            module = importlib.import_module(
                f"skills.{module_name}"
            )

            if hasattr(module, "Skill"):

                obj = module.Skill()

                self.skills[obj.name] = obj

    def get(self, name):

        return self.skills.get(name)