from PySide6.QtGui import *
from PySide6.QtCore import *


class HologramShadow:

    @staticmethod
    def draw(painter, rect):

        painter.save()

        painter.setPen(Qt.NoPen)

        painter.setBrush(

            QColor(

                0,

                0,

                0,

                60

            )

        )

        painter.drawRoundedRect(

            rect.adjusted(

                6,

                6,

                6,

                6

            ),

            10,

            10

        )

        painter.restore()