import re

from ai.plan import Plan
from ai.task import Task


class Reasoner:
    """Deterministic first-pass command planner.

    It deliberately keeps OS actions explicit so an LLM can be added later
    without allowing arbitrary shell text to become an executable command.
    """

    def build(self, text):
        raw = str(text or "").strip()
        lower = raw.lower()
        plan = Plan()

        parts = self._split_commands(lower)
        for part in parts:
            task = self._task_from_part(part)
            plan.add(task)

        return plan

    def _split_commands(self, text):
        # Split natural multi-step requests while preserving common phrases.
        separators = [
            r"\s+then\s+",
            r"\s+after that\s+",
            r"\s+sau đó\s+",
            r"\s+rồi\s+",
            r"\s+tiếp theo\s+",
        ]
        parts = [text]
        for pattern in separators:
            next_parts = []
            for part in parts:
                next_parts.extend(re.split(pattern, part))
            parts = next_parts
        return [p.strip() for p in parts if p.strip()]

    def _task_from_part(self, part):
        p = part.strip()
        if self._has(p, "vision", "screen", "màn hình", "nhìn"):
            return Task("VISION", p)

        if self._has(p, "open", "mở", "launch", "chạy", "khởi động"):
            target = self._after_command(
                p, ("open", "mở", "launch", "chạy", "khởi động")
            )
            return Task("OPEN_APP", target)

        if self._has(p, "close", "đóng", "tắt ứng dụng", "thoát ứng dụng"):
            target = self._after_command(
                p, ("close", "đóng", "tắt ứng dụng", "thoát ứng dụng")
            )
            return Task("CLOSE_APP", target)

        if self._has(p, "search", "tìm kiếm", "tìm", "google", "tra cứu"):
            target = self._after_command(
                p, ("search", "tìm kiếm", "tìm", "google", "tra cứu")
            )
            return Task("SEARCH", target)

        if self._has(p, "screenshot", "chụp màn hình"):
            return Task("SCREENSHOT", p)

        if self._has(p, "weather", "thời tiết"):
            return Task("WEATHER", p)

        if self._has(p, "calculate", "calculator", "tính toán", "tính"):
            return Task("CALCULATOR", p)

        if self._has(p, "play", "pause", "next track", "previous track",
                     "phát nhạc", "tạm dừng", "bài tiếp"):
            return Task("MEDIA", p)

        if self._has(p, "clipboard", "bộ nhớ tạm"):
            return Task("CLIPBOARD", p)

        if self._has(p, "file", "tệp", "thư mục", "folder"):
            return Task("FILES", p)

        if self._has(p, "shutdown", "tắt máy", "restart", "khởi động lại",
                     "lock", "khóa máy"):
            return Task("SYSTEM", p)

        return Task("CHAT", p)

    @staticmethod
    def _has(text, *words):
        return any(word in text for word in words)

    @staticmethod
    def _after_command(text, commands):
        lowered = text.lower()
        for command in commands:
            index = lowered.find(command)
            if index >= 0:
                target = text[index + len(command):].strip()
                target = re.sub(
                    r"^(ứng dụng|app|application)\s+",
                    "",
                    target,
                    flags=re.I,
                )
                return target or text
        return text
