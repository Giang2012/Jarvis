from PySide6.QtGui import *
from PySide6.QtCore import *


class SuitReactor:

    def __init__(self):

        self.radius = 0

    # ==================================

    def update(self):

        self.radius += 0.35

        if self.radius > 5:

            self.radius = 0

    # ==================================

    def draw(self, painter):

        self.update()

        painter.save()

        painter.setPen(Qt.NoPen)

        # ===============================
        # Pulse Glow
        # ===============================

        for i in range(12):

            r = 18 + self.radius + i * 5

            painter.setBrush(
                QColor(
                    0,
                    255,
                    255,
                    18
                )
            )

            painter.drawEllipse(
                QPointF(0, 55),
                r,
                r
            )

        # ===============================
        # Main Reactor
        # ===============================

        painter.setBrush(
            QColor(0, 255, 255)
        )

        painter.drawEllipse(
            QPointF(0, 55),
            18,
            18
        )

        painter.setBrush(
            QColor(255, 255, 255)
        )

        painter.drawEllipse(
            QPointF(0, 55),
            7,
            7
        )

        painter.restore()