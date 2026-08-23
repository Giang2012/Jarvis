from PySide6.QtGui import *
from PySide6.QtCore import *


class ReactorStatus:

    def __init__(self):

        self.power = 0

    def update(self):

        if self.power < 100:

            self.power += 1

    def draw(self,painter):

        self.update()

        painter.save()

        painter.setPen(
            QColor(0,255,255)
        )

        painter.setFont(
            QFont(
                "Orbitron",
                9
            )
        )

        painter.drawText(

            QRectF(

                -40,

                95,

                80,

                30

            ),

            Qt.AlignCenter,

            f"{self.power}%"

        )

        painter.restore()