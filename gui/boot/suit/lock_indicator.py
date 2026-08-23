from PySide6.QtGui import *
from PySide6.QtCore import *


class LockIndicator:

    def __init__(self, x, y, text):

        self.x = x
        self.y = y
        self.text = text

        self.alpha = 0

    # ============================

    def update(self):

        if self.alpha < 255:
            self.alpha += 8

    # ============================

    def draw(self, painter):

        self.update()

        c = QColor(0,255,255,self.alpha)

        painter.setPen(QPen(c,1))

        painter.setFont(
            QFont("Consolas",9)
        )

        painter.drawLine(
            self.x,
            self.y,
            self.x+45,
            self.y
        )

        painter.drawText(
            self.x+50,
            self.y+4,
            self.text
        )

        painter.setPen(
            QColor(120,255,120,self.alpha)
        )

        painter.drawText(
            self.x+50,
            self.y+18,
            "LOCKED ✓"
        )