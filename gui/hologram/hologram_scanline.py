from PySide6.QtGui import *
from PySide6.QtCore import *


class HologramScanline:

    def __init__(self):

        self.offset = 0

    # --------------------------

    def update(self):

        self.offset += 1

        if self.offset > 8:

            self.offset = 0

    # --------------------------

    def draw(self, painter, rect):

        self.update()

        painter.save()

        pen = QPen(QColor(0,255,255,18))

        painter.setPen(pen)

        y = rect.top() + self.offset

        while y < rect.bottom():

            painter.drawLine(

                rect.left(),

                y,

                rect.right(),

                y

            )

            y += 8

        painter.restore()