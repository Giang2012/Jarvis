import random
from PySide6.QtGui import *
from PySide6.QtCore import *


class ServoSparks:

    def __init__(self):

        self.points = []

        for _ in range(30):

            self.points.append([
                random.randint(-120,120),
                random.randint(-170,240),
                random.randint(2,5)
            ])

    # =============================

    def update(self):

        for p in self.points:

            p[1] += p[2]

            if p[1] > 250:

                p[0] = random.randint(-120,120)
                p[1] = -170

    # =============================

    def draw(self,painter):

        self.update()

        painter.save()

        painter.setPen(Qt.NoPen)

        for x,y,s in self.points:

            painter.setBrush(
                QColor(
                    0,
                    255,
                    255,
                    180
                )
            )

            painter.drawEllipse(
                QPointF(x,y),
                1.5,
                1.5
            )

        painter.restore()