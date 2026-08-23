from PySide6.QtCore import QRect
from gui.panels.base_panel import BasePanel
from gui.components.data_widget import DataWidget


class WeatherPanel(BasePanel):

    def __init__(self):

        super().__init__("WEATHER")

        self.widget = DataWidget()

    # ----------------------------------------

    def drawBody(self,painter,rect):

        data=[

            ("CITY","HCM",1),

            ("TEMP","30°C",0.60),

            ("HUM","72%",0.72),

            ("WIND","6km/h",0.20),

            ("RAIN","5%",0.05)

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