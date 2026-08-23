from PySide6.QtGui import *
from PySide6.QtCore import *


class Scanner:

    def __init__(self):

        self.y = -120

    # --------------------------

    def update(self):

        self.y += 2

        if self.y > 120:

            self.y = -120

    # --------------------------

    def draw(self,painter):

        self.update()

        painter.save()

        pen = QPen(
            QColor(0,255,255,80),
            2
        )

        painter.setPen(pen)

        painter.drawLine(
            -130,
            self.y,
            130,
            self.y
        )

        painter.restore()