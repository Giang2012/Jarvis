from PySide6.QtGui import *
from PySide6.QtCore import *


class HologramGlow:

    @staticmethod
    def draw(painter, rect):

        painter.save()

        color = QColor(0,255,255,40)

        painter.setPen(Qt.NoPen)

        painter.setBrush(color)

        painter.drawRoundedRect(

            rect.adjusted(-5,-5,5,5),

            12,

            12

        )

        painter.restore()