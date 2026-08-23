from PySide6.QtGui import *

from gui.common.panels.base_panel import BasePanel


class WeatherPanel(BasePanel):

    def __init__(self):

        super().__init__("WEATHER")

    # ----------------------------

    def drawContent(self,painter,rect):

        painter.save()

        painter.setPen(
            QColor(255,255,255)
        )

        font = QFont(
            "Consolas",
            24,
            QFont.Bold
        )

        painter.setFont(font)

        painter.drawText(
            rect.left()+20,
            rect.top()+90,
            "27°"
        )

        font = QFont(
            "Consolas",
            11
        )

        painter.setFont(font)

        painter.drawText(
            rect.left()+20,
            rect.top()+125,
            "Ho Chi Minh City"
        )

        painter.drawText(
            rect.left()+20,
            rect.top()+150,
            "Cloudy"
        )

        painter.restore()