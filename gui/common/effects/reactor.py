from .electric import ElectricBolt
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import (
    QTimer,
    Qt
)

from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
    QRadialGradient
)

import math


class Reactor(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.angle = 0
        self.pulse = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.timer.start(16)
        self.electric = []

        for _ in range(6):

            self.electric.append(

                ElectricBolt()

            )
    # =====================

    def updateAnimation(self):

        self.angle += 1.5

        if self.angle >= 360:
            self.angle = 0

        self.pulse += 0.05
        for bolt in self.electric:

            bolt.update()
        self.update()

    # =====================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.translate(
            self.width()/2,
            self.height()/2
        )

        self.drawGlow(painter)

        self.drawBloom(painter)

        self.drawShockWave(painter)

        self.drawHexRing(painter)

        self.drawOuterRing(painter)

        self.drawInnerRing(painter)

        self.drawEnergyRing(painter)

        self.drawEnergyNodes(painter)

        self.drawEnergyLines(painter)

        self.drawArcLightning(painter)

        self.drawPulse(painter)

        self.drawParticles(painter)

        self.drawCore(painter)

        self.drawTriangle(painter)

        self.drawLensFlare(painter)

        painter.end()
    # =====================

    def drawGlow(self, painter):

        glow = QRadialGradient(
            0,
            0,
            180
        )

        glow.setColorAt(
            0,
            QColor(
                0,
                220,
                255,
                180
            )
        )

        glow.setColorAt(
            1,
            QColor(
                0,
                220,
                255,
                0
            )
        )

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QBrush(glow)
        )

        painter.drawEllipse(
            -180,
            -180,
            360,
            360
        )
    # =====================

    def drawOuterRing(self, painter):

        painter.save()

        painter.rotate(
            self.angle
        )

        pen = QPen(
            QColor(
                0,
                216,
                255
            )
        )

        pen.setWidth(4)

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        painter.drawEllipse(
            -120,
            -120,
            240,
            240
        )

        for i in range(24):

            painter.rotate(15)

            painter.drawLine(
                0,
                -120,
                0,
                -140
            )

        painter.restore()
    # =====================

    def drawInnerRing(self, painter):

        painter.save()

        painter.rotate(
            -self.angle * 2
        )

        pen = QPen(
            QColor(
                100,
                240,
                255,
                220
            )
        )

        pen.setWidth(3)

        painter.setPen(pen)

        painter.drawEllipse(
            -85,
            -85,
            170,
            170
        )

        for i in range(12):

            painter.rotate(30)

            painter.drawLine(
                0,
                -85,
                0,
                -100
            )

        painter.restore()
    # =====================

    def drawCore(self, painter):

        painter.save()

        scale = 1 + math.sin(
            self.pulse
        ) * 0.05

        painter.scale(
            scale,
            scale
        )

        gradient = QRadialGradient(
            0,
            0,
            70
        )

        gradient.setColorAt(
            0,
            QColor(
                255,
                255,
                255
            )
        )

        gradient.setColorAt(
            0.35,
            QColor(
                80,
                240,
                255
            )
        )

        gradient.setColorAt(
            1,
            QColor(
                0,
                160,
                255
            )
        )

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            gradient
        )

        painter.drawEllipse(
            -55,
            -55,
            110,
            110
        )

        painter.restore()
    # =====================

    def drawTriangle(self, painter):

        painter.save()

        pen = QPen(
            QColor(
                255,
                255,
                255
            )
        )

        pen.setWidth(3)

        painter.setPen(pen)

        r = 35

        pts = []

        for i in range(3):

            a = math.radians(
                i * 120 - 90
            )

            pts.append((
                r * math.cos(a),
                r * math.sin(a)
            ))

        painter.drawLine(
            pts[0][0],
            pts[0][1],
            pts[1][0],
            pts[1][1]
        )

        painter.drawLine(
            pts[1][0],
            pts[1][1],
            pts[2][0],
            pts[2][1]
        )

        painter.drawLine(
            pts[2][0],
            pts[2][1],
            pts[0][0],
            pts[0][1]
        )

        painter.restore()
    # =====================

    def drawTriangle(self, painter):

        painter.save()

        pen = QPen(
            QColor(
                255,
                255,
                255
            )
        )

        pen.setWidth(3)

        painter.setPen(pen)

        r = 35

        pts = []

        for i in range(3):

            a = math.radians(
                i * 120 - 90
            )

            pts.append((
                r * math.cos(a),
                r * math.sin(a)
            ))

        painter.drawLine(
            pts[0][0],
            pts[0][1],
            pts[1][0],
            pts[1][1]
        )

        painter.drawLine(
            pts[1][0],
            pts[1][1],
            pts[2][0],
            pts[2][1]
        )

        painter.drawLine(
            pts[2][0],
            pts[2][1],
            pts[0][0],
            pts[0][1]
        )

        painter.restore()
    # =====================

    def drawEnergyRing(self, painter):

        painter.save()

        painter.rotate(self.angle * 3)

        pen = QPen(
            QColor(
                150,
                255,
                255,
                220
            )
        )

        pen.setWidth(5)

        painter.setPen(pen)

        radius = 70

        for i in range(6):

            start = i * 60

            painter.drawArc(
                -radius,
                -radius,
                radius * 2,
                radius * 2,
                start * 16,
                25 * 16
            )

        painter.restore()
    # =====================

    def drawHexRing(self, painter):

        painter.save()

        painter.rotate(
            -self.angle * 0.5
        )

        pen = QPen(
            QColor(
                0,
                255,
                255,
                120
            )
        )

        pen.setWidth(2)

        painter.setPen(pen)

        r = 145

        pts = []

        for i in range(6):

            a = math.radians(
                i * 60
            )

            pts.append((
                r * math.cos(a),
                r * math.sin(a)
            ))

        for i in range(6):

            p1 = pts[i]

            p2 = pts[(i+1)%6]

            painter.drawLine(
                p1[0],
                p1[1],
                p2[0],
                p2[1]
            )

        painter.restore()
    # =====================

    def drawPulse(self, painter):

        painter.save()

        alpha = (
            math.sin(
                self.pulse
            ) + 1
        ) / 2

        color = QColor(
            0,
            220,
            255,
            int(alpha * 80)
        )

        pen = QPen(color)

        pen.setWidth(3)

        painter.setPen(pen)

        r = 110 + alpha * 25

        painter.drawEllipse(
            -r,
            -r,
            r * 2,
            r * 2
        )

        painter.restore()
    # =====================

    def drawEnergyNodes(self, painter):

        painter.save()

        painter.rotate(
            self.angle * 2
        )

        for i in range(6):

            painter.save()

            painter.rotate(i * 60)

            painter.setPen(Qt.NoPen)

            painter.setBrush(
                QColor(
                    180,
                    255,
                    255
                )
            )

            painter.drawEllipse(
                -6,
                -132,
                12,
                12
            )

            painter.restore()

        painter.restore()
    # =====================

    def drawParticles(self, painter):

        painter.save()

        painter.setPen(Qt.NoPen)

        for i in range(50):

            angle = math.radians(
                i * 7 + self.angle * 3
            )

            radius = 45 + (
                i * 4
            ) % 120

            x = radius * math.cos(angle)

            y = radius * math.sin(angle)

            alpha = 255 - radius

            if alpha < 0:
                alpha = 0

            painter.setBrush(
                QColor(
                    120,
                    255,
                    255,
                    alpha
                )
            )

            size = 2 + (
                i % 3
            )

            painter.drawEllipse(
                x,
                y,
                size,
                size
            )

        painter.restore()
    # =====================

    def drawEnergyLines(self, painter):

        painter.save()

        pen = QPen(
            QColor(
                120,
                255,
                255,
                120
            )
        )

        pen.setWidth(2)

        painter.setPen(pen)

        painter.rotate(
            -self.angle
        )

        for i in range(12):

            painter.rotate(30)

            painter.drawLine(
                0,
                -55,
                0,
                -105
            )

        painter.restore()
    # =====================

    def drawShockWave(self, painter):

        painter.save()

        value = (math.sin(self.pulse * 2) + 1) / 2

        radius = 135 + value * 35

        alpha = int((1 - value) * 120)

        pen = QPen(
            QColor(
                0,
                220,
                255,
                alpha
            )
        )

        pen.setWidth(2)

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        painter.drawEllipse(
            -radius,
            -radius,
            radius * 2,
            radius * 2
        )

        painter.restore()
    # =====================

    def drawBloom(self, painter):

        painter.save()

        for i in range(8):

            alpha = 30 - i * 3

            if alpha < 0:
                alpha = 0

            painter.setPen(Qt.NoPen)

            painter.setBrush(
                QColor(
                    0,
                    220,
                    255,
                    alpha
                )
            )

            r = 55 + i * 7

            painter.drawEllipse(
                -r,
                -r,
                r * 2,
                r * 2
            )

        painter.restore()
    # =====================

    def drawArcLightning(self, painter):

        painter.save()

        pen = QPen(
            QColor(
                220,
                255,
                255
            )
        )

        pen.setWidth(2)

        painter.setPen(pen)

        for i in range(6):

            painter.save()

            painter.rotate(
                self.angle * 3 + i * 60
            )

            x = 0
            y = -95

            for j in range(8):

                nx = x + (-4 if j % 2 else 4)
                ny = y - 6

                painter.drawLine(
                    x,
                    y,
                    nx,
                    ny
                )

                x = nx
                y = ny

            painter.restore()

        painter.restore()
    # =====================

    def drawLensFlare(self, painter):

        painter.save()

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                255,
                255,
                255,
                45
            )
        )

        painter.drawEllipse(
            -18,
            -18,
            36,
            36
        )

        painter.setBrush(
            QColor(
                180,
                255,
                255,
                25
            )
        )

        painter.drawEllipse(
            -90,
            -4,
            180,
            8
        )

        painter.drawEllipse(
            -4,
            -90,
            8,
            180
        )

        painter.restore()