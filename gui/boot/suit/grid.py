from PySide6.QtGui import *
from PySide6.QtCore import *


class HologramGrid:

    def __init__(self):

        self.offset = 0

    # ====================================

    def update(self):

        self.offset += 1

        if self.offset > 20:

            self.offset = 0

    # ====================================

    def draw(self, painter):

        self.update()

        painter.save()

        pen = QPen(
            QColor(0,255,255,35),
            1
        )

        painter.setPen(pen)

        # Horizontal

        y = -220 + self.offset

        while y < 260:

            painter.drawLine(
                -180,
                y,
                180,
                y
            )

            y += 20

        # Vertical

        x = -180 + self.offset

        while x < 180:

            painter.drawLine(
                x,
                -220,
                x,
                260
            )

            x += 20

        painter.restore()