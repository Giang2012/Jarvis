from PySide6.QtGui import *

from gui.common.panels.base_panel import BasePanel


class TaskPanel(BasePanel):

    def __init__(self):

        super().__init__("TASKS")

        self.tasks = [

            ("Finish Dashboard",True),

            ("Voice Engine",False),

            ("Gemini API",False),

            ("Wake Word",False)

        ]

    # ---------------------------------

    def drawContent(self,painter,rect):

        painter.save()

        font = QFont("Consolas",10)

        painter.setFont(font)

        y = rect.top()+65

        for task,done in self.tasks:

            color = QColor(0,255,120) if done else QColor(255,180,80)

            painter.setBrush(color)

            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                rect.left()+18,
                y-7,
                8,
                8
            )

            painter.setPen(Qt.white)

            painter.drawText(
                rect.left()+35,
                y,
                task
            )

            y += 30

        painter.restore()