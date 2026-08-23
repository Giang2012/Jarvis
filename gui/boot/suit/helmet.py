from PySide6.QtGui import *
from PySide6.QtCore import *


class Helmet:

    def __init__(self):

        self.y = -260

    # =====================================

    def update(self):

        if self.y < -65:

            self.y += 5

    # =====================================

    def draw(self, painter):

        self.update()

        painter.save()

        pen = QPen(QColor(0,255,255),3)

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        # Khung ngoài
        painter.drawRoundedRect(
            QRectF(-45, self.y, 90, 110),
            18,
            18
        )

        # Mặt nạ
        painter.drawLine(-28, self.y + 55, 28, self.y + 55)
        painter.drawLine(-20, self.y + 83, 20, self.y + 83)

        # Mắt
        painter.drawLine(-22, self.y + 37, -6, self.y + 37)
        painter.drawLine(6, self.y + 37, 22, self.y + 37)

        # Cằm
        painter.drawLine(-18, self.y + 100, 18, self.y + 100)

        painter.restore()