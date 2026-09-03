from skills.base_skill import BaseSkill


class DesktopSkill(BaseSkill):
    def __init__(self, desktop):
        super().__init__()
        self.name = "DESKTOP"
        self.desktop = desktop

    def execute(self, text):
        text = str(text or "").strip()
        lower = text.lower()

        if lower.startswith("open_app:"):
            return self.desktop.open_app(text.split(":", 1)[1].strip())
        if lower.startswith("close_app:"):
            return self.desktop.close_app(text.split(":", 1)[1].strip())
        if lower.startswith("type:"):
            return self.desktop.type_text(text.split(":", 1)[1])
        if lower.startswith("press:"):
            return self.desktop.press(text.split(":", 1)[1])
        if lower.startswith("hotkey:"):
            return self.desktop.hotkey(text.split(":", 1)[1])

        return "Desktop command not recognized."
