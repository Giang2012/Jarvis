from PySide6.QtWidgets import QWidget
from PySide6.QtCore import (
    QTimer,
    Qt
)

from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QPolygonF
)

from PySide6.QtCore import QPointF

import math
class SuitBuilder(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.progress = 0
        import random

        self.particles = []

        for _ in range(120):

            self.particles.append({

                "x": random.randint(-220,220),

                "y": random.randint(-220,220),

                "speed": random.uniform(1.5,4),

                "size": random.randint(2,5)

            })

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(16)
    # ====================

    def animate(self):

        if self.progress < 1000:

            self.progress += 2
        for p in self.particles:

            p["y"] += p["speed"]

            if p["y"] > 260:

                p["y"] = -260

                p["x"] = random.randint(-220,220)
        self.update()
    # ====================

    def paintEvent(self, e):

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

        self.drawLeftShoulder(p)

        self.drawRightShoulder(p)

        self.drawLeftArm(p)

        self.drawRightArm(p)

        self.drawLegs(p)

        self.drawChestReactor(p)

        self.drawEyes(p)

        self.drawScan(p)
        p.end()
    # ====================

    def drawHelmet(self,p):

        if self.progress < 120:
            return

        p.save()

        offset = max(
            0,
            140 - self.progress
        )

        p.translate(
            0,
            -offset
        )

        pen = QPen(
            QColor(
                0,
                230,
                255
            )
        )

        pen.setWidth(3)

        p.setPen(pen)

        pts = QPolygonF([

            QPointF(-40,-60),

            QPointF(40,-60),

            QPointF(55,0),

            QPointF(0,55),

            QPointF(-55,0)

        ])

        p.drawPolygon(
            pts
        )

        p.restore()
    # ====================

    def drawChest(self,p):

        if self.progress < 240:
            return

        p.save()

        offset=max(
            0,
            170-self.progress
        )

        p.translate(
            0,
            -offset
        )

        pen=QPen(
            QColor(
                0,
                230,
                255
            )
        )

        pen.setWidth(3)

        p.setPen(pen)

        p.drawRoundedRect(

            -60,

            20,

            120,

            120,

            10,

            10

        )

        p.restore()
    # ====================

    def drawLeftShoulder(self,p):

        if self.progress < 320:
            return

        p.save()

        offset=max(
            0,
            220-self.progress
        )

        p.translate(
            -75-offset,
            30
        )

        pen=QPen(
            QColor(
                0,
                230,
                255
            )
        )

        pen.setWidth(3)

        p.setPen(pen)

        p.drawEllipse(
            -20,
            -20,
            40,
            40
        )

        p.restore()
    # ====================

    def drawRightShoulder(self,p):

        if self.progress < 400:
            return

        p.save()

        offset=max(
            0,
            220-self.progress
        )

        p.translate(
            75+offset,
            30
        )

        pen=QPen(
            QColor(
                0,
                230,
                255
            )
        )

        pen.setWidth(3)

        p.setPen(pen)

        p.drawEllipse(
            -20,
            -20,
            40,
            40
        )

        p.restore()
    # ====================

    def drawLeftArm(self,p):

        if self.progress < 500:
            return

        p.save()

        offset=max(
            0,
            260-self.progress
        )

        p.translate(
            -100-offset,
            70
        )

        pen=QPen(
            QColor(
                0,
                220,
                255
            )
        )

        pen.setWidth(3)

        p.setPen(pen)

        p.drawLine(
            0,
            0,
            0,
            110
        )

        p.restore()
    # ====================

    def drawRightArm(self,p):

        if self.progress < 580:
            return

        p.save()

        offset=max(
            0,
            260-self.progress
        )

        p.translate(
            100+offset,
            70
        )

        pen=QPen(
            QColor(
                0,
                220,
                255
            )
        )

        pen.setWidth(3)

        p.setPen(pen)

        p.drawLine(
            0,
            0,
            0,
            110
        )

        p.restore()
    # ====================

    def drawLegs(self,p):

        if self.progress < 680:
            return

        p.save()

        offset=max(
            0,
            320-self.progress
        )

        pen=QPen(
            QColor(
                0,
                220,
                255
            )
        )

        pen.setWidth(3)

        p.setPen(pen)

        # LEFT

        p.drawLine(
            -25,
            140-offset,
            -25,
            250
        )

        # RIGHT

        p.drawLine(
            25,
            140-offset,
            25,
            250
        )

        p.restore()
    # ====================

    def drawChestReactor(self,p):

        if self.progress < 760:
            return

        p.save()

        pulse=(
            math.sin(
                self.progress/20
            )+1
        )/2

        size=18+pulse*3

        p.setPen(Qt.NoPen)

        p.setBrush(
            QColor(
                180,
                255,
                255
            )
        )

        p.drawEllipse(
            -size,
            58-size,
            size*2,
            size*2
        )

        p.restore()
    # ====================

    def drawEyes(self,p):

        if self.progress < 840:
            return

        p.save()

        p.setPen(Qt.NoPen)

        p.setBrush(
            QColor(
                200,
                255,
                255
            )
        )

        p.drawRoundedRect(
            -26,
            -20,
            18,
            5,
            2,
            2
        )

        p.drawRoundedRect(
            8,
            -20,
            18,
            5,
            2,
            2
        )

        p.restore()
    # ====================

    def drawScan(self,p):

        if self.progress < 920:
            return

        y=(
            self.progress*3
        )%320-160

        pen=QPen(
            QColor(
                0,
                255,
                255,
                120
            )
        )

        pen.setWidth(2)

        p.setPen(pen)

        p.drawLine(
            -140,
            y,
            140,
            y
        )
    # ====================

    def drawParticles(self,p):

        if self.progress < 900:
            return

        p.save()

        p.setPen(Qt.NoPen)

        for item in self.particles:

            alpha=max(
                30,
                255-abs(item["y"])
            )

            p.setBrush(

                QColor(

                    0,

                    240,

                    255,

                    alpha

                )

            )

            p.drawEllipse(

                item["x"],

                item["y"],

                item["size"],

                item["size"]

            )

        p.restore()
    # ====================

    def drawNoise(self,p):

        if self.progress < 940:
            return

        p.save()

        pen=QPen(

            QColor(

                0,

                255,

                255,

                25

            )

        )

        p.setPen(pen)

        for i in range(-160,160,8):

            if i%16==0:

                p.drawLine(

                    -150,

                    i,

                    150,

                    i

                )

        p.restore()
    # ====================

    def drawFlash(self,p):

        if self.progress < 980:
            return

        value=(

            math.sin(

                self.progress/10

            )+1

        )/2

        radius=70+value*50

        alpha=int(

            value*90

        )

        p.save()

        p.setPen(Qt.NoPen)

        p.setBrush(

            QColor(

                255,

                255,

                255,

                alpha

            )

        )

        p.drawEllipse(

            -radius,

            -radius,

            radius*2,

            radius*2

        )

        p.restore()
    # ====================

    def drawSystemText(self,p):

        if self.progress < 995:
            return

        p.save()

        font=p.font()

        font.setPointSize(18)

        font.setBold(True)

        p.setFont(font)

        p.setPen(

            QColor(

                170,

                255,

                255

            )

        )

        p.drawText(

            -120,

            320,

            "J.A.R.V.I.S"

        )

        p.drawText(

            -120,

            350,

            "SYSTEM ONLINE"

        )

        p.drawText(

            -120,

            380,

            "WELCOME BACK SIR"

        )

        p.restore()