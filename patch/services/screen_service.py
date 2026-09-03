import base64
import io
import os
from pathlib import Path
from typing import Optional

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    import pytesseract
except Exception:
    pytesseract = None

import requests


class ScreenService:
    """Local screen capture/OCR/vision adapter.

    Screen awareness is opt-in. Captured frames stay local unless a local
    Ollama vision model is explicitly configured and called.
    """

    def __init__(self, vision_model: Optional[str] = None):
        self.vision_model = vision_model or os.getenv(
            "JARVIS_VISION_MODEL", "llava:7b"
        )
        self.ollama_url = os.getenv(
            "JARVIS_OLLAMA_URL", "http://localhost:11434"
        )

    def capture(self):
        if pyautogui is None:
            raise RuntimeError("PyAutoGUI is not installed.")
        return pyautogui.screenshot()

    def save(self, path=None):
        image = self.capture()
        if path is None:
            folder = Path.home() / "Pictures" / "JARVIS_Screenshots"
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / "screen.png"
        image.save(path)
        return str(path)

    def ocr(self, image=None):
        if pytesseract is None:
            return {
                "text": "",
                "boxes": [],
                "available": False,
                "message": "pytesseract is not installed.",
            }

        image = image or self.capture()
        data = pytesseract.image_to_data(
            image, output_type=pytesseract.Output.DICT
        )
        boxes = []
        words = []
        for i, text in enumerate(data["text"]):
            text = (text or "").strip()
            if not text:
                continue
            words.append(text)
            boxes.append({
                "text": text,
                "x": int(data["left"][i]),
                "y": int(data["top"][i]),
                "width": int(data["width"][i]),
                "height": int(data["height"][i]),
                "confidence": float(data["conf"][i]),
            })
        return {
            "text": " ".join(words),
            "boxes": boxes,
            "available": True,
        }

    def find_text(self, text, image=None):
        query = str(text or "").strip().lower()
        if not query:
            return None
        result = self.ocr(image)
        for box in result.get("boxes", []):
            if query in box["text"].lower():
                return box
        return None

    def describe_with_ollama(self, image=None, prompt=None):
        image = image or self.capture()
        prompt = prompt or (
            "Describe what is visible on this computer screen. "
            "Identify the active application, important visible UI elements, "
            "and what the user appears to be doing. Be concise."
        )
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        encoded = base64.b64encode(buffer.getvalue()).decode("ascii")

        payload = {
            "model": self.vision_model,
            "messages": [{
                "role": "user",
                "content": prompt,
                "images": [encoded],
            }],
            "stream": False,
        }
        response = requests.post(
            f"{self.ollama_url}/api/chat",
            json=payload,
            timeout=90,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "").strip()

    def inspect(self, semantic=False):
        image = self.capture()
        ocr = self.ocr(image)
        result = {"ocr": ocr, "description": None}

        if semantic:
            try:
                result["description"] = self.describe_with_ollama(image)
            except Exception as exc:
                result["description_error"] = str(exc)

        return result
