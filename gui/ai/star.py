from PySide6.QtGui import *
from PySide6.QtCore import *
import random


class Star:

    def __init__(self):

        self.x=random.randint(-260,260)

        self.y=random.randint(-260,260)

        self.size=random.randint(1,3)

        self.alpha=random.randint(80,255)

        self.timer=random.randint(0,300)

    def update(self):

        self.timer+=1

        if self.timer>300:

            self.timer=0

            self.alpha=random.randint(80,255)

    def draw(self,painter):

        self.update()

        painter.setPen(Qt.NoPen)

        painter.setBrush(

            QColor(

                255,

                255,

                255,

                self.alpha

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


class StarField:

    def __init__(self):

        self.stars=[

            Star()

            for _ in range(80)

        ]

    def draw(self,painter):

        for s in self.stars:

            s.draw(painter)