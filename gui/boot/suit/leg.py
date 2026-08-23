from PySide6.QtGui import *
from PySide6.QtCore import *


class Leg:

    def __init__(self, left=True):

        self.left = left

        self.y = 520

    # ===================================

    def update(self):

        if self.y > 185:

            self.y -= 6

    # ===================================

    def draw(self, painter):

        self.update()

        painter.save()

        painter.setPen(
            QPen(
                QColor(0,255,255),
                3
            )
        )

        painter.setBrush(Qt.NoBrush)

        x = -28 if self.left else 28

        painter.translate(x, self.y)

        # Upper Leg
        painter.drawRoundedRect(
            -12,
            -10,
            24,
            70,
            8,
            8
        )

        # Lower Leg
        painter.drawRoundedRect(
            -10,
            62,
            20,
            62,
            8,
            8
        )

        # Foot
        painter.drawRoundedRect(
            -16,
            122,
            32,
            14,
            6,
            6
        )

        painter.restore()