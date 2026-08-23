import random

from PySide6.QtGui import *
from PySide6.QtCore import *


class Spark:

    def __init__(self):

        self.reset()

    # ==========================

    def reset(self):

        self.x = random.randint(-120,120)
        self.y = random.randint(-180,180)

        self.vx = random.uniform(-2.5,2.5)
        self.vy = random.uniform(-2.5,2.5)

        self.life = random.randint(18,40)

    # ==========================

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.life -= 1

        if self.life <= 0:
            self.reset()

    # ==========================

    def draw(self,painter):

        self.update()

        alpha = max(0,self.life*8)

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                0,
                255,
                255,
                alpha
            )
        )

        painter.drawEllipse(
            QPointF(self.x,self.y),
            2,
            2
        )