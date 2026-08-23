from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class DynamicRing:

    def __init__(self):

        self.angle = 0
        self.time = 0

        self.radius = 95

    # ---------------------

    def update(self):

        self.angle += 0.45
        self.time += 0.08

    # ---------------------

    def draw(self,painter):

        self.update()

        painter.save()

        painter.rotate(self.angle)

        pen = QPen(
            QColor(0,255,255,180),
            2
        )

        painter.setPen(pen)

        points=[]

        for i in range(180):

            a=math.radians(i*2)

            r=self.radius+math.sin(
                self.time+i*0.12
            )*5

            x=math.cos(a)*r
            y=math.sin(a)*r

            points.append(
                QPointF(x,y)
            )

        painter.drawPolyline(points)

        painter.restore()