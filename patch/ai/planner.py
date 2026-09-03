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

        self.registry.register(OpenAppSkill(self.services.get("app")))
        self.registry.register(CloseAppSkill())
        self.registry.register(SearchSkill(self.services.get("browser")))
        self.registry.register(SystemSkill(self.services.get("system")))
        self.registry.register(CalculatorSkill())
        self.registry.register(WeatherSkill())

        desktop = self.services.get("desktop")
        screen = self.services.get("screen")
        files = self.services.get("files")
        media = self.services.get("media")
        clipboard = self.services.get("clipboard")

        if desktop:
            self.registry.register(DesktopSkill(desktop))
        if screen:
            self.registry.register(VisionSkill(screen))
        if files:
            self.registry.register(FileSkill(files))
        if media:
            self.registry.register(MediaSkill(media))
        if clipboard:
            self.registry.register(ClipboardSkill(clipboard))

    def execute(self, intent, text):
        if intent == "CHAT":
            return None

        # Map rich actions to the actual skill implementation.
        mapping = {
            "OPEN_APP": "OPEN_APP",
            "CLOSE_APP": "CLOSE_APP",
            "SEARCH": "SEARCH",
            "SYSTEM": "SYSTEM",
            "CALCULATOR": "CALCULATOR",
            "WEATHER": "WEATHER",
            "VISION": "VISION",
            "FILES": "FILES",
            "MEDIA": "MEDIA",
            "CLIPBOARD": "CLIPBOARD",
            "SCREENSHOT": "DESKTOP",
        }
        skill_name = mapping.get(intent, intent)
        skill = self.registry.find(skill_name)

        if skill is None:
            return None

        if intent == "SCREENSHOT":
            return skill.execute("screenshot")

        if intent in {"OPEN_APP", "CLOSE_APP"}:
            prefix = "open_app:" if intent == "OPEN_APP" else "close_app:"
            return self.registry.find("DESKTOP").execute(prefix + text)

        if intent == "VISION":
            return skill.execute(text)

        if intent == "FILES":
            return skill.execute("search:" + text)

        if intent == "MEDIA":
            command = self._media_command(text)
            return skill.execute(command)

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
