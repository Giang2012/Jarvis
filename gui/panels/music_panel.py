from PySide6.QtCore import QRect

from gui.panels.base_panel import BasePanel

from gui.components.data_widget import DataWidget


class MusicPanel(BasePanel):

    def __init__(self):

        super().__init__("MUSIC")

        self.widget = DataWidget()

    def drawBody(self,painter,rect):

        body = QRect(

            rect.left()+20,

            rect.top()+65,

            rect.width()-40,

            rect.height()-95

        )

        self.widget.draw(

            painter,

            body,

            [

                ("SONG","None",0),

                ("ARTIST","Unknown",0),

                ("STATUS","Idle",0)

            ]

        )