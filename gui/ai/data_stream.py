from PySide6.QtGui import *
from PySide6.QtCore import *
import random


class DataLine:

    def __init__(self):

        self.reset()

    # ----------------------------

    def reset(self):

        self.x = random.randint(-260,260)

        self.y = random.randint(-220,220)

        self.length = random.randint(30,80)

        self.speed = random.uniform(0.6,1.5)

        self.alpha = random.randint(20,80)

    # ----------------------------

    def update(self):

        self.x += self.speed

        if self.x > 300:

            self.reset()

            self.x = -300

    # ----------------------------

    def draw(self,painter):

        self.update()

        pen = QPen(

            QColor(

                0,

                255,

                255,

                self.alpha

            ),

            1

        )

        painter.setPen(pen)

        painter.drawLine(

            self.x,

            self.y,

            self.x+self.length,

            self.y

        )


class DataStream:

    def __init__(self):

        self.lines=[

            DataLine()

            for _ in range(40)

        ]

    def draw(self,painter):

        for line in self.lines:

            line.draw(painter)