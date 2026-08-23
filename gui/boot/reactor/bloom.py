from PySide6.QtGui import QColor
from PySide6.QtCore import QPointF
from PySide6.QtCore import Qt

class ReactorBloom:

    def __init__(self):

        self.radius = 120

    def draw(self, painter):

        painter.save()

        painter.setPen(Qt.NoPen)

        for i in range(12):

            alpha = max(0, 22 - i)

            painter.setBrush(
                QColor(
                    0,
                    255,
                    255,
                    alpha
                )
            )

            r = self.radius + i * 10

            painter.drawEllipse(
                QPointF(0, 0),
                r,
                r
            )

        painter.restore()