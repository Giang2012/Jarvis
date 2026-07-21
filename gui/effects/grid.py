from PySide6.QtGui import QColor, QPen


class Grid:

    @staticmethod
    def draw(painter, rect, offset=0):

        painter.save()

        pen = QPen(
            QColor(
                0,
                150,
                255,
                25
            ),
            1
        )

        painter.setPen(pen)

        step = 30

        for x in range(-step, rect.width()+step, step):

            painter.drawLine(
                x + offset,
                0,
                x + offset,
                rect.height()
            )

        for y in range(-step, rect.height()+step, step):

            painter.drawLine(
                0,
                y + offset,
                rect.width(),
                y + offset
            )

        painter.restore()