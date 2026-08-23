from PySide6.QtGui import *
from PySide6.QtCore import *
from datetime import datetime


class StatusBar:

    def paint(self, painter, rect):

        painter.save()

        painter.setPen(QColor(0, 255, 255))

        painter.setFont(QFont("Consolas", 10))

        painter.drawText(

            rect,

            Qt.AlignCenter,

            datetime.now().strftime("%H:%M:%S")

        )

        painter.restore()