from dataclasses import dataclass
from typing import Callable, Optional


@dataclass(frozen=True)
class ToolDefinition:
    key: str
    title: str
    subtitle: str
    category: str
    glyph: str
    description: str
    action: Optional[Callable] = None


class ToolRegistry:
    """Single source of truth for the Tool Space catalog."""

    CATEGORIES = (
        "PRODUCTIVITY",
        "DEVELOPMENT",
        "SYSTEM",
        "MEDIA",
        "INFORMATION",
        "AI",
    )

    def __init__(self):
        self._tools = {}
        self._register_defaults()

    def register(self, tool: ToolDefinition):
        self._tools[tool.key] = tool

    def get(self, key: str):
        return self._tools.get(key)

    def all(self):
        return tuple(self._tools.values())

    def by_category(self, category: str):
        return tuple(
            tool for tool in self._tools.values()
            if tool.category == category
        )

    def _register_defaults(self):
        definitions = [
            ("ai_chat", "AI CHAT", "Talk with JARVIS", "AI", "AI",
             "Open the conversational AI workspace."),
            ("search", "SEARCH", "Web intelligence", "INFORMATION", "⌕",
             "Search the web and inspect results."),
            ("weather", "WEATHER", "Live conditions", "INFORMATION", "☼",
             "Show live weather without a command prompt."),
            ("calculator", "CALCULATOR", "Quick calculations", "PRODUCTIVITY", "∑",
             "Calculate expressions and common conversions."),
            ("open_app", "OPEN APP", "Launch applications", "SYSTEM", "▦",
             "Browse and launch installed applications."),
            ("system", "SYSTEM", "System control", "SYSTEM", "⌁",
             "Inspect system state and available controls."),
            ("music", "MUSIC", "Media control", "MEDIA", "♫",
             "Control local media playback."),
            ("notifications", "NOTIFICATIONS", "Notification center", "PRODUCTIVITY", "♧",
             "Review and manage notifications."),
            ("notes", "NOTES", "Quick notes", "PRODUCTIVITY", "▤",
             "Create and organize quick notes."),
            ("calendar", "CALENDAR", "Schedule", "PRODUCTIVITY", "□",
             "View events and schedule."),
            ("terminal", "TERMINAL", "Developer console", "DEVELOPMENT", ">_",
             "Open a controlled developer terminal."),
            ("code_runner", "CODE RUNNER", "Execute snippets", "DEVELOPMENT", "</>",
             "Run supported code snippets."),
            ("files", "FILES", "File browser", "SYSTEM", "▱",
             "Browse project and user files."),
            ("screenshot", "SCREENSHOT", "Capture screen", "SYSTEM", "▣",
             "Capture the current screen."),
            ("voice", "VOICE INPUT", "Speech control", "AI", "♩",
             "Open voice input controls."),
            ("translate", "TRANSLATE", "Language utility", "INFORMATION", "文",
             "Translate selected text."),
            ("memory", "MEMORY", "JARVIS memory", "AI", "◇",
             "Inspect memory and conversation context."),
        ]

        for key, title, subtitle, category, glyph, description in definitions:
            self.register(
                ToolDefinition(
                    key=key,
                    title=title,
                    subtitle=subtitle,
                    category=category,
                    glyph=glyph,
                    description=description,
                )
            )
