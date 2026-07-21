from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtCore import Qt


class GlassPanel(QFrame):

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground)

        self.setStyleSheet("""
        QFrame{
            background:rgba(8,15,25,180);

            border:1px solid rgba(0,255,255,60);

            border-radius:18px;
        }
        """)

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(
            QColor(0,255,255,40),
            2
        )

        painter.setPen(pen)

        painter.drawRoundedRect(
            self.rect().adjusted(1,1,-2,-2),
            18,
            18
        )