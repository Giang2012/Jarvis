import os
import subprocess
import time
from pathlib import Path
from typing import Optional

try:
    import pyautogui
except Exception:
    pyautogui = None


class DesktopService:
    """Windows desktop automation with explicit, bounded operations."""

    APP_ALIASES = {
        "chrome": "chrome",
        "google chrome": "chrome",
        "edge": "msedge",
        "microsoft edge": "msedge",
        "notepad": "notepad",
        "calculator": "calc",
        "calc": "calc",
        "explorer": "explorer",
        "file explorer": "explorer",
        "terminal": "wt",
        "powershell": "powershell",
        "cmd": "cmd",
    }

    def open_app(self, name: str):
        target = self._normalize(name)
        command = self.APP_ALIASES.get(target, target)
        if not command:
            return "No application specified."

        try:
            subprocess.Popen(command, shell=True)
            return f"Opening {target}."
        except Exception as exc:
            return f"Could not open {target}: {exc}"

    def close_app(self, name: str):
        target = self._normalize(name)
        aliases = {
            "chrome": "chrome.exe",
            "google chrome": "chrome.exe",
            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe",
            "notepad": "notepad.exe",
            "calculator": "CalculatorApp.exe",
            "calc": "CalculatorApp.exe",
            "explorer": "explorer.exe",
        }
        process = aliases.get(target, target if target.endswith(".exe") else f"{target}.exe")

        try:
            result = subprocess.run(
                ["taskkill", "/IM", process, "/T", "/F"],
                capture_output=True,
                text=True,
                timeout=8,
            )
            if result.returncode == 0:
                return f"Closed {target}."
            return f"Could not close {target}."
        except Exception as exc:
            return f"Could not close {target}: {exc}"

    def press(self, key: str):
        if pyautogui is None:
            return "PyAutoGUI is not available."
        key = key.strip().lower()
        if not key or len(key) > 30:
            return "Invalid key."
        try:
            pyautogui.press(key)
            return f"Pressed {key}."
        except Exception as exc:
            return f"Key action failed: {exc}"

    def hotkey(self, keys):
        if pyautogui is None:
            return "PyAutoGUI is not available."
        parts = [x.strip().lower() for x in keys.split("+") if x.strip()]
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
        try:
            pyautogui.write(str(text), interval=float(interval))
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
        value = str(value or "").strip()
        prefixes = (
            "ứng dụng ", "app ", "application ",
            "mở ", "open ", "chạy ", "launch ",
            "đóng ", "tắt ", "close ",
        )
        lowered = value.lower()
        for prefix in prefixes:
            if lowered.startswith(prefix):
                value = value[len(prefix):].strip()
                break
        return value.strip().lower()
