# boot_screen.py
# PART 1
from gui.effects.reactor import ReactorEffect
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import math
import random


class BootScreen(QWidget):

    bootFinished = Signal()

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background:#02050b;")
        self.reactor = ReactorEffect()
        self.fade = 0
        self.transition = False
        self.flash = 0
        self.progress = 0
        self.rotation = 0
        self.glow = 0
        self.scan_offset = 0
        self.grid_offset = 0
        self.cursor = True
        self.hex_rotation = 0
        self.ring_rotation = 0
        self.energy_phase = 0
        self.bloom_phase = 0
        self.flash_alpha = 0
        self.flashing = False

        self.fade_alpha = 255
        self.fading = False
        self.full_text = "INITIALIZING JARVIS CORE..."
        self.display_text = ""

        self.logs = [
            "[ OK ] Power System",
            "[ OK ] Neural Engine",
            "[ OK ] Security Layer",
            "[ OK ] Memory Cache",
            "[ OK ] Quantum Link",
            "[ OK ] Holographic Renderer",
            "[ OK ] Voice Engine",
            "[ OK ] AI Core",
        ]

        self.current_log = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateAnimation)
        self.timer.start(16)

        self.type_timer = QTimer(self)
        self.type_timer.timeout.connect(self.updateTyping)
        self.type_timer.start(40)

        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.updateLogs)
        self.log_timer.start(700)
        self.particles = []
        self.rain = []

        chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for _ in range(70):

            self.rain.append({
                "x": random.randint(0, 1920),
                "y": random.randint(-1200, 0),
                "speed": random.uniform(2.5, 7.0),
                "length": random.randint(10, 26),
                "chars": "".join(
                    random.choice(chars)
                    for _ in range(60)
                )
            })

        for _ in range(160):

            self.particles.append({
                "x": random.randint(0, 1920),
                "y": random.randint(0, 1080),
                "r": random.uniform(1.0, 3.5),
                "speed": random.uniform(0.4, 2.2),
                "alpha": random.randint(40, 180)
            })

    def updateAnimation(self):

        self.rotation += 1.8
        self.hex_rotation += 0.35
        self.ring_rotation -= 0.9
        self.glow += 0.05
        self.energy_phase += 0.08
        self.bloom_phase += 0.035
        self.scan_offset += 2
        self.grid_offset += 1

        w = max(1, self.width())
        h = max(1, self.height())

        for p in self.particles:

            p["y"] -= p["speed"]

            if p["y"] < -10:

                p["y"] = h + random.randint(0, 100)
                p["x"] = random.randint(0, w)
                p["r"] = random.uniform(1.0, 3.5)
                p["speed"] = random.uniform(0.4, 2.2)
                p["alpha"] = random.randint(40, 180)

        h = max(1, self.height())
        w = max(1, self.width())

        for rain in self.rain:

            rain["y"] += rain["speed"]

            if rain["y"] > h + 300:

                rain["y"] = random.randint(-1200, -200)
                rain["x"] = random.randint(0, w)
                rain["speed"] = random.uniform(2.5, 7.0)

        if self.progress < 100:

            self.progress += 0.25


        else:

           if not self.transition:

            self.transition = True
            self.flash = 1
            self.system_status = "ONLINE"

        if self.progress < 100:

            self.progress += 0.25

        else:

            if not self.flashing and not self.fading:

                self.flashing = True
                self.flash_alpha = 255


        if self.flashing:

            self.flash_alpha -= 12

            if self.flash_alpha <= 0:

                self.flash_alpha = 0
                self.flashing = False
                self.fading = True


        if self.fading:

            self.fade_alpha -= 5

            if self.fade_alpha <= 0:

                self.fade_alpha = 0

                if not hasattr(self, "_boot_done"):

                    self._boot_done = True
                    self.bootFinished.emit()
        self.reactor.update_animation()
        self.update()

    def updateTyping(self):

        if len(self.display_text) < len(self.full_text):
            self.display_text += self.full_text[len(self.display_text)]
        else:
            self.cursor = not self.cursor

    def updateLogs(self):

        if self.current_log < len(self.logs):
            self.current_log += 1

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.drawBackground(painter)
        self.drawBloom(painter)
        self.drawGlow(painter)
        self.drawBloomParticles(painter)
        self.drawGrid(painter)
        self.drawScanlines(painter)

        self.drawDigitalRain(painter)
        self.drawParticles(painter)

        self.drawOrbitRing(painter)
        self.drawHexFrame(painter)
        self.drawEnergyBeam(painter)
        self.reactor.draw(painter)
        self.drawProgressRing(painter)
        self.system_status = "BOOTING"
        self.drawLoadingText(painter)
        self.drawTerminal(painter)
        self.drawTransition(painter)
        self.drawFlash(painter)
        self.drawFade(painter)

    def drawTransition(self, painter):

        if not self.transition:
            return


        painter.save()


        # ===== WHITE CORE FLASH =====

        flash_alpha = int(
            max(0, (1 - self.fade / 100) * 180)
        )


        painter.fillRect(
            self.rect(),
            QColor(
                255,
                255,
                255,
                flash_alpha
            )
        )


        # ===== DARK FADE OUT =====

        fade_alpha = int(
            self.fade * 2
        )


        painter.fillRect(
            self.rect(),
            QColor(
                0,
                0,
                0,
                fade_alpha
            )
        )


        # ===== ONLINE TEXT =====

        if self.fade < 40:

            font = QFont(
                "Consolas",
                26,
                QFont.Bold
            )

            painter.setFont(font)

            painter.setPen(
                QColor(
                    180,
                    255,
                    255,
                    220
                )
            )


            painter.drawText(
                QRectF(
                    0,
                    self.height()/2 + 260,
                    self.width(),
                    50
                ),
                Qt.AlignCenter,
                "JARVIS CORE ONLINE"
            )


        painter.restore()

    def drawDigitalRain(self, painter):

        painter.save()

        font = QFont("Consolas", 10)
        painter.setFont(font)

        for rain in self.rain:

            y = rain["y"]

            for i in range(rain["length"]):

                alpha = max(0, 220 - i * 12)

                painter.setPen(
                    QColor(
                        0,
                        255,
                        220,
                        alpha
                    )
                )

                if i < len(rain["chars"]):

                    painter.drawText(
                        int(rain["x"]),
                        int(y + i * 18),
                        rain["chars"][i]
                    )

        painter.restore()

    def drawOrbitRing(self, painter):

        painter.save()

        cx = self.width() / 2
        cy = self.height() / 2 - 40

        painter.translate(cx, cy)
        painter.rotate(self.ring_rotation)

        pen = QPen(QColor(0, 220, 255, 90))
        pen.setWidth(2)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        r = 132

        for i in range(12):

            painter.drawArc(
                QRectF(
                    -r,
                    -r,
                    r * 2,
                    r * 2
                ),
                i * 30 * 16,
                12 * 16
            )

        painter.restore()

    def drawHexFrame(self, painter):

        painter.save()

        cx = self.width() / 2
        cy = self.height() / 2 - 40

        painter.translate(cx, cy)
        painter.rotate(self.hex_rotation)

        pen = QPen(QColor(0, 255, 255, 130))
        pen.setWidth(2)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        radius = 88

        points = []

        for i in range(6):

            angle = math.radians(i * 60 - 30)

            points.append(
                QPointF(
                    radius * math.cos(angle),
                    radius * math.sin(angle)
                )
            )

        painter.drawPolygon(QPolygonF(points))

        radius = 68

        points.clear()

        for i in range(6):

            angle = math.radians(i * 60 + 30)

            points.append(
                QPointF(
                    radius * math.cos(angle),
                    radius * math.sin(angle)
                )
            )

        painter.drawPolygon(QPolygonF(points))

        painter.restore()

    def drawEnergyBeam(self, painter):

        painter.save()

        cx = self.width() / 2
        cy = self.height() / 2 - 40

        length = 150

        alpha = int(
            90 + 60 * abs(math.sin(self.energy_phase))
        )

        beam = QLinearGradient(
            cx,
            cy - length,
            cx,
            cy + length
        )

        beam.setColorAt(
            0,
            QColor(0, 255, 255, 0)
        )

        beam.setColorAt(
            0.5,
            QColor(120, 255, 255, alpha)
        )

        beam.setColorAt(
            1,
            QColor(0, 255, 255, 0)
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(beam)

        painter.drawRoundedRect(
            QRectF(
                cx - 3,
                cy - length,
                6,
                length * 2
            ),
            3,
            3
        )

        beam2 = QLinearGradient(
            cx,
            cy - 90,
            cx,
            cy + 90
        )

        beam2.setColorAt(
            0,
            QColor(255, 255, 255, 0)
        )

        beam2.setColorAt(
            0.5,
            QColor(255, 255, 255, 120)
        )

        beam2.setColorAt(
            1,
            QColor(255, 255, 255, 0)
        )

        painter.setBrush(beam2)

        painter.drawRoundedRect(
            QRectF(
                cx - 1,
                cy - 90,
                2,
                180
            ),
            1,
            1
        )

        painter.restore()

    def drawBackground(self, painter):

        painter.fillRect(self.rect(), QColor(2, 6, 12))

        gradient = QRadialGradient(
            self.width() / 2,
            self.height() / 2,
            self.width() * 0.8
        )

        gradient.setColorAt(0.0, QColor(0, 255, 255, 22))
        gradient.setColorAt(0.4, QColor(0, 180, 255, 12))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))

        painter.fillRect(self.rect(), gradient)

    def drawGrid(self, painter):

        painter.save()

        pen = QPen(QColor(0, 180, 255, 18))
        pen.setWidth(1)
        painter.setPen(pen)

        step = 40

        ox = self.grid_offset % step
        oy = self.grid_offset % step

        for x in range(-step, self.width() + step, step):
            painter.drawLine(
                x + ox,
                0,
                x + ox,
                self.height()
            )

        for y in range(-step, self.height() + step, step):
            painter.drawLine(
                0,
                y + oy,
                self.width(),
                y + oy
            )

        painter.restore()

    def drawScanlines(self, painter):

        painter.save()

        pen = QPen(QColor(0, 255, 255, 10))
        painter.setPen(pen)

        for y in range(0, self.height(), 4):
            painter.drawLine(0, y, self.width(), y)

        glow = QLinearGradient(
            0,
            self.scan_offset,
            0,
            self.scan_offset + 120
        )

        glow.setColorAt(0, QColor(0, 255, 255, 0))
        glow.setColorAt(0.5, QColor(0, 255, 255, 45))
        glow.setColorAt(1, QColor(0, 255, 255, 0))

        painter.fillRect(
            0,
            self.scan_offset - 60,
            self.width(),
            120,
            glow
        )

        if self.scan_offset > self.height() + 120:
            self.scan_offset = -120

        painter.restore()

    def drawReactor(self, painter):

        painter.save()

        cx = self.width() / 2
        cy = self.height() / 2 - 40

        t = self.glow
        painter.translate(cx, cy)

        # ===== OUTER GLOW =====

        for radius, alpha in [
            (170, 8),
            (145, 14),
            (120, 24),
            (100, 40),
        ]:
            color = QColor(0, 255, 255, alpha)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(
                QPointF(cx, cy),
                radius,
                radius
            )

        # ===== ROTATING TRIANGLES =====

        for layer in range(2):

            painter.save()

            painter.rotate(
                self.rotation * (2.2 + layer)
            )

            radius = 95 - layer * 18

            pen = QPen(
                QColor(
                    0,
                    255,
                    255,
                    90 - layer * 20
                )
            )

            pen.setWidth(2)

            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            pts = []

            for i in range(3):

                a = math.radians(i * 120 - 90)

                pts.append(
                    QPointF(
                        math.cos(a) * radius,
                        math.sin(a) * radius
                    )
                )

            painter.drawPolygon(
                QPolygonF(pts)
            )

            painter.restore()

        # ===== OUTER TICKS =====

        pen = QPen(
            QColor(
                120,
                255,
                255,
                150
            )
        )

        pen.setWidth(2)

        painter.setPen(pen)

        tick_r = 118

        for i in range(36):

            angle = math.radians(
                i * 10 +
                self.rotation
            )

            length = 8 if i % 3 else 14

            x1 = math.cos(angle) * tick_r
            y1 = math.sin(angle) * tick_r

            x2 = math.cos(angle) * (tick_r + length)
            y2 = math.sin(angle) * (tick_r + length)

            painter.drawLine(
                QPointF(x1, y1),
                QPointF(x2, y2)
            )

       # ===== REACTOR V3 =====

        for layer in range(4):

            painter.save()

            speed = (1.0 + layer * 0.35)
            direction = 1 if layer % 2 == 0 else -1

            painter.rotate(
                self.rotation * speed * direction
            )

            radius = 112 - layer * 18

            pen = QPen(
                QColor(
                    0,
                    255,
                    255,
                    190 - layer * 35
                )
            )
            pen.setWidth(2)

            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            for angle in range(0, 360, 60):

                span = 26 + layer * 4

                painter.drawArc(
                    QRectF(
                        -radius,
                        -radius,
                        radius * 2,
                        radius * 2
                    ),
                    angle * 16,
                    span * 16
                )

            painter.restore()

        # ===== INNER PULSE =====

        pulse = 60 + math.sin(t * 3.5) * 5

        pen = QPen(QColor(180, 255, 255))
        pen.setWidth(3)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        painter.drawEllipse(
            QPointF(0, 0),
            pulse,
            pulse
        )

        for i in range(12):

            a = math.radians(i * 30 + self.rotation * 2)

            x = math.cos(a) * pulse
            y = math.sin(a) * pulse

            painter.drawLine(
                QPointF(
                    x * 0.86,
                    y * 0.86
                ),
                QPointF(x, y)
            )

        # ===== ENERGY NODES =====

        node_radius = 82

        for i in range(6):

            angle = math.radians(
                i * 60 +
                self.rotation * 2
            )

            x = math.cos(angle) * node_radius
            y = math.sin(angle) * node_radius

            glow = QRadialGradient(QPointF(x, y), 12)

            glow.setColorAt(0, QColor(255, 255, 255))
            glow.setColorAt(0.4, QColor(140, 255, 255))
            glow.setColorAt(1, QColor(0, 255, 255, 0))

            painter.setPen(Qt.NoPen)
            painter.setBrush(glow)

            painter.drawEllipse(QPointF(x, y), 9, 9)

        # ===== REACTOR SPARKS =====

            spark_radius = 48

            for i in range(24):

                angle = math.radians(
                    i * 15 +
                    self.rotation * 4
                )

                length = 6 + 6 * abs(
                    math.sin(
                        t * 4 + i
                    )
                )

                x1 = math.cos(angle) * spark_radius
                y1 = math.sin(angle) * spark_radius

                x2 = math.cos(angle) * (spark_radius + length)
                y2 = math.sin(angle) * (spark_radius + length)

                pen = QPen(
                    QColor(
                        180,
                        255,
                        255,
                        180
                    )
                )

                pen.setWidthF(1.3)

                painter.setPen(pen)

                painter.drawLine(
                    QPointF(x1, y1),
                    QPointF(x2, y2)
                )

        # ===== INNER ROTOR =====

            painter.save()

            painter.rotate(-self.rotation * 3)

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

            for i in range(8):

                painter.rotate(45)

                painter.drawLine(
                    20,
                    0,
                    38,
                    0
                )

            painter.restore()

        # ===== ENERGY CONNECTIONS =====

            pen = QPen(
                QColor(
                    0,
                    255,
                    255,
                    70
                )
            )

            pen.setWidthF(1.2)

            painter.setPen(pen)

            for i in range(6):

                a1 = math.radians(
                    i * 60 +
                    self.rotation * 2
                )

                a2 = math.radians(
                    (i + 2) * 60 +
                    self.rotation * 2
                )

                p1 = QPointF(
                    math.cos(a1) * node_radius,
                    math.sin(a1) * node_radius
                )

                p2 = QPointF(
                    math.cos(a2) * node_radius,
                    math.sin(a2) * node_radius
                )

                painter.drawLine(p1, p2)

            # ===== INNER ENERGY RING =====

            ring = 36 + math.sin(t * 6) * 3

            pen = QPen(
                QColor(
                    180,
                    255,
                    255,
                    180
                )
            )

            pen.setWidth(2)

            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            painter.drawEllipse(
                QPointF(0, 0),
                ring,
                ring
            )

            # ===== CENTER PULSE =====

            pulse = 10 + abs(
                math.sin(
                    t * 7
                )
            ) * 6

            painter.setBrush(
                QColor(
                    255,
                    255,
                    255,
                    210
                )
            )

            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                QPointF(0, 0),
                pulse,
                pulse
            )

        # ===== ENERGY ORBITS =====

        for orbit in range(2):

            painter.save()

            speed = (-3.2 if orbit == 0 else 2.6)

            painter.rotate(
                self.rotation * speed
            )

            orbit_r = 72 + orbit * 18

            for i in range(4):

                angle = math.radians(i * 90)

                x = math.cos(angle) * orbit_r
                y = math.sin(angle) * orbit_r

                glow = QRadialGradient(
                    QPointF(x, y),
                    8
                )

                glow.setColorAt(
                    0,
                    QColor(255, 255, 255)
                )

                glow.setColorAt(
                    0.4,
                    QColor(120, 255, 255)
                )

                glow.setColorAt(
                    1,
                    QColor(0, 255, 255, 0)
                )

                painter.setBrush(glow)
                painter.setPen(Qt.NoPen)

                painter.drawEllipse(
                    QPointF(x, y),
                    6,
                    6
                )

            painter.restore()

        # ===== REACTOR FLASH =====

        flash = abs(math.sin(t * 8))

        if flash > 0.85:

            painter.setBrush(
                QColor(
                    255,
                    255,
                    255,
                    int((flash - 0.85) * 900)
                )
            )

            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                QPointF(0, 0),
                32,
                32
            )
        # ===== CORE =====

        core = QRadialGradient(
            QPointF(0, 0),
            36
        )

        core.setColorAt(0, QColor(255,255,255))
        core.setColorAt(0.25, QColor(180,255,255))
        core.setColorAt(0.65, QColor(0,220,255))
        core.setColorAt(1, QColor(0,80,140))

        painter.setBrush(core)
        painter.setPen(Qt.NoPen)

        size = 22 + math.sin(t * 4) * 2

        painter.drawEllipse(
            QPointF(0, 0),
            size,
            size
        )

        painter.restore()

    def drawBloomParticles(self, painter):

        painter.save()

        cx = self.width() / 2
        cy = self.height() / 2 - 40

        painter.translate(cx, cy)


        for i in range(28):

            angle = math.radians(
                i * (360 / 28)
                +
                self.rotation * 1.8
            )


            radius = (
                92
                +
                math.sin(
                    self.bloom_phase * 3
                    +
                    i * 0.45
                ) * 14
                +
                abs(
                    math.sin(
                        self.glow * 2
                    )
                ) * 10
            )


            x = math.cos(angle) * radius
            y = math.sin(angle) * radius


            g = QRadialGradient(
                QPointF(x,y),
                8
            )


            g.setColorAt(
                0,
                QColor(
                    255,
                    255,
                    255,
                    180
                )
            )

            g.setColorAt(
                0.35,
                QColor(
                    120,
                    255,
                    255,
                    130
                )
            )

            g.setColorAt(
                1,
                QColor(
                    0,
                    255,
                    255,
                    0
                )
            )


            painter.setBrush(g)
            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                QPointF(x,y),
                5,
                5
            )


        painter.restore()

    def drawBloom(self, painter):

        painter.save()

        cx = self.width() / 2
        cy = self.height() / 2 - 40

        pulse = (
            math.sin(self.bloom_phase * 2)
            + 1
        ) / 2


        for radius, alpha in [

            (260, 5),
            (220, 10),
            (180, 18),
            (140, 30),
            (100, 45),

        ]:

            glow = QRadialGradient(
                QPointF(cx, cy),
                radius
            )


            glow.setColorAt(
                0,
                QColor(
                    0,
                    255,
                    255,
                    int(alpha * pulse)
                )
            )

            glow.setColorAt(
                0.4,
                QColor(
                    0,
                    200,
                    255,
                    int(alpha * 0.5)
                )
            )

            glow.setColorAt(
                1,
                QColor(
                    0,
                    255,
                    255,
                    0
                )
            )


            painter.setPen(Qt.NoPen)
            painter.setBrush(glow)


            painter.drawEllipse(
                QPointF(cx, cy),
                radius,
                radius
            )


        painter.restore()
    def drawGlow(self, painter):

        painter.save()

        cx = self.width() / 2
        cy = self.height() / 2 - 40

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        pulse = (
            math.sin(
                self.glow * 3
            ) + 1
        ) / 2

        for i in range(10):

            radius = 45 + i * 7 + pulse * 4

            alpha = max(
                0,
                80 - i * 8
            )

            pen = QPen(
                QColor(
                    120,
                    255,
                    255,
                    alpha
                )
            )

            pen.setWidth(2)

            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            painter.drawEllipse(
                QPointF(cx, cy),
                radius,
                radius
            )

        flare = QRadialGradient(
            QPointF(cx, cy),
            70
        )

        flare.setColorAt(
            0,
            QColor(
                255,
                255,
                255,
                60
            )
        )

        flare.setColorAt(
            0.35,
            QColor(
                120,
                255,
                255,
                45
            )
        )

        flare.setColorAt(
            1,
            QColor(
                0,
                255,
                255,
                0
            )
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(flare)

        painter.drawEllipse(
            QPointF(cx, cy),
            70,
            70
        )

        # ===== ROTATING HALO =====

        painter.save()

        painter.translate(cx, cy)
        painter.rotate(self.rotation * 1.5)

        pen = QPen(QColor(180, 255, 255, 120))
        pen.setWidth(2)

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)

        for i in range(8):

            painter.drawArc(
                QRectF(
                    -82,
                    -82,
                    164,
                    164
                ),
                i * 45 * 16,
                18 * 16
            )

        painter.restore()

        # ===== LIGHT RAYS =====

        painter.save()

        painter.translate(cx, cy)
        painter.rotate(-self.rotation * 2)

        pen = QPen(QColor(255, 255, 255, 45))
        pen.setWidth(1)

        painter.setPen(pen)

        for i in range(16):

            painter.rotate(22.5)

            painter.drawLine(
                72,
                0,
                105,
                0
            )

        painter.restore()

    def drawBloomParticles(self, painter):

        painter.save()

        cx = self.width() / 2
        cy = self.height() / 2 - 40

        painter.translate(cx, cy)


        for i in range(28):

            angle = math.radians(
                i * (360 / 28)
                +
                self.rotation * 1.8
            )


            radius = (
                92
                +
                math.sin(
                    self.bloom_phase * 3
                    +
                    i * 0.45
                ) * 14
                +
                abs(
                    math.sin(
                        self.glow * 2
                    )
                ) * 10
            )


            x = math.cos(angle) * radius
            y = math.sin(angle) * radius


            glow = QRadialGradient(
                QPointF(x,y),
                8
            )


            glow.setColorAt(
                0,
                QColor(
                    255,
                    255,
                    255,
                    180
                )
            )


            glow.setColorAt(
                0.4,
                QColor(
                    120,
                    255,
                    255,
                    120
                )
            )


            glow.setColorAt(
                1,
                QColor(
                    0,
                    255,
                    255,
                    0
                )
            )


            painter.setBrush(glow)
            painter.setPen(Qt.NoPen)


            painter.drawEllipse(
                QPointF(x,y),
                5,
                5
            )


        painter.restore()
    def drawProgressRing(self, painter):

        painter.save()

        cx = self.width() / 2
        cy = self.height() / 2 - 40

        r = 145

        painter.setPen(
            QPen(
                QColor(0, 255, 255, 25),
                6
            )
        )

        painter.setBrush(Qt.NoBrush)

        painter.drawEllipse(
            QPointF(cx, cy),
            r,
            r
        )

        pen = QPen(
            QColor(0, 255, 255),
            6
        )

        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)

        angle = int(
            self.progress / 100 * 360 * 16
        )

        painter.drawArc(
            QRectF(
                cx - r,
                cy - r,
                r * 2,
                r * 2
            ),
            90 * 16,
            -angle
        )

        painter.restore()

    def drawLoadingText(self, painter):

        painter.save()

        cx = self.width() / 2

        title_font = QFont(
            "Consolas",
            16,
            QFont.Bold
        )

        painter.setFont(title_font)

        painter.setPen(
            QColor(120, 255, 255)
        )

        painter.drawText(
            QRectF(
                0,
                self.height() / 2 + 150,
                self.width(),
                40
            ),
            Qt.AlignCenter,
            self.display_text +
            ("|" if self.cursor else "")
        )

        percent_font = QFont(
            "Consolas",
            28,
            QFont.Bold
        )

        painter.setFont(percent_font)

        painter.drawText(
            QRectF(
                0,
                self.height() / 2 + 185,
                self.width(),
                60
            ),
            Qt.AlignCenter,
            f"{int(self.progress)}%"
        )

        painter.restore()

    def drawTerminal(self, painter):

        painter.save()

        font = QFont(
            "Consolas",
            10
        )

        painter.setFont(font)

        x = 60
        y = self.height() - 180

        for i in range(self.current_log):

            painter.setPen(
                QColor(
                    120,
                    255,
                    180
                )
            )

            painter.drawText(
                x,
                y + i * 22,
                self.logs[i]
            )

        painter.restore()

    def drawParticles(self, painter):

        painter.save()

        painter.setPen(Qt.NoPen)

        for p in self.particles:

            glow = QRadialGradient(
                QPointF(
                    p["x"],
                    p["y"]
                ),
                p["r"] * 4
            )

            glow.setColorAt(
                0,
                QColor(
                    180,
                    255,
                    255,
                    p["alpha"]
                )
            )

            glow.setColorAt(
                0.45,
                QColor(
                    0,
                    255,
                    255,
                    p["alpha"] // 2
                )
            )

            glow.setColorAt(
                1,
                QColor(
                    0,
                    255,
                    255,
                    0
                )
            )

            painter.setBrush(glow)

            painter.drawEllipse(
                QPointF(
                    p["x"],
                    p["y"]
                ),
                p["r"] * 4,
                p["r"] * 4
            )

            painter.setBrush(
                QColor(
                    220,
                    255,
                    255,
                    p["alpha"]
                )
            )

            painter.drawEllipse(
                QPointF(
                    p["x"],
                    p["y"]
                ),
                p["r"],
                p["r"]
            )

        painter.restore()
    def drawFlash(self, painter):

        if self.flash_alpha <= 0:
            return

        painter.save()

        painter.fillRect(
            self.rect(),
            QColor(
                255,
                255,
                255,
                self.flash_alpha
            )
        )

        painter.restore()


    def drawFade(self, painter):

        if self.fade_alpha >= 255:
            return

        painter.save()

        painter.fillRect(
            self.rect(),
            QColor(
                0,
                0,
                0,
                255 - self.fade_alpha
            )
        )

        painter.restore()