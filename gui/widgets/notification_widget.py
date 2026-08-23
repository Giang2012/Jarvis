from PySide6.QtWidgets import QLabel, QVBoxLayout

from gui.widgets.glass_card import GlassCard

from kernel.event_bus import event_bus
from kernel.events import NOTIFICATION


class NotificationWidget(GlassCard):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        self.title = QLabel("Notifications")
        self.message = QLabel("No notification")

        self.title.setStyleSheet("""
        QLabel{
            color:white;
            font-size:16px;
            font-weight:bold;
            background:transparent;
        }
        """)

        self.message.setWordWrap(True)

        self.message.setStyleSheet("""
        QLabel{
            color:#BFEFFF;
            font-size:13px;
            background:transparent;
        }
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.message)
        layout.addStretch()

        event_bus.subscribe(
            NOTIFICATION,
            self.update_notification
        )

    def update_notification(self, item):

        self.title.setText(item.title)

        self.message.setText(
            f"{item.message}\n{item.time}"
        )