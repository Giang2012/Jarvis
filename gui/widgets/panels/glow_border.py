from PySide6.QtGui import *
from PySide6.QtCore import *


class GlowBorder:

    def draw(self, painter, rect):

        painter.save()

        for i in range(6):

            color = QColor(
                0,
                255,
                255,
                12 - i * 2
            )

            pen = QPen(
                color,
                8 - i
            )

            painter.setPen(pen)

            painter.setBrush(Qt.NoBrush)

            painter.drawRoundedRect(
                rect,
                20,
                20
            )

        painter.restore()