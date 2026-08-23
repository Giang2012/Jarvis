from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class GlassReflection:

    def __init__(self):

        self.time = 0

    # --------------------------

    def update(self):

        self.time += 0.03

    # --------------------------

    def draw(self, painter):

        self.update()

        painter.save()

        painter.rotate(-25)

        x = math.sin(self.time) * 220

        gradient = QLinearGradient(
            x - 120,
            -250,
            x + 120,
            250
        )

        gradient.setColorAt(
            0,
            QColor(255,255,255,0)
        )

        gradient.setColorAt(
            0.5,
            QColor(255,255,255,45)
        )

        gradient.setColorAt(
            1,
            QColor(255,255,255,0)
        )

        painter.setPen(Qt.NoPen)

        painter.setBrush(gradient)

        painter.drawRoundedRect(
            QRectF(
                -220,
                -220,
                440,
                440
            ),
            220,
            220
        )

        painter.restore()