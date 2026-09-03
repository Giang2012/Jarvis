from PySide6.QtGui import QColor


class Flash:

    def __init__(self):

        self.alpha = 0

    # ========================

    def trigger(self):

        self.alpha = 180

    # ========================

    def update(self):

        if self.alpha > 0:

            self.alpha -= 8

            if self.alpha < 0:

                self.alpha = 0

    # ========================

    def draw(self, painter, rect):

        self.update()

        if self.alpha == 0:

            return

        painter.fillRect(

            rect,

            QColor(
                255,
                255,
                255,
                self.alpha
            )
        )