from PySide6.QtGui import *
from PySide6.QtCore import *


class Arm:

    def __init__(self, left=True):

        self.left = left

        if left:
            self.x = -320
        else:
            self.x = 320

    # ====================================

    def update(self):

        if self.left:

            if self.x < -125:

                self.x += 6

        else:

            if self.x > 125:

                self.x -= 6

    # ====================================

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

        painter.translate(self.x,65)

        # Upper Arm
        painter.drawRoundedRect(
            -12,
            -45,
            24,
            55,
            8,
            8
        )

        # Joint
        painter.drawEllipse(
            QPointF(0,10),
            7,
            7
        )

        # Forearm
        painter.drawRoundedRect(
            -10,
            12,
            20,
            60,
            8,
            8
        )

        painter.restore()