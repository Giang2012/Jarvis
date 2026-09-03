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
    def __init__(self, services):
        self.services = services
        self.registry = SkillRegistry()
        self.registry.register(OpenAppSkill(services.get("app")))
        self.registry.register(CloseAppSkill())
        self.registry.register(SearchSkill(services.get("browser")))
        self.registry.register(SystemSkill(services.get("system")))
        self.registry.register(CalculatorSkill())
        self.registry.register(WeatherSkill())
        if services.get("desktop"):
            self.registry.register(DesktopSkill(services.get("desktop")))
        if services.get("screen"):
            self.registry.register(VisionSkill(services.get("screen")))
        if services.get("files"):
            self.registry.register(FileSkill(services.get("files")))
        if services.get("media"):
            self.registry.register(MediaSkill(services.get("media")))
        if services.get("clipboard"):
            self.registry.register(ClipboardSkill(services.get("clipboard")))

    def execute(self, intent, text):
        if intent == "CHAT":
            return None
        if intent == "SCREENSHOT":
            skill = self.registry.find("DESKTOP")
            return skill.execute("screenshot") if skill else None
        if intent in {"OPEN_APP", "CLOSE_APP"}:
            skill = self.registry.find("DESKTOP")
            if not skill:
                return None
            prefix = "open_app:" if intent == "OPEN_APP" else "close_app:"
            return skill.execute(prefix + str(text))
        skill_name = {"VISION": "VISION", "FILES": "FILES", "MEDIA": "MEDIA", "CLIPBOARD": "CLIPBOARD"}.get(intent, intent)
        skill = self.registry.find(skill_name)
        if not skill:
            return None
        if intent == "FILES":
            return skill.execute("search:" + str(text))
        if intent == "MEDIA":
            return skill.execute(self._media_command(text))
        return skill.execute(text)

    @staticmethod
    def _media_command(text):
        lower = str(text).lower()
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
        return "play"
