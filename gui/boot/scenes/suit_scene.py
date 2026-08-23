from PySide6.QtGui import *
from PySide6.QtCore import *

from gui.boot.suit.armor_renderer_v2 import ArmorRendererV2


class SuitScene:

    def __init__(self):

        self.armor = ArmorRendererV2()

    def paint(self, painter: QPainter, rect):

        painter.save()

        painter.setRenderHint(QPainter.Antialiasing)

        painter.translate(rect.center())

        self.armor.draw(painter)

        painter.restore()


# ==========================================================
# ====================== OLD SUIT V1 ========================
# ==========================================================
#
# Giữ lại để tham khảo.
# Không chạy nữa.
#
"""
        cyan = QColor(0,255,255)

        pen = QPen(cyan,3)

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        # ================= HELMET =================

        hy=max(-250+self.t,-160)

        if self.t>0:

            painter.drawRoundedRect(
                QRectF(-45,hy,90,100),
                18,
                18
            )

            painter.drawLine(-18,hy+40,18,hy+40)

            painter.drawLine(-25,hy+60,25,hy+60)

        # ================= SHOULDERS =================

        if self.t>40:

            sy=max(260-self.t,-20)

            painter.drawLine(-90,sy,-55,0)

            painter.drawLine(90,sy,55,0)

        # ================= CHEST =================

        if self.t>80:

            cy=max(340-self.t,-10)

            painter.drawRoundedRect(
                QRectF(-60,cy,120,140),
                12,
                12
            )

            painter.drawLine(-35,cy+20,35,cy+20)

            painter.drawLine(0,cy+20,0,cy+140)

            painter.drawEllipse(
                QRectF(-15,cy+48,30,30)
            )

        # ================= WAIST =================

        if self.t>120:

            wy=max(420-self.t,135)

            painter.drawPolygon([

                QPoint(-35,wy),

                QPoint(35,wy),

                QPoint(25,wy+30),

                QPoint(-25,wy+30)

            ])

        # ================= LEFT ARM =================

        if self.t>160:

            x=max(-320+self.t,-125)

            painter.drawLine(x,25,-62,25)

            painter.drawLine(-62,25,-62,110)

            painter.drawLine(-62,110,-72,155)

        # ================= RIGHT ARM =================

        if self.t>200:

            x=min(320-self.t,125)

            painter.drawLine(62,25,x,25)

            painter.drawLine(62,25,62,110)

            painter.drawLine(62,110,72,155)

        # ================= LEFT LEG =================

        if self.t>250:

            y=min(620-self.t,270)

            painter.drawLine(-20,165,-20,y)

            painter.drawLine(-20,y,-35,y+55)

        # ================= RIGHT LEG =================

        if self.t>300:

            y=min(680-self.t,270)

            painter.drawLine(20,165,20,y)

            painter.drawLine(20,y,35,y+55)

        # ================= ARC REACTOR =================

        if self.t>360:

            for i in range(8):

                painter.setBrush(
                    QColor(
                        0,
                        255,
                        255,
                        25-i*2
                    )
                )

                painter.setPen(Qt.NoPen)

                painter.drawEllipse(
                    QPointF(0,53),
                    18+i*5,
                    18+i*5
                )

            painter.setBrush(cyan)

            painter.drawEllipse(
                QPointF(0,53),
                16,
                16
            )

            painter.setBrush(QColor(255,255,255))

            painter.drawEllipse(
                QPointF(0,53),
                6,
                6
            )

        # ================= STATUS =================

        if self.t>420:

            painter.setPen(QColor(255,255,255))

            painter.setFont(
                QFont(
                    "Orbitron",
                    18,
                    QFont.Bold
                )
            )

            painter.drawText(
                QRectF(-250,320,500,40),
                Qt.AlignCenter,
                "MARK VII READY"
            )
"""