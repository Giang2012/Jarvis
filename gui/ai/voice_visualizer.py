from PySide6.QtGui import *
from PySide6.QtCore import *
import random


class VoiceVisualizer:

    def __init__(self):

        self.level = 0

        self.target = 0

    # ------------------------

    def setLevel(self, level):

        self.target = max(
            0,
            min(1, level)
        )

    # ------------------------

    def update(self):

        self.level += (self.target-self.level)*0.15

    # ------------------------

    def draw(self,painter):

        self.update()

        painter.save()

        pen = QPen(
            QColor(0,255,255,180),
            3
        )

        painter.setPen(pen)

        bars = 48

        for i in range(bars):

            angle = i*360/bars

            painter.save()

            painter.rotate(angle)

            h = 8 + self.level*35 + random.uniform(-2,2)

            painter.drawLine(
                0,
                -120,
                0,
                -120-h
            )

            painter.restore()

        painter.restore()