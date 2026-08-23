from PySide6.QtGui import *
from PySide6.QtCore import *


class PanelTitle:

    def draw(self, painter, rect, title):

        painter.save()

        painter.setPen(
            QColor(0,255,255)
        )

        font = QFont(
            "Consolas",
            10,
            QFont.Bold
        )

        painter.setFont(font)

        painter.drawText(
            rect.adjusted(
                18,
                18,
                -18,
                0
            ),
            title
        )

        painter.setPen(
            QColor(0,255,255,80)
        )

        painter.drawLine(
            rect.left()+15,
            rect.top()+38,
            rect.right()-15,
            rect.top()+38
        )

        painter.restore()