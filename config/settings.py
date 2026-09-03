import os


# ============================================================
# Existing Gemini configuration
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


# ============================================================
# Local Ollama configuration
# ============================================================

OLLAMA_URL = os.getenv(
    "JARVIS_OLLAMA_URL",
    "http://localhost:11434",
)

OLLAMA_MODEL = os.getenv(
    "JARVIS_OLLAMA_MODEL",
    "llama3.2:3b",
)

VISION_MODEL = os.getenv(
    "JARVIS_VISION_MODEL",
    "llava:7b",
)


# ============================================================
# Screen awareness
# ============================================================

SCREEN_AWARENESS_DEFAULT = (
    os.getenv("JARVIS_SCREEN_AWARENESS", "0") == "1"
)

SCREEN_INTERVAL = float(
    os.getenv("JARVIS_SCREEN_INTERVAL", "5")
)


class Settings:
    """Runtime settings for JARVIS."""

    GEMINI_API_KEY = GEMINI_API_KEY
    GEMINI_MODEL = GEMINI_MODEL

    OLLAMA_URL = OLLAMA_URL
    OLLAMA_MODEL = OLLAMA_MODEL
    VISION_MODEL = VISION_MODEL

    SCREEN_AWARENESS_DEFAULT = SCREEN_AWARENESS_DEFAULT
    SCREEN_INTERVAL = SCREEN_INTERVAL