from skills.base_skill import BaseSkill


class VisionSkill(BaseSkill):
    def __init__(self, screen):
        super().__init__()
        self.name = "VISION"
        self.screen = screen

    def execute(self, text):
        command = str(text or "").lower().strip()
        semantic = any(
            phrase in command
            for phrase in (
                "what do you see",
                "what's on my screen",
                "look at my screen",
                "màn hình đang",
                "đang làm gì",
                "nhìn màn hình",
            )
        )
        result = self.screen.inspect(semantic=semantic)
        if result.get("description"):
            return result["description"]
        ocr = result.get("ocr", {})
        if ocr.get("text"):
            return "Visible text: " + ocr["text"][:1800]
        if result.get("description_error"):
            return "Vision model unavailable; OCR fallback also has no text."
        return "Screen captured, but no readable text was detected."
