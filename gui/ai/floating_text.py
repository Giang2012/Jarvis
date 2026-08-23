from PySide6.QtGui import *
from PySide6.QtCore import *
import random


class FloatingText:

    WORDS = [

        "READY",

        "SEARCH",

        "ONLINE",

        "SYNC",

        "AI",

        "SYSTEM",

        "VOICE",

        "DATA"

    ]

    def __init__(self):

        self.reset()

    def reset(self):

        self.text = random.choice(self.WORDS)

        self.x = random.randint(-120,120)

        self.y = random.randint(-120,120)

        self.alpha = 0

        self.life = 0

    def update(self):

        self.life += 1

        self.alpha = min(120,self.life*4)

        self.y -= 0.25

        if self.life > 180:

            self.reset()

    def draw(self,painter):

        self.update()

        painter.save()

        painter.setPen(

            QColor(

                0,

                255,

                255,

                self.alpha

            )

        )

        painter.setFont(

            QFont(

                "Consolas",

                8

            )

        )

        painter.drawText(

            QPointF(

                self.x,

                self.y

            ),

            self.text

        )

        painter.restore()