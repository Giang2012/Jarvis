from PySide6.QtGui import *
from PySide6.QtCore import *


class Chest:

    def __init__(self):

        self.y = 320

    # ======================================

    def update(self):

        if self.y > -75:

            self.y -= 5

    # ======================================

    def draw(self, painter):

        self.update()

        painter.save()

        pen = QPen(QColor(0,255,255),3)

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        # Upper Chest

        painter.drawPolygon([

            QPointF(-75,self.y+35),

            QPointF(-45,self.y),

            QPointF(45,self.y),

            QPointF(75,self.y+35),

            QPointF(60,self.y+100),

            QPointF(-60,self.y+100)

        ])

        # Lower Chest

        painter.drawPolygon([

            QPointF(-55,self.y+100),

            QPointF(55,self.y+100),

            QPointF(35,self.y+195),

            QPointF(-35,self.y+195)

        ])

        # Reactor Housing

        painter.drawEllipse(

            QPointF(0,self.y+100),

            28,

            28

        )

        # Armor Lines

        painter.drawLine(

            0,

            self.y,

            0,

            self.y+195

        )

        painter.drawLine(

            -40,

            self.y+55,

            40,

            self.y+55

        )

        painter.drawLine(

            -25,

            self.y+145,

            25,

            self.y+145

        )

        painter.restore()