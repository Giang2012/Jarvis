from PySide6.QtGui import *


class GlassPanel:

    @staticmethod
    def paint(painter, rect):

        painter.save()

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(15, 20, 30, 120)
        )

        painter.drawRoundedRect(
            rect,
            18,
            18
        )

        painter.setPen(
            QPen(
                QColor(0,255,255,70),
                1
            )
        )

        painter.drawRoundedRect(
            rect.adjusted(0,0,-1,-1),
            18,
            18
        )

        painter.restore()