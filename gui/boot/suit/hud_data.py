from PySide6.QtGui import *
from PySide6.QtCore import *


class HUDData:

    def __init__(self):

        self.alpha = 0

    # =============================

    def update(self):

        if self.alpha < 255:

            self.alpha += 3

    # =============================

    def draw(self,painter):

        self.update()

        c = QColor(0,255,255,self.alpha)

        painter.setPen(QPen(c,1))

        painter.setFont(
            QFont(
                "Consolas",
                10
            )
        )

        # ---------------- LEFT ----------------

        painter.drawLine(-240,-90,-95,-90)
        painter.drawLine(-240,-30,-60,-30)
        painter.drawLine(-240,60,-15,55)

        painter.drawText(
            QRectF(-390,-115,130,40),
            Qt.AlignRight,
            "MARK VII"
        )

        painter.drawText(
            QRectF(-390,-55,130,40),
            Qt.AlignRight,
            "POWER\n98%"
        )

        painter.drawText(
            QRectF(-390,35,130,40),
            Qt.AlignRight,
            "REACTOR\nONLINE"
        )

        # ---------------- RIGHT ----------------

        painter.drawLine(95,-90,240,-90)
        painter.drawLine(60,-30,240,-30)
        painter.drawLine(15,55,240,55)

        painter.drawText(
            QRectF(260,-115,130,40),
            Qt.AlignLeft,
            "AI CORE"
        )

        painter.drawText(
            QRectF(260,-55,130,40),
            Qt.AlignLeft,
            "CONNECTED"
        )

        painter.drawText(
            QRectF(260,35,130,40),
            Qt.AlignLeft,
            "SYSTEM READY"
        )