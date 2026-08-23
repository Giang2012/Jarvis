from PySide6.QtGui import *
from PySide6.QtCore import *

import random


class HologramParticles:

    def __init__(self):

        self.points = []

        for _ in range(15):

            self.points.append(

                QPointF(

                    random.randint(-20,20),

                    random.randint(-20,20)

                )

            )

    # ------------------------

    def draw(self,painter,rect):

        painter.save()

        painter.setPen(Qt.NoPen)

        painter.setBrush(

            QColor(

                0,

                255,

                255,

                150

            )

        )

        center = rect.center()

        for p in self.points:

            painter.drawEllipse(

                center + p,

                2,

                2

            )

        painter.restore()