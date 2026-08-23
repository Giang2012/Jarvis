from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QPolygonF
)
from PySide6.QtCore import (
    Qt,
    QPointF,
    QTimer
)
import math
class IronmanSuit(QWidget):

    def __init__(self,parent=None):

        super().__init__(parent)

        self.scan = -500

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(16)
    def animate(self):

        self.scan += 4

        if self.scan > self.height()+200:

            self.scan = -200

        self.update()
    def paintEvent(self,e):

        p = QPainter(self)

        p.setRenderHint(
            QPainter.Antialiasing
        )

        p.translate(

            self.width()/2,

            self.height()/2

        )

        self.drawHelmet(p)

        self.drawChest(p)

        self.drawShoulders(p)

        self.drawScan(p)
    def drawHelmet(self,p):

        pen = QPen(

            QColor(

                0,

                220,

                255

            )

        )

        pen.setWidth(3)

        p.setPen(pen)

        p.setBrush(Qt.NoBrush)

        poly = QPolygonF([

            QPointF(-45,-180),

            QPointF(-28,-220),

            QPointF(28,-220),

            QPointF(45,-180),

            QPointF(35,-130),

            QPointF(-35,-130)

        ])

        p.drawPolygon(poly)

        p.drawLine(-20,-165,20,-165)

        p.drawLine(0,-220,0,-130)
    def drawChest(self,p):

        pen = QPen(

            QColor(

                0,

                220,

                255

            )

        )

        pen.setWidth(3)

        p.setPen(pen)

        p.drawRoundedRect(

            -80,

            -90,

            160,

            170,

            12,

            12

        )
    def drawShoulders(self,p):

        pen = QPen(

            QColor(

                0,

                220,

                255

            )

        )

        pen.setWidth(3)

        p.setPen(pen)

        p.drawEllipse(

            -130,

            -70,

            45,

            45

        )

        p.drawEllipse(

            85,

            -70,

            45,

            45

        )
    def drawScan(self,p):

        pen = QPen(

            QColor(

                0,

                255,

                255,

                180

            )

        )

        pen.setWidth(2)

        p.setPen(pen)

        y = self.scan-self.height()/2

        p.drawLine(

            -300,

            y,

            300,

            y

        )