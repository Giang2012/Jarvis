from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class Aura:

    def __init__(self):

        self.time = 0

    # --------------------------

    def update(self):

        self.time += 0.04

    # --------------------------

    def draw(self, painter):

        self.update()

        alpha = 60 + 30 * math.sin(

            self.time * 2

        )

        color = QColor(

            0,

            255,

            255,

            int(alpha)

        )

        painter.save()

        painter.setPen(Qt.NoPen)

        painter.setBrush(color)

        painter.drawEllipse(

            QPointF(0, 0),

            80,

            80

        )

        painter.restore()