from PySide6.QtGui import QColor, QPen


class CornerHUD:

    @staticmethod
    def draw(painter, rect):

        painter.save()

        pen = QPen(
            QColor(
                0,
                255,
                255
            ),
            3
        )

        painter.setPen(pen)

        l = 35

        w = rect.width()
        h = rect.height()

        # Top Left
        painter.drawLine(0, 0, l, 0)
        painter.drawLine(0, 0, 0, l)

        # Top Right
        painter.drawLine(w-l, 0, w, 0)
        painter.drawLine(w, 0, w, l)

        # Bottom Left
        painter.drawLine(0, h-l, 0, h)
        painter.drawLine(0, h, l, h)

        # Bottom Right
        painter.drawLine(w-l, h, w, h)
        painter.drawLine(w, h-l, w, h)

        painter.restore()