from PySide6.QtGui import *

from gui.common.panels.base_panel import BasePanel


class MusicPanel(BasePanel):

    def __init__(self):

        super().__init__("NOW PLAYING")

        self.song = "Nothing Playing"
        self.artist = "JARVIS"

    # ----------------------------------

    def drawContent(self, painter, rect):

        painter.save()

        # Album

        painter.setPen(QPen(QColor(0,255,255),2))

        painter.setBrush(QColor(25,40,60))

        painter.drawRoundedRect(
            rect.left()+20,
            rect.top()+60,
            60,
            60,
            10,
            10
        )

        painter.setPen(Qt.white)

        font = QFont("Consolas",10,QFont.Bold)

        painter.setFont(font)

        painter.drawText(
            rect.left()+95,
            rect.top()+85,
            self.song
        )

        font = QFont("Consolas",9)

        painter.setFont(font)

        painter.setPen(QColor(170,220,255))

        painter.drawText(
            rect.left()+95,
            rect.top()+108,
            self.artist
        )

        painter.restore()