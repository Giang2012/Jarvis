import os
import subprocess
import time
from pathlib import Path
from typing import Optional

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    import pyperclip
except Exception:
    pyperclip = None


class DesktopService:
    """Bounded Windows desktop automation. No arbitrary shell command execution."""

    APP_ALIASES = {
        "chrome": "chrome", "google chrome": "chrome", "edge": "msedge",
        "microsoft edge": "msedge", "notepad": "notepad", "calculator": "calc",
        "calc": "calc", "explorer": "explorer", "file explorer": "explorer",
        "terminal": "wt", "windows terminal": "wt", "powershell": "powershell", "cmd": "cmd",
    }

    def open_app(self, name: str):
        target = self._normalize(name)
        command = self.APP_ALIASES.get(target)
        if not command:
            return f"Application '{target}' is not in the safe launcher catalog."
        try:
            subprocess.Popen([command], shell=False)
            return f"Opening {target}."
        except Exception as exc:
            return f"Could not open {target}: {exc}"

    def close_app(self, name: str):
        target = self._normalize(name)
        aliases = {"chrome":"chrome.exe", "google chrome":"chrome.exe", "edge":"msedge.exe", "microsoft edge":"msedge.exe", "notepad":"notepad.exe", "calculator":"CalculatorApp.exe", "calc":"CalculatorApp.exe", "explorer":"explorer.exe"}
        process = aliases.get(target)
        if not process:
            return f"Application '{target}' is not in the safe closer catalog."
        try:
            result = subprocess.run(["taskkill", "/IM", process, "/T", "/F"], capture_output=True, text=True, timeout=8)
            return f"Closed {target}." if result.returncode == 0 else f"Could not close {target}."
        except Exception as exc:
            return f"Could not close {target}: {exc}"

    def press(self, key: str):
        if pyautogui is None:
            return "PyAutoGUI is not available."
        try:
            pyautogui.press(str(key).strip().lower())
            return f"Pressed {key}."
        except Exception as exc:
            return f"Key action failed: {exc}"

    def hotkey(self, keys):
        if pyautogui is None:
            return "PyAutoGUI is not available."
        parts = [x.strip().lower() for x in str(keys).split("+") if x.strip()]
        if not parts or len(parts) > 5:
            return "Invalid hotkey."
        try:
            pyautogui.hotkey(*parts)
            return f"Pressed {'+'.join(parts)}."
        except Exception as exc:
            return f"Hotkey failed: {exc}"

    def click(self, x: int, y: int, button="left", clicks=1):
        if pyautogui is None:
            return "PyAutoGUI is not available."
        try:
            pyautogui.click(int(x), int(y), clicks=int(clicks), button=button)
            return f"Clicked {x},{y}."
        except Exception as exc:
            return f"Click failed: {exc}"

    def type_text(self, text: str, interval=0.01):
        if pyautogui is None:
            return "PyAutoGUI is not available."
        value = str(text)
        try:
            if pyperclip and any(ord(ch) > 127 for ch in value):
                pyperclip.copy(value)
                pyautogui.hotkey("ctrl", "v")
            else:
                pyautogui.write(value, interval=float(interval))
            return "Text entered."
        except Exception as exc:
            return f"Typing failed: {exc}"

    def move(self, x: int, y: int, duration=0.15):
        if pyautogui is None:
            return "PyAutoGUI is not available."
        try:
            pyautogui.moveTo(int(x), int(y), duration=float(duration))
            return f"Moved pointer to {x},{y}."
        except Exception as exc:
            return f"Pointer move failed: {exc}"

    def screenshot(self, path: Optional[str] = None):
        if pyautogui is None:
            return None, "PyAutoGUI is not available."
        try:
            image = pyautogui.screenshot()
            if path is None:
                folder = Path.home() / "Pictures" / "JARVIS_Screenshots"
                folder.mkdir(parents=True, exist_ok=True)
                path = str(folder / f"jarvis_{time.strftime('%Y%m%d_%H%M%S')}.png")
            image.save(path)
            return path, f"Screenshot saved to {path}."
        except Exception as exc:
            return None, f"Screenshot failed: {exc}"

    @staticmethod
    def _normalize(value):
        value = str(value or "").strip().lower()
        for prefix in ("ứng dụng ", "app ", "application ", "mở ", "open ", "chạy ", "launch ", "đóng ", "tắt ", "close "):
            if value.startswith(prefix):
                return value[len(prefix):].strip()
        return value
