import random
import math

from PySide6.QtGui import (
    QColor,
    QPen,
)


class ElectricBolt:

    def __init__(self):

        self.points = []

        self.life = 0

        self.randomize()

    # ----------------------------

    def randomize(self):

        self.points.clear()

        radius = random.randint(45, 80)

        angle = random.random() * math.pi * 2

        for i in range(7):

            r = radius + random.randint(-8, 8)

            a = angle + random.uniform(-0.4, 0.4)

            x = math.cos(a) * r

            y = math.sin(a) * r

            self.points.append((x, y))

            radius += random.randint(-5, 5)
            angle += random.uniform(-0.3, 0.3)

        self.life = random.randint(4, 10)

    # ----------------------------

    def update(self):

        self.life -= 1

        if self.life <= 0:

            self.randomize()

    # ----------------------------

    def draw(self, painter):

        pen = QPen(

            QColor(

                120,

                255,

                255,

                200

            )

        )

        pen.setWidth(2)

        painter.setPen(pen)

        for i in range(len(self.points) - 1):

            x1, y1 = self.points[i]

            x2, y2 = self.points[i + 1]

            painter.drawLine(

                int(x1),
                int(y1),

                int(x2),
                int(y2)

            )