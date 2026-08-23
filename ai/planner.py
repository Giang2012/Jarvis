from skills.registry import SkillRegistry

from skills.open_app import OpenAppSkill
from skills.close_app import CloseAppSkill
from skills.search import SearchSkill
from skills.weather import WeatherSkill
from skills.system import SystemSkill
from skills.calculator import CalculatorSkill


class Planner:

    def __init__(self, services):

        self.services = services

        self.registry = SkillRegistry()

        # =========================
        # APPLICATION
        # =========================

        self.registry.register(
            OpenAppSkill(
                self.services.get("app")
            )
        )

        self.registry.register(
            CloseAppSkill()
        )

        # =========================
        # WEB
        # =========================

        self.registry.register(
            SearchSkill(
                self.services.get("browser")
            )
        )

        # =========================
        # SYSTEM
        # =========================

        self.registry.register(
            SystemSkill(
                self.services.get("system")
            )
        )

        # =========================
        # TOOLS
        # =========================

        self.registry.register(
            CalculatorSkill()
        )

        self.registry.register(
            WeatherSkill()
        )

    # =========================
    # EXECUTE
    # =========================

    def execute(self, intent, text):

        # CHAT → Ollama fallback
        if intent == "CHAT":

            return None

        # =========================
        # SYSTEM
        # =========================

        if intent == "SYSTEM":

            skill = self.registry.find(
                "SYSTEM"
            )

            if skill is None:
                return None

            return skill.execute(text)

        # =========================
        # NORMAL SKILL
        # =========================

        skill = self.registry.find(
            intent
        )

        if skill is None:
            return None

        return skill.execute(text)