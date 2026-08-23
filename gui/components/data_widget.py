from PySide6.QtGui import *
from PySide6.QtCore import *


class DataWidget:

    def __init__(self):

        self.fontTitle = QFont("Consolas", 9, QFont.Bold)
        self.fontValue = QFont("Consolas", 9)

    # --------------------------------------

    def draw(self, painter, rect, data):

        painter.save()

        h = 28

        y = rect.top()

        for item in data:

            key = item[0]
            value = item[1]

            painter.setPen(QColor(0, 255, 255, 180))
            painter.setFont(self.fontTitle)

            painter.drawText(

                QRect(

                    rect.left(),

                    y,

                    rect.width() // 2,

                    h

                ),

                Qt.AlignVCenter,

                key

            )

            painter.setPen(QColor(255, 255, 255))

            painter.setFont(self.fontValue)

            painter.drawText(

                QRect(

                    rect.center().x(),

                    y,

                    rect.width() // 2,

                    h

                ),

                Qt.AlignRight | Qt.AlignVCenter,

                str(value)

            )

            y += h

        painter.restore()