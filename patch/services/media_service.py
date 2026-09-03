import subprocess


class MediaService:
    def key(self, action):
        action = str(action or "").strip().lower()
        mapping = {
            "play": "playpause",
            "pause": "playpause",
            "playpause": "playpause",
            "next": "nexttrack",
            "previous": "prevtrack",
            "prev": "prevtrack",
            "volume up": "volumeup",
            "volume down": "volumedown",
            "mute": "volumemute",
        }
        key = mapping.get(action)
        if not key:
            return f"Unknown media action: {action}"
        try:
            import pyautogui
            pyautogui.press(key)
            return f"Media: {action}."
        except Exception as exc:
            return f"Media control failed: {exc}"
