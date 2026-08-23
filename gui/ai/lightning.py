from PySide6.QtGui import *
from PySide6.QtCore import *

import random


class Lightning:

    def __init__(self):

        self.timer=0

    def draw(self,painter):

        self.timer+=1

        if self.timer<8:

            return

        self.timer=0

        pen=QPen(
            QColor(0,255,255,140),
            2
        )

        painter.setPen(pen)

        x=0
        y=0

        for i in range(8):

            nx=x+random.randint(-15,15)
            ny=y-random.randint(8,20)

            painter.drawLine(
                x,
                y,
                nx,
                ny
            )

            x=nx
            y=ny