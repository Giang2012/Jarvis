from PySide6.QtGui import *
from PySide6.QtCore import *


class Shoulder:

    def __init__(self, left=True):

        self.left = left

        if left:
            self.x = -260
        else:
            self.x = 260

    # ====================================

    def update(self):

        if self.left:

            if self.x < -72:

                self.x += 6

        else:

            if self.x > 72:

                self.x -= 6

    # ====================================

    def draw(self, painter):

        self.update()

        painter.save()

        painter.setPen(
            QPen(
                QColor(0,255,255),
                3
            )
        )

        painter.setBrush(Qt.NoBrush)

        painter.translate(self.x,-8)

        painter.drawEllipse(
            QRectF(
                -22,
                -18,
                44,
                36
            )
        )

        painter.drawArc(
            QRectF(
                -26,
                -22,
                52,
                44
            ),
            0,
            180*16
        )

        painter.restore()