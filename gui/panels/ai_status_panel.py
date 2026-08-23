from PySide6.QtCore import QRect

from gui.panels.base_panel import BasePanel
from gui.components.data_widget import DataWidget


class AIStatusPanel(BasePanel):

    def __init__(self):

        super().__init__("AI STATUS")

        self.widget = DataWidget()

    def drawBody(self, painter, rect):

        body = QRect(

            rect.left() + 20,

            rect.top() + 65,

            rect.width() - 40,

            rect.height() - 95

        )

        self.widget.draw(

            painter,

            body,

            [

                ("MODE", "IDLE", 0),

                ("STATE", "READY", 0),

                ("CPU", "0%", 0)

            ]

        )