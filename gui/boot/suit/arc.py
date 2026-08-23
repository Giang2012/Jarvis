import random

from PySide6.QtGui import *
from PySide6.QtCore import *


class ElectricArc:

    def __init__(self):

        self.points = []

        self.randomize()

    # =====================================

    def randomize(self):

        self.points.clear()

        for i in range(10):

            x = -70 + i * 15 + random.randint(-6, 6)
            y = random.randint(-6, 6)

            self.points.append(QPointF(x, y))

    # =====================================

    def update(self):

        self.randomize()

    # =====================================

    def draw(self, painter):

        self.update()

        pen = QPen(QColor(0,255,255,180),2)

        painter.setPen(pen)

        for i in range(len(self.points)-1):

            painter.drawLine(
                self.points[i],
                self.points[i+1]
            )