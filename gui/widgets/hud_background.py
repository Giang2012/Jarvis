from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen
)

import random
import math


class HUDBackground(QWidget):

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.scan_y = 0
        self.rotation = 0

        self.stars = []

        for _ in range(120):

            self.stars.append([
                random.randint(0, 1920),
                random.randint(0, 1080),
                random.randint(1, 3),
                random.randint(40, 150)
            ])

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    def animate(self):

        self.scan_y += 2

        if self.scan_y > self.height():
            self.scan_y = 0

        self.rotation += 0.5

        if self.rotation >= 360:
            self.rotation = 0

        for star in self.stars:

            star[1] += 0.15

            if star[1] > self.height():

                star[0] = random.randint(0, self.width())
                star[1] = 0

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        painter.fillRect(
            self.rect(),
            QColor(5, 10, 20)
        )

        # grid

        pen = QPen(
            QColor(0, 255, 255, 20),
            1
        )

        painter.setPen(pen)

        step = 40

        for x in range(0, w, step):
            painter.drawLine(x, 0, x, h)

        for y in range(0, h, step):
            painter.drawLine(0, y, w, y)

        # stars

        painter.setPen(Qt.NoPen)

        for x, y, r, a in self.stars:

            painter.setBrush(
                QColor(0, 255, 255, a)
            )

            painter.drawEllipse(
                int(x),
                int(y),
                r,
                r
            )

        # scan line

        painter.fillRect(
            0,
            self.scan_y,
            w,
            3,
            QColor(0, 255, 255, 80)
        )

        # center radar

        cx = w / 2
        cy = h / 2

        radius = min(w, h) / 3

        pen = QPen(
            QColor(0, 255, 255, 18),
            1
        )

        painter.setPen(pen)

        for i in range(1, 6):

            painter.drawEllipse(
                cx - radius * i / 5,
                cy - radius * i / 5,
                radius * 2 * i / 5,
                radius * 2 * i / 5
            )

        # rotating beam

        angle = math.radians(self.rotation)

        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius

        pen = QPen(
            QColor(0, 255, 255, 100),
            2
        )

        painter.setPen(pen)

        painter.drawLine(cx, cy, x, y)

        # crosshair

        pen = QPen(
            QColor(0,255,255,25),
            1
        )

        painter.setPen(pen)

        painter.drawLine(cx-radius, cy, cx+radius, cy)
        painter.drawLine(cx, cy-radius, cx, cy+radius)