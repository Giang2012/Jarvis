from PySide6.QtGui import *

from gui.common.panels.base_panel import BasePanel


class AIStatusPanel(BasePanel):

    def __init__(self):

        super().__init__("AI STATUS")

        self.state = "ONLINE"
        self.model = "Gemini"
        self.voice = "READY"

    # ----------------------------------

    def drawContent(self, painter, rect):

        painter.save()

        font = QFont("Consolas",10)

        painter.setFont(font)

        painter.setPen(Qt.white)

        y = rect.top()+65

        painter.drawText(
            rect.left()+20,
            y,
            f"State : {self.state}"
        )

        painter.drawText(
            rect.left()+20,
            y+30,
            f"Model : {self.model}"
        )

        painter.drawText(
            rect.left()+20,
            y+60,
            f"Voice : {self.voice}"
        )

        painter.restore()