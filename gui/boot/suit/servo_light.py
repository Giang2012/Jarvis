from PySide6.QtGui import *
from PySide6.QtCore import *


class ServoLight:

    def __init__(self):

        self.y = -220

    # =============================

    def update(self):

        self.y += 6

        if self.y > 260:

            self.y = -220

    # =============================

    def draw(self,painter):

        self.update()

        painter.save()

        gradient = QLinearGradient(
            0,
            self.y-30,
            0,
            self.y+30
        )

        gradient.setColorAt(
            0,
            QColor(0,255,255,0)
        )

        gradient.setColorAt(
            0.5,
            QColor(0,255,255,160)
        )

        gradient.setColorAt(
            1,
            QColor(0,255,255,0)
        )

        painter.fillRect(

            QRectF(
                -160,
                self.y,
                320,
                12
            ),

            gradient

        )

        painter.restore()