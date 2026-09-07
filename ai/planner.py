from __future__ import annotations

from skills.registry import SkillRegistry
from skills.open_app import OpenAppSkill
from skills.close_app import CloseAppSkill
from skills.search import SearchSkill
from skills.weather import WeatherSkill
from skills.system import SystemSkill
from skills.calculator import CalculatorSkill
from skills.desktop import DesktopSkill
from skills.vision import VisionSkill
from skills.files import FileSkill
from skills.media import MediaSkill
from skills.clipboard import ClipboardSkill


class Planner:
    """
    Skill routing layer.

    Reasoner decides WHAT should happen.
    Planner decides WHICH skill handles it.
    Executor decides WHEN and HOW the tasks are run safely.
    """

    def __init__(self, services):
        self.services = services
        self.registry = SkillRegistry()

        self._register("OPEN_APP", OpenAppSkill(services.get("app")))
        self._register("CLOSE_APP", CloseAppSkill())
        self._register("SEARCH", SearchSkill(services.get("browser")))
        self._register("SYSTEM", SystemSkill(services.get("system")))
        self._register("CALCULATOR", CalculatorSkill())
        self._register("WEATHER", WeatherSkill())

        if services.get("desktop"):
            self._register("DESKTOP", DesktopSkill(services.get("desktop")))

        if services.get("screen"):
            self._register("VISION", VisionSkill(services.get("screen")))

        if services.get("files"):
            self._register("FILES", FileSkill(services.get("files")))

        if services.get("media"):
            self._register("MEDIA", MediaSkill(services.get("media")))

        if services.get("clipboard"):
            self._register("CLIPBOARD", ClipboardSkill(services.get("clipboard")))

    def _register(self, name, skill):
        if skill is not None:
            # Keep compatibility with skills whose own name differs from
            # the task action (e.g. OPEN_APP -> skill implementation).
            skill.name = name
            self.registry.register(skill)

    def execute(self, intent, text):
        action = str(intent or "").strip().upper()
        target = str(text or "").strip()

        if not action:
            return "Planner rejected an empty action."

        if action == "CHAT":
            return None

        if action == "SCREENSHOT":
            return self._execute_desktop("screenshot")

        if action in {"OPEN_APP", "CLOSE_APP"}:
            return self._execute_desktop(
                f"{'open_app' if action == 'OPEN_APP' else 'close_app'}:{target}"
            )

        if action == "FILES":
            return self._execute_skill("FILES", "search:" + target)

        if action == "MEDIA":
            return self._execute_skill("MEDIA", self._media_command(target))

        return self._execute_skill(action, target)

    def _execute_desktop(self, command):
        return self._execute_skill("DESKTOP", command)

    def _execute_skill(self, skill_name, command):
        skill = self.registry.find(skill_name)

        if not skill:
            return f"No skill registered for action: {skill_name}"

        try:
            result = skill.execute(command)
        except Exception as exc:
            raise RuntimeError(
                f"{skill_name} skill failed: {type(exc).__name__}: {exc}"
            ) from exc

        if result is None:
            return f"{skill_name} completed with no result."

        return result

    @staticmethod
    def _media_command(text):
        lower = str(text or "").lower()

        if "next" in lower or "tiếp" in lower:
            return "next"
        if "previous" in lower or "prev" in lower or "trước" in lower:
            return "previous"
        if "pause" in lower or "dừng" in lower:
            return "pause"
        if "volume up" in lower or "tăng âm" in lower:
            return "volume up"
        if "volume down" in lower or "giảm âm" in lower:
            return "volume down"
        if "mute" in lower or "tắt tiếng" in lower:
            return "mute"
        if "unmute" in lower or "bật tiếng" in lower:
            return "unmute"

        return "play"
