from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class EnergyLink:

    def __init__(self):

        self.angle = 0

    # --------------------------

    def update(self):

        self.angle += 0.6

        if self.angle >= 360:
            self.angle -= 360

    # --------------------------

    def draw(self, painter):

        self.update()

        painter.save()

        pen = QPen(
            QColor(0,255,255,40),
            1
        )

        painter.setPen(pen)

        r = 110

        pts = []

        for i in range(6):

            a = math.radians(self.angle + i*60)

            pts.append(
                QPointF(
                    math.cos(a)*r,
                    math.sin(a)*r
                )
            )

        for i in range(len(pts)):

            painter.drawLine(
                pts[i],
                pts[(i+1)%len(pts)]
            )

            painter.drawLine(
                QPointF(0,0),
                pts[i]
            )

        painter.restore()