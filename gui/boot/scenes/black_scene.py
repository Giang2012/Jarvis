from PySide6.QtGui import QColor


class BlackScene:

    def update(self):
        pass

    def paint(self, painter, rect):

        painter.fillRect(
            rect,
            QColor(0, 0, 0)
        )