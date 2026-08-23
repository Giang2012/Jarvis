from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class AIEyes:

    def __init__(self):

        self.mouse = QPointF(0, 0)

        self.left = QPointF(-18, -8)

        self.right = QPointF(18, -8)

        self.radius = 4

        self.blink = 1.0

        self.time = 0

    # --------------------------------

    def update(self):

        self.time += 0.03

        self.blink = 0.85 + 0.15 * math.sin(self.time * 2)

    # --------------------------------

    def setMouse(self, pos):

        self.mouse = pos

    # --------------------------------

    def draw(self, painter):

        self.update()

        painter.save()

        color = QColor(0, 255, 255)

        painter.setPen(Qt.NoPen)

        painter.setBrush(color)

        painter.drawEllipse(

            self.left,

            self.radius,

            self.radius * self.blink

        )

        painter.drawEllipse(

            self.right,

            self.radius,

            self.radius * self.blink

        )

        painter.restore()