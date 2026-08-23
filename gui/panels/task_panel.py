from PySide6.QtCore import QRect
from gui.panels.base_panel import BasePanel
from gui.components.data_widget import DataWidget


class TaskPanel(BasePanel):

    def __init__(self):

        super().__init__("TASKS")

        self.widget=DataWidget()

    # ----------------------------------------

    def drawBody(self,painter,rect):

        data=[

            ("Python","80%",0.80),

            ("Jarvis","65%",0.65),

            ("Math","30%",0.30),

            ("English","50%",0.50),

            ("Unity","10%",0.10)

        ]

        body=QRect(

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