from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import QRect
from PySide6.QtCore import Qt

class HologramPanel:

    def __init__(self):

        self.scanOffset = 0

        self.scanSpeed = 2

    # --------------------------------

    def update(self):

        self.scanOffset += self.scanSpeed

        if self.scanOffset > 10000:

            self.scanOffset = 0

    # --------------------------------

    def paint(self, painter, rect: QRect):

        painter.save()

        painter.setPen(Qt.NoPen)

        # Scan Line

        y = rect.top() + (self.scanOffset % max(1, rect.height()))

        painter.fillRect(

            QRect(

                rect.left(),

                y,

                rect.width(),

                3

            ),

            QColor(

                0,

                255,

                255,

                35

            )

        )

        painter.restore()