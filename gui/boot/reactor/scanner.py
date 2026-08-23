from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPen
from math import cos, sin, radians


class ReactorScanner:

    def __init__(self):

        self.radius = 110
        self.angle = 0

    def update(self):

        self.angle += 2

        if self.angle >= 360:
            self.angle = 0

    def draw(self, painter):

        self.update()

        painter.save()

        pen = QPen(
            QColor(
                0,
                255,
                255,
                180
            )
        )

        pen.setWidth(2)

        painter.setPen(pen)

        x = cos(radians(self.angle)) * self.radius
        y = sin(radians(self.angle)) * self.radius

        painter.drawLine(
            QPointF(0, 0),
            QPointF(x, y)
        )

        painter.restore()