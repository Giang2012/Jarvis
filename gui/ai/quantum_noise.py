from PySide6.QtGui import *
from PySide6.QtCore import *

import random


class QuantumNoise:

    def draw(self,painter):

        painter.save()

        painter.setPen(
            QColor(
                0,
                255,
                255,
                18
            )
        )

        for i in range(45):

            x=random.randint(-220,220)

            y=random.randint(-220,220)

            painter.drawPoint(x,y)

        painter.restore()