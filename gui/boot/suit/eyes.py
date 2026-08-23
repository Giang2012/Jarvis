from PySide6.QtGui import *
from PySide6.QtCore import *


class Eyes:

    def __init__(self):

        self.alpha = 0

    def update(self):

        if self.alpha < 255:
            self.alpha += 5

    def draw(self,painter):

        self.update()

        painter.save()

        for i in range(8):

            painter.setBrush(
                QColor(
                    0,
                    255,
                    255,
                    20-i*2
                )
            )

            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                QPointF(-15,-122),
                4+i,
                2+i*0.4
            )

            painter.drawEllipse(
                QPointF(15,-122),
                4+i,
                2+i*0.4
            )

        painter.setBrush(
            QColor(
                255,
                255,
                255
            )
        )

        painter.drawEllipse(
            QPointF(-15,-122),
            4,
            2
        )

        painter.drawEllipse(
            QPointF(15,-122),
            4,
            2
        )

        painter.restore()