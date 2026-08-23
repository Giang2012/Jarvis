import random
from PySide6.QtGui import *
from PySide6.QtCore import *


class DigitalCode:

    def __init__(self):

        self.lines = []

        self.generate()

    # =================================

    def generate(self):

        self.lines.clear()

        for _ in range(16):

            s = ""

            for _ in range(18):

                s += random.choice("01")

            self.lines.append(s)

    # =================================

    def update(self):

        if random.randint(0,4)==0:

            self.generate()

    # =================================

    def draw(self,painter):

        self.update()

        painter.save()

        painter.setPen(
            QColor(0,255,255,70)
        )

        painter.setFont(
            QFont(
                "Consolas",
                8
            )
        )

        y = -170

        for txt in self.lines:

            painter.drawText(
                -340,
                y,
                txt
            )

            painter.drawText(
                220,
                y,
                txt
            )

            y += 18

        painter.restore()