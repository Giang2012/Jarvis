from dataclasses import dataclass

@dataclass(frozen=True)
class ToolDefinition:
    key: str
    title: str
    subtitle: str
    category: str
    glyph: str
    description: str

class ToolRegistry:
    categories = ("AI", "WEB", "DESKTOP", "SYSTEM", "MEDIA", "FILES")

    def __init__(self):
        self._items = {}
        self._load_defaults()

    def register(self, tool):
        self._items[tool.key] = tool

    def get(self, key):
        return self._items.get(key)

    def all(self):
        return tuple(self._items.values())

    def category(self, name):
        return tuple(x for x in self._items.values() if x.category == name)

    def search(self, text):
        q = (text or "").strip().lower()
        if not q:
            return self.all()
        return tuple(
            x for x in self._items.values()
            if any(q in field.lower() for field in
                   (x.title, x.subtitle, x.description, x.category, x.key))
        )

    def _load_defaults(self):
        rows = [
            ("ai_chat", "AI CHAT", "Talk with Ollama", "AI", "AI",
             "Chat with the local Ollama model."),
            ("calculator", "CALCULATOR", "Fast calculations", "AI", "∑",
             "Calculate a simple expression."),
            ("system", "SYSTEM STATUS", "Local telemetry", "SYSTEM", "⌁",
             "Show local CPU/RAM/platform information."),
            ("screenshot", "SCREENSHOT", "Capture the screen", "DESKTOP", "▣",
             "Capture the current desktop."),
            ("open_app", "OPEN APP", "Launch a safe app", "DESKTOP", "▦",
             "Launch a common desktop application."),
            ("search", "SEARCH", "Web search", "WEB", "⌕",
             "Open a web search in the default browser."),
        ]
        for row in rows:
            self.register(ToolDefinition(*row))
