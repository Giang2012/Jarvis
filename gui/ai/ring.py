from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class Ring:

    def __init__(self, radius, speed, width=2):

        self.radius = radius
        self.speed = speed
        self.angle = 0
        self.width = width

    # --------------------------

    def update(self):

        self.angle += self.speed

        if self.angle >= 360:
            self.angle -= 360

    # --------------------------

    def draw(self, painter):

        self.update()

        painter.save()

        painter.rotate(self.angle)

        pen = QPen(
            QColor(0,255,255,180),
            self.width
        )

        painter.setPen(pen)

        rect = QRectF(
            -self.radius,
            -self.radius,
            self.radius*2,
            self.radius*2
        )

        painter.drawArc(
            rect,
            0*16,
            110*16
        )

        painter.drawArc(
            rect,
            180*16,
            70*16
        )

        painter.restore()