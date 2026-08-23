from PySide6.QtGui import *
from PySide6.QtCore import *
import math
import random


class Orbit:

    def __init__(self):

        self.radius = random.randint(70,130)

        self.angle = random.randint(0,360)

        self.speed = random.uniform(0.15,0.5)

        self.size = random.randint(3,7)

        self.alpha = random.randint(120,255)

    # ------------------------

    def update(self):

        self.angle += self.speed

        if self.angle >= 360:

            self.angle -= 360

    # ------------------------

    def draw(self,painter):

        self.update()

        rad = math.radians(self.angle)

        x = math.cos(rad)*self.radius

        y = math.sin(rad)*self.radius

        painter.save()

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                0,
                255,
                255,
                self.alpha
            )
        )

        painter.drawEllipse(
            QPointF(x,y),
            self.size,
            self.size
        )

        painter.restore()