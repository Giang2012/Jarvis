"""
services/ai_service.py

JARVIS AI Service
"""
from kernel.context import context
from PySide6.QtCore import QObject

from kernel.event_bus import event_bus
from kernel.events import (
    AI_READY,
    AI_THINKING,
    AI_SPEAKING,
)


class AIService(QObject):

    def __init__(self):

        super().__init__()

        self.ready = False

    # ==========================
    # Initialize
    # ==========================

    def start(self):

        self.ready = True

        event_bus.emit(AI_READY)

    def stop(self):

        self.ready = False

    # ==========================
    # Thinking
    # ==========================

    def think(self, prompt: str):

        context.add_message(
            "user",
            prompt
        )

        event_bus.emit(
            AI_THINKING,
            prompt
        )

        answer = f"Processing: {prompt}"

        context.add_message(
            "assistant",
            answer
        )

        event_bus.emit(
            AI_SPEAKING,
            answer
        )

        return answer