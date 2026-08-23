from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from gui.engine.layer import Layer


class Glow(Layer):

    def __init__(self):

        super().__init__()

        self.radius = 140

        self.color = QColor(0, 220, 255)

        self.alpha = 35

    def draw(self, painter):

        painter.setPen(Qt.NoPen)

        for i in range(12):

            a = self.alpha - i * 2

            if a < 0:
                a = 0

            painter.setBrush(
                QColor(
                    self.color.red(),
                    self.color.green(),
                    self.color.blue(),
                    a
                )
            )

            r = self.radius + i * 8

            painter.drawEllipse(
                -r,
                -r,
                r * 2,
                r * 2
            )