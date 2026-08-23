from PySide6.QtGui import *
from PySide6.QtCore import *


class LockEffect:

    def __init__(self):

        self.alpha = 255

        self.scale = 0

    # ===============================

    def update(self):

        if self.alpha > 0:

            self.alpha -= 4

        if self.scale < 1:

            self.scale += 0.03

    # ===============================

    def draw(self,painter,x,y,text):

        self.update()

        painter.save()

        painter.translate(x,y)

        painter.scale(self.scale,self.scale)

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
                "Orbitron",
                10,
                QFont.Bold
            )
        )

        painter.drawText(
            QRectF(
                -50,
                -10,
                100,
                20
            ),
            Qt.AlignCenter,
            f"{text} ✓"
        )

        painter.restore()