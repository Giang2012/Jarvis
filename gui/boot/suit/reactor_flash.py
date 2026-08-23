from PySide6.QtGui import *
from PySide6.QtCore import *


class ReactorFlash:

    def __init__(self):

        self.alpha = 255

    def update(self):

        self.alpha -= 6

        if self.alpha < 0:
            self.alpha = 0

    def draw(self,painter):

        self.update()

        painter.save()

        painter.setBrush(
            QColor(
                255,
                255,
                255,
                self.alpha
            )
        )

        painter.setPen(Qt.NoPen)

        painter.drawEllipse(
            QPointF(0,55),
            70,
            70
        )

        painter.restore()