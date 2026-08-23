from PySide6.QtCore import QRect
from gui.panels.base_panel import BasePanel
from gui.components.data_widget import DataWidget


class SystemPanel(BasePanel):

    def __init__(self):

        super().__init__("SYSTEM")

        self.widget = DataWidget()

    # ------------------------------------------------

    def drawBody(self,painter,rect):

        data = [

        ("CPU","12%",0.12),

        ("RAM","4.8GB",0.48),

        ("GPU","35%",0.35),

        ("TEMP","42°C",0.42),

        ("NET","ONLINE",1)

        ]

        body = QRect(

            rect.left()+20,

            rect.top()+65,

            rect.width()-40,

            rect.height()-95

        )

        self.widget.draw(

            painter,

            body,

            data

        )