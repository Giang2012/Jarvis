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
    """Only exposes tools that are actually backed by JARVIS services."""

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
        return tuple(x for x in self._items.values() if any(q in field.lower() for field in (x.title, x.subtitle, x.description, x.category)))

    def _load_defaults(self):
        tools = [
            ("ai_chat", "AI CHAT", "Talk with JARVIS", "AI", "AI", "Send a request through the JARVIS brain."),
            ("screen_vision", "SCREEN VISION", "Understand the screen", "AI", "◉", "Inspect the current screen locally with screenshot/OCR/vision."),
            ("search", "SEARCH", "Web intelligence", "WEB", "⌕", "Search the web through the browser service."),
            ("weather", "WEATHER", "Forecast lookup", "WEB", "☼", "Query weather information."),
            ("open_app", "OPEN APP", "Launch a safe app", "DESKTOP", "▦", "Launch an application from the safe launcher catalog."),
            ("screenshot", "SCREENSHOT", "Capture the screen", "DESKTOP", "▣", "Save a local screenshot."),
            ("clipboard", "CLIPBOARD", "Read / write clipboard", "DESKTOP", "▤", "Inspect or update the local clipboard."),
            ("system", "SYSTEM STATUS", "Health & telemetry", "SYSTEM", "⌁", "Inspect CPU, RAM, uptime and platform status."),
            ("media", "MEDIA", "Playback controls", "MEDIA", "♫", "Play, pause, next, previous, volume and mute."),
            ("files", "FILES", "Find local files", "FILES", "▱", "Search local filenames and open safe paths."),
            ("calculator", "CALCULATOR", "Fast calculations", "AI", "∑", "Calculate expressions through JARVIS."),
            ("screen_awareness", "SCREEN AWARENESS", "Opt-in local observer", "AI", "◎", "Enable or disable periodic local screen observation."),
        ]
        for row in tools:
            self.register(ToolDefinition(*row))
