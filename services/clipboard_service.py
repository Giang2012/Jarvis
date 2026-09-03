try:
    import pyperclip
except Exception:
    pyperclip = None


class ClipboardService:
    def get(self):
        if pyperclip is None:
            return ""
        try:
            return pyperclip.paste()
        except Exception:
            return ""

    def set(self, text):
        if pyperclip is None:
            return "pyperclip is not installed."
        try:
            pyperclip.copy(str(text))
            return "Clipboard updated."
        except Exception as exc:
            return f"Clipboard failed: {exc}"
