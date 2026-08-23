from PySide6.QtCore import QRect
from gui.panels.base_panel import BasePanel
from gui.components.data_widget import DataWidget


class CalendarPanel(BasePanel):

    def __init__(self):

        super().__init__("CALENDAR")

        self.widget=DataWidget()

    # ----------------------------------------

    def drawBody(self,painter,rect):

        data=[

            ("DAY","Monday",1),

            ("DATE","02 Aug",1),

            ("EVENT","Meeting",0.50),

            ("NEXT","Coding",0.70),

            ("TIME","14:30",1)

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