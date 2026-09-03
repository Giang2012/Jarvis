import os


class Settings:
    """Runtime settings for local-first JARVIS capabilities."""

    OLLAMA_URL = os.getenv(
        "JARVIS_OLLAMA_URL", "http://localhost:11434"
    )
    OLLAMA_MODEL = os.getenv(
        "JARVIS_OLLAMA_MODEL", "llama3.2:3b"
    )
    VISION_MODEL = os.getenv(
        "JARVIS_VISION_MODEL", "llava:7b"
    )
    SCREEN_AWARENESS_DEFAULT = (
        os.getenv("JARVIS_SCREEN_AWARENESS", "0") == "1"
    )
    SCREEN_INTERVAL = float(
        os.getenv("JARVIS_SCREEN_INTERVAL", "5")
    )
