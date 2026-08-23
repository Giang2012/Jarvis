from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
)
from PySide6.QtCore import (
    Qt,
    QTimer,
)


class HUDBackground(QWidget):

    def __init__(self, mode_manager):
        super().__init__()

        self.mode_manager = mode_manager

        self.offset = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):

        self.offset += 1

        if self.offset >= 40:
            self.offset = 0

        self.update()

    def paintEvent(self, e):

        p = QPainter(self)

        p.setRenderHint(
            QPainter.Antialiasing
        )

        p.fillRect(
            self.rect(),
            QColor(5, 8, 15)
        )

        pen = QPen(
            QColor(0, 216, 255, 22)
        )

        pen.setWidth(1)

        p.setPen(pen)

        grid = 40

        for x in range(
            self.offset,
            self.width(),
            grid
        ):
            p.drawLine(
                x,
                0,
                x,
                self.height()
            )

        for y in range(
            self.offset,
            self.height(),
            grid
        ):
            p.drawLine(
                0,
                y,
                self.width(),
                y
            )

        pen.setColor(
            QColor(0,216,255,40)
        )

        pen.setWidth(2)

        p.setPen(pen)

        p.drawRect(
            self.rect().adjusted(
                10,
                10,
                -10,
                -10
            )
        )