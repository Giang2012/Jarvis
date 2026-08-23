from PySide6.QtGui import *
from PySide6.QtCore import *
from datetime import datetime

from gui.common.panels.base_panel import BasePanel


class CalendarPanel(BasePanel):

    def __init__(self):

        super().__init__("CALENDAR")

    # ----------------------------------

    def drawContent(self, painter, rect):

        painter.save()

        now = datetime.now()

        # Month

        painter.setPen(QColor(0,255,255))

        font = QFont("Consolas",11,QFont.Bold)

        painter.setFont(font)

        painter.drawText(
            rect.left()+20,
            rect.top()+65,
            now.strftime("%B %Y")
        )

        # Day

        font = QFont("Consolas",42,QFont.Bold)

        painter.setFont(font)

        painter.setPen(Qt.white)

        painter.drawText(
            rect.left()+18,
            rect.top()+135,
            str(now.day)
        )

        # Weekday

        font = QFont("Consolas",11)

        painter.setFont(font)

        painter.setPen(QColor(180,220,255))

        painter.drawText(
            rect.left()+22,
            rect.top()+160,
            now.strftime("%A")
        )

        painter.restore()