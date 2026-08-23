from PySide6.QtGui import QColor


class FadeScene:

    def __init__(self):

        self.alpha = 0

    # -----------------------------

    def update(self):

        if self.alpha < 255:
            self.alpha += 3

    # -----------------------------

    def paint(self, painter, rect):

        self.update()

        painter.fillRect(
            rect,
            QColor(
                0,
                0,
                0,
                self.alpha
            )
        )