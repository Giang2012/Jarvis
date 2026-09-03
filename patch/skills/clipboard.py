from skills.base_skill import BaseSkill


class ClipboardSkill(BaseSkill):
    def __init__(self, clipboard):
        super().__init__()
        self.name = "CLIPBOARD"
        self.clipboard = clipboard

    def execute(self, text):
        text = str(text or "")
        if text.lower().startswith("set:"):
            return self.clipboard.set(text.split(":", 1)[1])
        return self.clipboard.get()
