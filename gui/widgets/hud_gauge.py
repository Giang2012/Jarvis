from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QFont
)
from PySide6.QtCore import Qt


class HUDGauge(QWidget):

    def __init__(self, title="CPU"):
        super().__init__()

        self.title = title
        self.value = 0

        self.setMinimumSize(120,120)
        self.setMaximumSize(120,120)

    def setValue(self,value):

        self.value = value

        self.update()

    def paintEvent(self,event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        rect = self.rect().adjusted(
            12,
            12,
            -12,
            -12
        )

        # background ring

        pen = QPen(
            QColor(40,60,80),
            8
        )

        painter.setPen(pen)

        painter.drawEllipse(rect)

        # value ring

        color = QColor(
            0,
            255,
            255
        )

        if self.value > 80:
            color = QColor(
                255,
                120,
                50
            )

        pen = QPen(
            color,
            8
        )

        pen.setCapStyle(
            Qt.RoundCap
        )

        painter.setPen(pen)

        span = int(
            -360*16*self.value/100
        )

        painter.drawArc(
            rect,
            90*16,
            span
        )

        painter.setPen(color)

        font = QFont()

        font.setPointSize(16)

        font.setBold(True)

        painter.setFont(font)

        painter.drawText(
            rect,
            Qt.AlignCenter,
            f"{self.value}%"
        )

        painter.setPen(
            QColor(180,220,255)
        )

        font.setPointSize(10)

        font.setBold(False)

        painter.setFont(font)

        painter.drawText(
            0,
            self.height()-8,
            self.width(),
            20,
            Qt.AlignCenter,
            self.title
        )