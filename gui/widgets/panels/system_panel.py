from PySide6.QtGui import *
from PySide6.QtCore import *
import psutil

from gui.common.panels.base_panel import BasePanel


class SystemPanel(BasePanel):

    def __init__(self):

        super().__init__("SYSTEM")

    # -------------------------------------

    def drawContent(self, painter, rect):

        painter.save()

        font = QFont(
            "Consolas",
            10
        )

        painter.setFont(font)

        painter.setPen(
            QColor(220,240,255)
        )

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        gpu = 32
        temp = 51

        y = rect.top() + 65
        x = rect.left() + 18

        info = [

            ("CPU", cpu),
            ("RAM", ram),
            ("GPU", gpu),
            ("TEMP", temp)

        ]

        for name, value in info:

            painter.drawText(
                x,
                y,
                f"{name}"
            )

            painter.drawText(
                x + 120,
                y,
                f"{value}%"
            )

            self.drawBar(
                painter,
                x,
                y + 8,
                170,
                value
            )

            y += 55

        painter.restore()

    # -------------------------------------

    def drawBar(
        self,
        painter,
        x,
        y,
        width,
        percent
    ):

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                35,
                50,
                70
            )
        )

        painter.drawRoundedRect(
            x,
            y,
            width,
            8,
            4,
            4
        )

        color = QColor(
            0,
            255,
            255
        )

        if percent > 80:

            color = QColor(
                255,
                80,
                80
            )

        painter.setBrush(color)

        painter.drawRoundedRect(
            x,
            y,
            width * percent / 100,
            8,
            4,
            4
        )