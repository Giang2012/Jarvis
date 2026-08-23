import math

from PySide6.QtGui import *
from PySide6.QtCore import *


class ReactorHUD:

    def __init__(self):

        self.angle = 0

    # =====================================

    def update(self):

        self.angle += 1.5

    # =====================================

    def draw(self,painter):

        self.update()

        painter.save()

        painter.translate(0,55)

        painter.rotate(self.angle)

        pen = QPen(
            QColor(0,255,255,120),
            2
        )

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        painter.drawArc(
            QRectF(-38,-38,76,76),
            0*16,
            55*16
        )

        painter.drawArc(
            QRectF(-38,-38,76,76),
            120*16,
            55*16
        )

        painter.drawArc(
            QRectF(-38,-38,76,76),
            240*16,
            55*16
        )

        painter.restore()