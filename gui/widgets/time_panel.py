from PySide6.QtGui import QColor, QFont
from datetime import datetime


class TimePanel:

    def draw(self, painter, x, y):

        now = datetime.now()

        painter.save()

        painter.setPen(
            QColor(0, 255, 255, 220)
        )

        painter.setFont(
            QFont(
                "Consolas",
                14,
                QFont.Bold
            )
        )

        painter.drawText(
            x,
            y,
            now.strftime("%H:%M:%S")
        )

        painter.setFont(
            QFont(
                "Consolas",
                8
            )
        )

        painter.setPen(
            QColor(120, 240, 255, 150)
        )

        painter.drawText(
            x,
            y + 16,
            now.strftime("%d/%m/%Y")
        )

        painter.restore()