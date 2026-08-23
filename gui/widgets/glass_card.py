from PySide6.QtWidgets import QFrame
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtCore import Qt


class GlassCard(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setMinimumHeight(180)

        self.radius = 18

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)

        painter.setPen(
            QPen(
                QColor(0, 220, 255, 120),
                1.5
            )
        )

        painter.setBrush(
            QColor(15, 22, 35, 120)
        )

        painter.drawRoundedRect(
            rect,
            self.radius,
            self.radius
        )

        glow = QColor(0, 220, 255, 25)

        painter.setPen(Qt.NoPen)

        painter.setBrush(glow)

        painter.drawRoundedRect(
            rect.adjusted(4, 4, -4, -4),
            self.radius,
            self.radius
        )