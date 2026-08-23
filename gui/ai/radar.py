from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class Radar:

    def __init__(self):

        self.angle = 0

    def update(self):

        self.angle += 1

        if self.angle >= 360:

            self.angle = 0

    def draw(self, painter):

        self.update()

        painter.save()

        painter.rotate(self.angle)

        gradient = QConicalGradient(
            0,
            0,
            0
        )

        gradient.setColorAt(
            0,
            QColor(0,255,255,120)
        )

        gradient.setColorAt(
            0.08,
            QColor(0,255,255,0)
        )

        painter.setPen(Qt.NoPen)

        painter.setBrush(gradient)

        path = QPainterPath()

        path.moveTo(0,0)

        path.arcTo(
            -180,
            -180,
            360,
            360,
            0,
            30
        )

        path.closeSubpath()

        painter.drawPath(path)

        painter.restore()