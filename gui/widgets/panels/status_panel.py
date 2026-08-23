from PySide6.QtGui import *


class StatusPanel:

    def draw(self,painter,w,h):

        painter.save()

        painter.setPen(
            QColor(0,255,255,120)
        )

        painter.drawLine(
            30,
            h-55,
            w-30,
            h-55
        )

        font = QFont(
            "Consolas",
            10
        )

        painter.setFont(font)

        painter.setPen(Qt.white)

        painter.drawText(
            40,
            h-25,
            "ONLINE"
        )

        painter.drawText(
            180,
            h-25,
            "MODE : STUDY"
        )

        painter.drawText(
            380,
            h-25,
            "MIC READY"
        )

        painter.drawText(
            560,
            h-25,
            "FPS : 60"
        )

        painter.restore()