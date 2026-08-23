from PySide6.QtWidgets import QWidget

from PySide6.QtCore import (
    Qt,
    QTimer,
    QSize
)

from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen
)

import math
class Reactor(QWidget):

    READY = 0
    LISTENING = 1
    THINKING = 2
    EXECUTING = 3
    SPEAKING = 4
    ERROR = 5

    def __init__(self,parent=None):

        super().__init__(parent)

        self.state = Reactor.READY

        self.angle1 = 0

        self.angle2 = 0

        self.angle3 = 0

        self.energy = 0

        self.orbit = 0

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(16)
    def sizeHint(self):

        return QSize(
            700,
            700
        )

    def setState(self,state):

        self.state = state
    def animate(self):

        speed = 1

        if self.state == Reactor.READY:

            speed = 1

        elif self.state == Reactor.LISTENING:

            speed = 2

        elif self.state == Reactor.THINKING:

            speed = 6

        elif self.state == Reactor.EXECUTING:

            speed = 8

        elif self.state == Reactor.SPEAKING:

            speed = 4

        elif self.state == Reactor.ERROR:

            speed = 10

        self.angle1 += speed

        self.angle2 -= speed*0.7

        self.angle3 += speed*1.5

        self.energy += speed

        self.orbit += speed * 2

        self.update()
    def paintEvent(self,e):

        p = QPainter(self)

        p.setRenderHint(
            QPainter.Antialiasing
        )

        p.fillRect(
            self.rect(),
            QColor(
                0,
                0,
                0,
                0
            )
        )

        p.translate(

            self.width()/2,

            self.height()/2

        )

        self.drawGlow(p)

        self.drawOuterRing(p)

        self.drawMiddleRing(p)

        self.drawInnerRing(p)

        self.drawEnergy(p)

        self.drawArc(p)

        self.drawCore(p)

        p.end()
    # ==========================================
    # GLOW LAYER
    # ==========================================

    def drawGlow(self, p):

        pulse = (
            math.sin(
                self.energy * 0.05
            ) + 1
        ) / 2

        radius = 140 + pulse * 15

        for i in range(10):

            alpha = 35 - i * 3

            if alpha < 0:
                alpha = 0

            p.setPen(Qt.NoPen)

            p.setBrush(

                QColor(
                    0,
                    220,
                    255,
                    alpha
                )

            )

            r = radius + i * 10

            p.drawEllipse(
                -r,
                -r,
                r * 2,
                r * 2
            )
    # ==========================================
    # OUTER RING
    # ==========================================

    def drawOuterRing(self, p):

        p.save()

        p.rotate(self.angle1)

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

        p.drawEllipse(
            -120,
            -120,
            240,
            240
        )

        for i in range(12):

            p.rotate(30)

            p.drawLine(
                100,
                0,
                120,
                0
            )

        p.restore()
    # ==========================================
    # MIDDLE RING
    # ==========================================

    def drawMiddleRing(self, p):

        p.save()

        p.rotate(self.angle2)

        pen = QPen(
            QColor(
                100,
                255,
                255
            )
        )

        pen.setWidth(2)

        p.setPen(pen)

        p.drawEllipse(
            -85,
            -85,
            170,
            170
        )

        for i in range(18):

            p.rotate(20)

            p.drawLine(
                70,
                0,
                84,
                0
            )

        p.restore()
    # ==========================================
    # INNER RING
    # ==========================================

    def drawInnerRing(self, p):

        p.save()

        p.rotate(self.angle3)

        pen = QPen(
            QColor(
                180,
                255,
                255
            )
        )

        pen.setWidth(2)

        p.setPen(pen)

        p.drawEllipse(
            -45,
            -45,
            90,
            90
        )

        for i in range(8):

            p.rotate(45)

            p.drawLine(
                30,
                0,
                45,
                0
            )

        p.restore()
    # ==========================================
    # CORE
    # ==========================================

    def drawCore(self,p):

        pulse = (

            math.sin(

                self.energy*0.08

            )+1

        )/2

        radius = 22 + pulse*5

        for i in range(8):

            alpha = 160 - i*18

            if alpha < 0:
                alpha = 0

            p.setPen(Qt.NoPen)

            p.setBrush(

                QColor(

                    180,

                    255,

                    255,

                    alpha

                )

            )

            r = radius + i*3

            p.drawEllipse(

                -r,

                -r,

                r*2,

                r*2

            )

        p.setBrush(

            QColor(

                255,

                255,

                255

            )

        )

        p.drawEllipse(

            -10,

            -10,

            20,

            20

        )
    # ==========================================
    # ELECTRIC ARC
    # ==========================================

    def drawArc(self, p):

        import random

        if self.state == Reactor.READY:

            chance = 4

        elif self.state == Reactor.THINKING:

            chance = 20

        elif self.state == Reactor.EXECUTING:

            chance = 35

        else:

            chance = 10

        if random.randint(0,100) > chance:
            return

        pen = QPen(
            QColor(
                180,
                255,
                255,
                220
            )
        )

        pen.setWidth(2)

        p.setPen(pen)

        angle = random.randint(
            0,
            360
        )

        r1 = 38

        r2 = 118

        x1 = math.cos(
            math.radians(angle)
        ) * r1

        y1 = math.sin(
            math.radians(angle)
        ) * r1

        x2 = math.cos(
            math.radians(angle)
        ) * r2

        y2 = math.sin(
            math.radians(angle)
        ) * r2

        p.drawLine(
            x1,
            y1,
            x2,
            y2
        )
    # ==========================================
    # ENERGY ORBIT
    # ==========================================

    def drawEnergy(self,p):

        p.save()

        p.rotate(self.orbit)

        p.setPen(Qt.NoPen)

        for i in range(8):

            p.rotate(45)

            p.setBrush(

                QColor(

                    0,

                    255,

                    255,

                    180

                )

            )

            p.drawEllipse(

                102,

                -3,

                7,

                7

            )

        p.restore()