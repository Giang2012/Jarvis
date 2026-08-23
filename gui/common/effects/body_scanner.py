from PySide6.QtGui import *
from PySide6.QtCore import *


class BodyScanner:

    def __init__(self):

        self.y = -230

    # =======================

    def update(self):

        self.y += 4

        if self.y > 240:

            self.y = -230

    # =======================

    def draw(self, painter):

        self.update()

        # Glow

        gradient = QLinearGradient(

            0,
            self.y - 18,

            0,
            self.y + 18

        )

        gradient.setColorAt(
            0,
            QColor(0,255,255,0)
        )

        gradient.setColorAt(
            0.5,
            QColor(0,255,255,150)
        )

        gradient.setColorAt(
            1,
            QColor(0,255,255,0)
        )

        painter.fillRect(

            QRectF(
                -180,
                self.y-18,
                360,
                36
            ),

            gradient

        )

        # Line

        painter.setPen(
            QPen(
                QColor(255,255,255,180),
                1
            )
        )

        painter.drawLine(

            -170,
            self.y,

            170,
            self.y

        )