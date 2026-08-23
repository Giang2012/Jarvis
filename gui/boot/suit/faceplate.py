from PySide6.QtGui import *
from PySide6.QtCore import *


class FacePlate:

    def __init__(self):

        self.offset = -26

    # ==========================

    def update(self):

        if self.offset < 0:

            self.offset += 0.5

    # ==========================

    def draw(self,painter):

        self.update()

        painter.save()

        painter.setPen(
            QPen(
                QColor(0,255,255),
                2
            )
        )

        painter.setBrush(
            QColor(
                30,
                40,
                45
            )
        )

        # LEFT

        painter.drawPolygon([

            QPointF(-40,-48),

            QPointF(-5+self.offset,-48),

            QPointF(-5+self.offset,18),

            QPointF(-40,18)

        ])

        # RIGHT

        painter.drawPolygon([

            QPointF(5-self.offset,-48),

            QPointF(40,-48),

            QPointF(40,18),

            QPointF(5-self.offset,18)

        ])

        painter.restore()