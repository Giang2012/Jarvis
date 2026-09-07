import os


class Settings:
    """Runtime settings for local-first JARVIS capabilities."""

    OLLAMA_URL = os.getenv("JARVIS_OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("JARVIS_OLLAMA_MODEL", "llama3.2:3b")
    VISION_MODEL = os.getenv("JARVIS_VISION_MODEL", "llava:7b")
    SCREEN_AWARENESS_DEFAULT = os.getenv("JARVIS_SCREEN_AWARENESS", "0") == "1"
    SCREEN_INTERVAL = float(os.getenv("JARVIS_SCREEN_INTERVAL", "5"))

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


OLLAMA_URL = Settings.OLLAMA_URL
OLLAMA_MODEL = Settings.OLLAMA_MODEL
VISION_MODEL = Settings.VISION_MODEL
SCREEN_AWARENESS_DEFAULT = Settings.SCREEN_AWARENESS_DEFAULT
SCREEN_INTERVAL = Settings.SCREEN_INTERVAL
GEMINI_API_KEY = Settings.GEMINI_API_KEY
GEMINI_MODEL = Settings.GEMINI_MODEL
