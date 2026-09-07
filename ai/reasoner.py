from __future__ import annotations

import re

from ai.plan import Plan
from ai.task import Task


class Reasoner:
    """
    Deterministic command-to-plan reasoning layer.

    Converts natural-language commands into an ordered Plan while keeping
    execution itself inside Planner/Executor.
    """

    _SEPARATORS = (
        r"\s+sau\s+đó\s+",
        r"\s+sau\s+do\s+",
        r"\s+rồi\s+",
        r"\s+tiếp\s+theo\s+",
        r"\s+then\s+",
        r"\s+after\s+that\s+",
        r"\s+and\s+then\s+",
    )

    _OPEN_WORDS = ("open", "mở", "launch", "chạy", "khởi động")
    _CLOSE_WORDS = ("close", "đóng", "tắt ứng dụng", "thoát ứng dụng", "close app", "exit app")
    _SEARCH_WORDS = ("search for", "search", "tìm kiếm", "tìm", "google", "tra cứu", "hãy tìm")
    _WEATHER_WORDS = ("weather", "thời tiết", "dự báo thời tiết", "nhiệt độ", "dự báo")
    _CALC_WORDS = ("calculate", "calculator", "calculate", "tính toán", "tính")
    _MEDIA_WORDS = (
        "play", "pause", "next track", "previous track", "next song",
        "previous song", "phát nhạc", "tạm dừng", "bài tiếp", "bài trước",
        "tăng âm lượng", "giảm âm lượng", "tắt tiếng", "bật tiếng",
        "mute", "unmute", "volume up", "volume down",
    )
    _CLIPBOARD_WORDS = ("clipboard", "bộ nhớ tạm", "copy", "paste", "sao chép", "dán")
    _FILE_WORDS = ("file", "files", "tệp", "tệp tin", "thư mục", "folder", "folders")
    _SYSTEM_WORDS = (
        "shutdown", "shut down", "tắt máy", "restart",
        "khởi động lại", "reboot", "lock", "khóa máy",
    )
    _VISION_WORDS = (
        "nhìn màn hình", "xem màn hình", "quan sát màn hình",
        "màn hình đang", "trên màn hình", "đang làm gì",
        "tôi đang làm gì", "what do you see", "what's on my screen",
        "what is on my screen", "vision",
    )
    _SCREENSHOT_WORDS = (
        "screenshot", "screen shot", "chụp màn hình",
        "chụp lại màn hình", "capture screen",
    )

    def build(self, text) -> Plan:
        raw = self._normalize(text)
        plan = Plan()

        if not raw:
            return plan

        for part in self._split_commands(raw):
            task = self._task_from_part(part)
            plan.add(task)

        return plan

    @staticmethod
    def _normalize(text) -> str:
        value = str(text or "").strip().lower()
        value = re.sub(r"\s+", " ", value)
        return value

    def _split_commands(self, text: str) -> list[str]:
        parts = [text]

        for pattern in self._SEPARATORS:
            next_parts = []
            for part in parts:
                next_parts.extend(re.split(pattern, part))
            parts = next_parts

        return [part.strip(" ,.!?") for part in parts if part.strip(" ,.!?")]

    def _task_from_part(self, part: str) -> Task:
        p = part.strip()

        if self._contains(p, self._SCREENSHOT_WORDS):
            return Task("SCREENSHOT", p)

        if self._contains(p, self._VISION_WORDS):
            return Task("VISION", p)

        if self._contains(p, self._OPEN_WORDS):
            return Task("OPEN_APP", self._after_command(p, self._OPEN_WORDS))

        if self._contains(p, self._CLOSE_WORDS):
            return Task("CLOSE_APP", self._after_command(p, self._CLOSE_WORDS))

        if self._contains(p, self._SEARCH_WORDS):
            return Task("SEARCH", self._after_command(p, self._SEARCH_WORDS))

        if self._contains(p, self._WEATHER_WORDS):
            return Task("WEATHER", p)

        if self._contains(p, self._CALC_WORDS):
            return Task("CALCULATOR", p)

        if self._contains(p, self._MEDIA_WORDS):
            return Task("MEDIA", p)

        if self._contains(p, self._CLIPBOARD_WORDS):
            return Task("CLIPBOARD", p)

        if self._contains(p, self._FILE_WORDS):
            return Task("FILES", p)

        if self._contains(p, self._SYSTEM_WORDS):
            return Task("SYSTEM", p)

        return Task("CHAT", p)

    @staticmethod
    def _contains(text: str, words) -> bool:
        for word in words:
            pattern = r"(?<!\w)" + re.escape(word) + r"(?!\w)"
            if re.search(pattern, text, flags=re.IGNORECASE):
                return True
        return False

    @staticmethod
    def _after_command(text: str, commands) -> str:
        lowered = text.lower()
        matches = []

        for command in commands:
            index = lowered.find(command.lower())
            if index >= 0:
                matches.append((index, command))

        if not matches:
            return text

        index, command = min(matches, key=lambda item: item[0])
        target = text[index + len(command):].strip(" ,.!?")

        target = re.sub(
            r"^(ứng dụng|app|application)\s+",
            "",
            target,
            flags=re.IGNORECASE,
        )

        return target or text


if __name__ == "__main__":
    reasoner = Reasoner()

    examples = [
        "mở chrome rồi tìm Python rồi chụp màn hình",
        "mở ứng dụng calculator",
        "tìm kiếm Python",
        "xem màn hình",
        "tính 25 nhân 4",
        "đóng notepad",
    ]

    for example in examples:
        plan = reasoner.build(example)
        print(example)
        for task in plan:
            print("  ->", task.action, "|", task.target)
