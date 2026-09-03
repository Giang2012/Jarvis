import re

from ai.plan import Plan
from ai.task import Task


class Reasoner:
    """Deterministic first-pass planner with explicit OS actions."""

    def build(self, text):
        raw = str(text or "").strip().lower()
        plan = Plan()
        if not raw:
            return plan
        for part in self._split_commands(raw):
            plan.add(self._task_from_part(part))
        return plan

    def _split_commands(self, text):
        separators = [
            r"\s+then\s+", r"\s+after that\s+", r"\s+sau đó\s+",
            r"\s+rồi\s+", r"\s+tiếp theo\s+",
        ]
        parts = [text]
        for pattern in separators:
            next_parts = []
            for part in parts:
                next_parts.extend(re.split(pattern, part))
            parts = next_parts
        return [p.strip() for p in parts if p.strip()]

    def _task_from_part(self, p):
        if self._has(p, "screenshot", "screen shot", "chụp màn hình", "chụp lại màn hình", "capture screen"):
            return Task("SCREENSHOT", p)
        if self._has(p, "nhìn màn hình", "xem màn hình", "quan sát màn hình", "màn hình đang", "trên màn hình", "đang làm gì", "tôi đang làm gì", "what do you see", "what's on my screen", "what is on my screen", "vision"):
            return Task("VISION", p)
        if self._has(p, "open", "mở", "launch", "chạy", "khởi động"):
            return Task("OPEN_APP", self._after_command(p, ("open", "mở", "launch", "chạy", "khởi động")))
        if self._has(p, "close", "đóng", "tắt ứng dụng", "thoát ứng dụng", "close app", "exit app"):
            return Task("CLOSE_APP", self._after_command(p, ("close", "đóng", "tắt ứng dụng", "thoát ứng dụng", "close app", "exit app")))
        if self._has(p, "search", "tìm kiếm", "tìm", "google", "tra cứu", "hãy tìm", "search for"):
            return Task("SEARCH", self._after_command(p, ("search for", "search", "tìm kiếm", "tìm", "google", "tra cứu", "hãy tìm")))
        if self._has(p, "weather", "thời tiết", "dự báo thời tiết"):
            return Task("WEATHER", p)
        if self._has(p, "calculate", "calculator", "tính toán", "tính"):
            return Task("CALCULATOR", p)
        if self._has(p, "play", "pause", "next track", "previous track", "next song", "previous song", "phát nhạc", "tạm dừng", "bài tiếp", "bài trước", "tăng âm lượng", "giảm âm lượng", "tắt tiếng", "bật tiếng", "mute", "unmute", "volume up", "volume down"):
            return Task("MEDIA", p)
        if self._has(p, "clipboard", "bộ nhớ tạm", "copy", "paste", "sao chép", "dán"):
            return Task("CLIPBOARD", p)
        if self._has(p, "file", "files", "tệp", "tệp tin", "thư mục", "folder", "folders"):
            return Task("FILES", p)
        if self._has(p, "shutdown", "shut down", "tắt máy", "restart", "khởi động lại", "reboot", "lock", "khóa máy"):
            return Task("SYSTEM", p)
        return Task("CHAT", p)

    @staticmethod
    def _has(text, *words):
        return any(word in text for word in words)

    @staticmethod
    def _after_command(text, commands):
        lowered = text.lower()
        matches = [(lowered.find(command), command) for command in commands if lowered.find(command) >= 0]
        if not matches:
            return text
        index, command = min(matches, key=lambda item: item[0])
        target = text[index + len(command):].strip()
        target = re.sub(r"^(ứng dụng|app|application)\s+", "", target, flags=re.I)
        return target or text
