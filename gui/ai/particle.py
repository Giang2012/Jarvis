from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor
import math
import random
from PySide6.QtCore import Qt

class Particle:

    def __init__(self):

        self.radius = random.uniform(25, 110)
        self.angle = random.uniform(0, 360)

        self.size = random.uniform(1.5, 4)

        self.speed = random.uniform(0.2, 0.8)

        self.alpha = random.randint(60, 180)

        self.pos = QPointF()

        self.update_position()

    # --------------------------

    def update_position(self):

        rad = math.radians(self.angle)

        self.pos.setX(
            math.cos(rad) * self.radius
        )

        self.pos.setY(
            math.sin(rad) * self.radius
        )

    # --------------------------

    def update(self):

        self.angle += self.speed

        if self.angle >= 360:

            self.angle -= 360

        self.update_position()

    # --------------------------

    def draw(self, painter):

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                0,
                255,
                255,
                self.alpha
            )
        )

        painter.drawEllipse(
            self.pos,
            self.size,
            self.size
        )