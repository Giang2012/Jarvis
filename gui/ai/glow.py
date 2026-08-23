from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class Glow:

    def __init__(self):

        self.time = 0
        self.state = 0

    def setState(self, state):

        self.state = state

    # --------------------------

    def update(self):

        self.time += 0.05

    # --------------------------

    def draw(self,painter):

        self.update()

        painter.save()

        if self.state == 0:
            alpha = 30 + abs(math.sin(self.time))*15

        elif self.state == 1:
            alpha = 70 + abs(math.sin(self.time*5))*80

        elif self.state == 2:
            alpha = 60 + abs(math.sin(self.time*8))*60

        elif self.state == 3:
            alpha = 120

        else:
            alpha = 15

        for i in range(6):

            painter.setPen(Qt.NoPen)

            color = self.getColor()

            color.setAlpha(
                int(alpha)
            )

            painter.setBrush(color)
            painter.drawEllipse(
                QPointF(0,0),
                130+i*12,
                130+i*12
            )

        painter.restore()

    def getColor(self):

        if self.state == 0:

            return QColor(0,255,255)

        elif self.state == 1:

            return QColor(0,180,255)

        elif self.state == 2:

            return QColor(0,255,180)

        elif self.state == 3:

            return QColor(120,255,255)

        return QColor(40,120,120)