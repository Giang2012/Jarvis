from PySide6.QtGui import *

from gui.common.panels.base_panel import BasePanel


class NotificationPanel(BasePanel):

    def __init__(self):

        super().__init__("NOTIFICATIONS")

        self.messages = [

            "System Ready",

            "Voice Offline",

            "Network Stable"

        ]

    # ------------------------------

    def drawContent(self,painter,rect):

        painter.save()

        painter.setPen(Qt.white)

        font = QFont("Consolas",9)

        painter.setFont(font)

        y = rect.top()+60

        for msg in self.messages:

            painter.drawText(

                rect.left()+20,

                y,

                "• " + msg

            )

            y += 25

        painter.restore()