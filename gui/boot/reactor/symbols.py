from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPen, QFont
from math import cos, sin, radians


class ReactorSymbols:

    def __init__(self):

        self.radius = 95
        self.angle = 0

    def update(self):

        self.angle += 0.6

    def draw(self, painter):

        self.update()

        painter.save()

        painter.setPen(
            QPen(
                QColor(0, 255, 255, 180)
            )
        )

        painter.setFont(
            QFont(
                "Consolas",
                8
            )
        )

        symbols = [
            "◉", "◈", "△", "◇",
            "◌", "⬢", "✦", "◎"
        ]

        for i, s in enumerate(symbols):

            a = radians(i * 45 + self.angle)

            x = cos(a) * self.radius
            y = sin(a) * self.radius

            painter.drawText(
                QPointF(x - 4, y + 4),
                s
            )

        painter.restore()