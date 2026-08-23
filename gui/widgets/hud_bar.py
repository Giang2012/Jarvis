import math
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QFont,
)
from PySide6.QtCore import Qt


class HUDBar(QWidget):

    def __init__(self, title="CPU"):
        super().__init__()

        self.title = title
        self.value = 0
        self.value = 0
        self.glow = 0
        self.display_value = 0

        self.setMinimumHeight(48)

    def setValue(self, value):

        self.value = max(
            0,
            min(100, value)
        )

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # -----------------------------
        # Smooth Animation
        # -----------------------------

        if self.display_value < self.value:

            self.display_value += 1

        elif self.display_value > self.value:

            self.display_value -= 1

        if self.display_value != self.value:

            self.update()

        self.glow += 0.15

        if self.glow > math.pi * 2:
            self.glow = 0
        # -----------------------------
        # TITLE
        # -----------------------------

        painter.setPen(self.currentColor())

        painter.setFont(
            QFont(
                "Segoe UI",
                9,
                QFont.Bold
            )
        )

        painter.drawText(
            0,
            12,
            self.title
        )

        # -----------------------------
        # HUD SEGMENTS
        # -----------------------------

        x = 0
        y = 20

        bw = w - 60
        bh = 12

        segments = 20

        gap = 2

        segment_width = (bw - (segments - 1) * gap) / segments

        active = int(
            self.display_value
            / 100
            * segments
        )

        for i in range(segments):

            sx = x + i * (segment_width + gap)

            if i < active:

                alpha = 180 + int(
                    60 * math.sin(
                        self.glow + i * 0.3
                    )
                )

                painter.setBrush(
                    QColor(
                        0,
                        220,
                        255,
                        alpha
                    )
                )

            else:

                painter.setBrush(
                    QColor(
                        0,
                        220,
                        255,
                        25
                    )
                )

            painter.setPen(Qt.NoPen)

            painter.drawRoundedRect(
                sx,
                y,
                segment_width,
                bh,
                2,
                2
            )

        # -----------------------------
        # VALUE
        # -----------------------------

        painter.setPen(Qt.white)

        font = QFont("Consolas", 10)
        font.setBold(True)

        painter.setFont(font)

        painter.drawText(

            bw + 8,

            y + 10,

        f"{self.display_value:02d}%"

        )

    def currentColor(self):

        if self.display_value < 60:
            return self.currentColor()

        if self.display_value < 85:
            return QColor(255,210,40)

        return QColor(255,70,70)