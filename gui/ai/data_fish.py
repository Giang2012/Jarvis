from PySide6.QtGui import *
from PySide6.QtCore import *

import math
import random


class DataFish:

    def __init__(self):

        self.angle = random.uniform(0,360)

        self.radius = random.uniform(120,180)

        self.speed = random.uniform(0.08,0.25)

        self.size = random.randint(8,16)

        self.alpha = random.randint(80,180)

    # --------------------------

    def update(self):

        self.angle += self.speed

        if self.angle >= 360:

            self.angle -= 360

    # --------------------------

    def draw(self,painter):

        self.update()

        rad = math.radians(self.angle)

        x = math.cos(rad)*self.radius

        y = math.sin(rad)*self.radius

        painter.save()

        painter.translate(x,y)

        painter.rotate(self.angle+90)

        pen = QPen(
            QColor(0,255,255,self.alpha),
            2
        )

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        # body

        painter.drawEllipse(
            QRectF(
                -6,
                -3,
                12,
                6
            )
        )

        # tail

        painter.drawLine(
            -6,
            0,
            -12,
            -4
        )

        painter.drawLine(
            -6,
            0,
            -12,
            4
        )

        painter.restore()