from PySide6.QtGui import *
from PySide6.QtCore import *
import math


class Reactor:

    def __init__(self):

        self.time = 0
        self.state = 0

    # --------------------------

    def setState(self, state):

        self.state = state

    # --------------------------

    def update(self):

        if self.state == 0:          # IDLE
            speed = 0.08

        elif self.state == 1:        # LISTENING
            speed = 0.18

        elif self.state == 2:        # THINKING
            speed = 0.25

        elif self.state == 3:        # SPEAKING
            speed = 0.35

        else:                        # SLEEP
            speed = 0.03

        self.time += speed

    # --------------------------

    def draw(self, painter):

        self.update()

        painter.save()

        scale = 1 + abs(math.sin(self.time)) * 0.08

        painter.scale(scale, scale)

        painter.setPen(Qt.NoPen)

        # Glow
        for i in range(8):

            painter.setBrush(
                QColor(
                    0,
                    255,
                    255,
                    18
                )
            )

            painter.drawEllipse(
                QPointF(0,0),
                18+i*6,
                18+i*6
            )

        # Reactor
        painter.setBrush(
            QColor(
                0,
                255,
                255
            )
        )

        painter.drawEllipse(
            QPointF(0,0),
            20,
            20
        )

        # Core
        painter.setBrush(
            QColor(
                255,
                255,
                255
            )
        )

        painter.drawEllipse(
            QPointF(0,0),
            8,
            8
        )

        painter.restore()