from PySide6.QtGui import QColor, QPen
from gui.engine.layer import Layer


class Scanline(Layer):

    def __init__(self):

        super().__init__()

        self.offset = 0

    def update(self):

        self.offset += 1

        if self.offset > 40:
            self.offset = 0

    def draw(self, painter):

        pen = QPen(
            QColor(
                0,
                255,
                255,
                18
            )
        )

        painter.setPen(pen)

        w = painter.viewport().width()

        h = painter.viewport().height()

        y = self.offset

        while y < h:

            painter.drawLine(
                0,
                y,
                w,
                y
            )

            y += 4