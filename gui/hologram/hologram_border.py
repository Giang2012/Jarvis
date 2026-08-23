from PySide6.QtGui import *
from PySide6.QtCore import *


class HologramBorder:

    @staticmethod
    def draw(painter, rect):

        painter.save()

        pen = QPen(

            QColor(0,255,255)

        )

        pen.setWidth(2)

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        painter.drawRoundedRect(

            rect,

            8,

            8

        )

        painter.restore()