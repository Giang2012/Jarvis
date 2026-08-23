from PySide6.QtGui import *
from PySide6.QtCore import *


class WireFrame:

    def __init__(self):

        self.alpha = 0

    # ===============================

    def update(self):

        if self.alpha < 120:
            self.alpha += 2

    # ===============================

    def draw(self, painter):

        self.update()

        pen = QPen(
            QColor(
                0,
                255,
                255,
                self.alpha
            ),
            1,
            Qt.DashLine
        )

        painter.setPen(pen)

        # Head

        painter.drawEllipse(
            QRectF(-35,-165,70,90)
        )

        # Chest

        painter.drawRoundedRect(
            QRectF(-60,-70,120,150),
            10,
            10
        )

        # Arms

        painter.drawLine(-60,-30,-120,20)
        painter.drawLine(60,-30,120,20)

        painter.drawLine(-120,20,-120,120)
        painter.drawLine(120,20,120,120)

        # Waist

        painter.drawLine(-35,80,-25,120)
        painter.drawLine(35,80,25,120)

        # Legs

        painter.drawLine(-20,120,-30,240)
        painter.drawLine(20,120,30,240)