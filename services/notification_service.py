"""
services/notification_service.py

JARVIS Notification Service
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

from kernel.event_bus import event_bus
from kernel.events import NOTIFICATION


@dataclass
class Notification:

    title: str
    message: str
    level: str = "info"
    time: str = ""


class NotificationService:

    MAX_HISTORY = 100

    def __init__(self):

        self.history: List[Notification] = []

    # ==========================
    # Send
    # ==========================

    def notify(
        self,
        title: str,
        message: str,
        level: str = "info"
    ):

        item = Notification(
            title=title,
            message=message,
            level=level,
            time=datetime.now().strftime("%H:%M:%S")
        )

        self.history.append(item)

        if len(self.history) > self.MAX_HISTORY:
            self.history.pop(0)

        event_bus.emit(
            NOTIFICATION,
            item
        )

    # ==========================
    # History
    # ==========================

    def get_history(self):

        return self.history

    # ==========================
    # Clear
    # ==========================

    def clear(self):

        self.history.clear()