from PySide6.QtGui import *
from PySide6.QtCore import *
import random


class BackgroundParticle:

    def __init__(self):

        self.x = random.randint(-900,900)

        self.y = random.randint(-500,500)

        self.size = random.randint(1,3)

        self.speed = random.uniform(0.05,0.3)

    def update(self):

        self.y += self.speed

        if self.y > 520:

            self.y = -520

    def draw(self,painter):

        self.update()

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                0,
                255,
                255,
                30
            )
        )

        painter.drawEllipse(
            QPointF(
                self.x,
                self.y
            ),
            self.size,
            self.size
        )
class LivingBackground:

    def __init__(self):

        self.particles = [

            BackgroundParticle()

            for _ in range(180)

        ]

    def draw(self,painter):

        for p in self.particles:

            p.draw(painter)