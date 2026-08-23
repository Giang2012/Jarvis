from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class Pulse:

    def __init__(self):

        self.radius = 25

        self.speed = 0.8

        self.alpha = 180

    # ---------------------

    def update(self):

        self.radius += self.speed

        self.alpha -= 1

        if self.alpha <= 0:

            self.radius = 25

            self.alpha = 180

    # ---------------------

    def draw(self,painter):

        self.update()

        pen = QPen(

            QColor(
                0,
                255,
                255,
                self.alpha
            ),

            2

        )

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        painter.drawEllipse(

            QPointF(0,0),

            self.radius,

            self.radius

        )