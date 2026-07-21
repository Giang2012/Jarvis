from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QPainter,
    QPen,
    QColor,
    QBrush
)

import math
import random


class AICore(QWidget):

    def __init__(self):
        super().__init__()

        self.setMinimumSize(420, 420)

        # animation
        self.rotation = 0
        self.inner_rotation = 0
        self.pulse = 0
        self.particles = []

        # trạng thái agent sau này
        self.state = "idle"

        # tạo hạt năng lượng
        for i in range(60):
            self.particles.append({
                "angle": random.uniform(0, 360),
                "radius": random.randint(120, 180),
                "speed": random.uniform(0.5, 2)
            })


        # timer animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)
        # =========================
        # Animation Variables
        # =========================

        self.state = "READY"

        self.outer_rotation = 0
        self.inner_rotation = 0
        self.core_rotation = 0
        self.hex_rotation = 0
        self.text_rotation = 0
        self.radar_rotation = 0

        self.energy = 0
        self.energy_direction = 1

        self.pulse = 0
        self.glow = 0

        self.scan_offset = 0

        self.rings = [
            170,
            145,
            120,
            92,
            68
        ]

        self.state_colors = {
            "READY": QColor(0,255,255),
            "IDLE": QColor(0,170,255),
            "LISTENING": QColor(0,255,180),
            "THINKING": QColor(180,80,255),
            "REASONING": QColor(255,200,60),
            "EXECUTING": QColor(255,120,40),
            "SPEAKING": QColor(255,255,255),
            "ERROR": QColor(255,70,70)
        }

        self.particles = []

        for _ in range(180):

            angle = random.uniform(0, math.pi * 2)

            radius = random.randint(55,170)

            speed = random.uniform(0.003,0.02)

            size = random.randint(2,5)

            alpha = random.randint(70,200)

            self.particles.append({
                "angle":angle,
                "radius":radius,
                "speed":speed,
                "size":size,
                "alpha":alpha
            })

        self.orbit_text = " J.A.R.V.I.S  QUANTUM AI CORE "

    def animate(self):

        self.outer_rotation += 0.6
        self.inner_rotation -= 1.3
        self.core_rotation += 2.1
        self.hex_rotation -= 0.35

        self.text_rotation += 0.4
        self.radar_rotation += 2.8

        self.energy += self.energy_direction

        if self.energy > 100:
            self.energy_direction = -1

        if self.energy < 0:
            self.energy_direction = 1

        self.glow = self.energy
        self.pulse += 0.08

        if self.pulse > math.pi * 2:
            self.pulse = 0

        self.scan_offset += 3

        if self.scan_offset > self.height():
            self.scan_offset = 0

        for p in self.particles:

            p["angle"] += p["speed"]

            if p["angle"] > math.pi * 2:
                p["angle"] = 0

        self.update()



    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )


        center = self.rect().center()


        # =========================
        # PARTICLE ENERGY
        # =========================

        for p in self.particles:

            angle = math.radians(p["angle"])

            x = (
                center.x()
                +
                math.cos(angle)
                *
                p["radius"]
            )

            y = (
                center.y()
                +
                math.sin(angle)
                *
                p["radius"]
            )


            painter.setBrush(
                QColor(
                    0,
                    220,
                    255,
                    120
                )
            )

            painter.setPen(Qt.NoPen)

            painter.drawEllipse(
                int(x),
                int(y),
                3,
                3
            )


        # =========================
        # REACTOR RINGS
        # =========================

        painter.save()

        painter.translate(center)

        rings = [
            (170, self.outer_rotation, 260, 0),
            (145, -self.inner_rotation, 180, 120),
            (120, self.core_rotation, 120, 200),
            (92, -self.hex_rotation, 80, 40),
        ]

        color = self.currentColor()

        for radius, rotation, span, start in rings:

            painter.save()

            painter.rotate(rotation)

            pen = QPen(color, 3)

            pen.setCapStyle(Qt.RoundCap)

            painter.setPen(pen)

            for i in range(4):

                painter.drawArc(
                    -radius,
                    -radius,
                    radius * 2,
                    radius * 2,
                    (start + i * 90) * 16,
                    span * 16 // 4
                )

            painter.restore()

        painter.restore()
        
        # =========================
        # CORE GLOW
        # =========================

        for i in range(6):

            alpha = 45 - i * 7

            painter.setBrush(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    alpha
                )
            )

            painter.setPen(Qt.NoPen)

            size = 90 + i * 12 + math.sin(self.pulse) * 6

            painter.drawEllipse(
                center,
                int(size),
                int(size)
            )

        # =========================
        # INNER CORE
        # =========================


        pulse_size = (
            65
            +
            math.sin(self.pulse)
            *
            10
        )


        painter.setBrush(
           QColor(
                color.red(),
                color.green(),
                color.blue(),
                70
            )
        )


        painter.setPen(
            QPen(
                color,
                2
                )
        )


        painter.drawEllipse(
            center,
            int(pulse_size),
            int(pulse_size)
        )

        # =========================
        # PLASMA RING
        # =========================

        painter.save()

        painter.translate(center)

        painter.rotate(self.core_rotation)

        pen = QPen(color,2)

        painter.setPen(pen)

        for i in range(18):

            angle = math.radians(i * 20)

            r = 82 + math.sin(
                angle * 4 +
                self.pulse
            ) * 6

            x = math.cos(angle) * r
            y = math.sin(angle) * r

            painter.drawPoint(
                int(x),
                int(y)
            )

        painter.restore()

        # =========================
        # CORE LIGHT
        # =========================

        painter.setBrush(
            QColor(
                255,
                255,
                255,
                240
            )
        )

        painter.setPen(Qt.NoPen)


        painter.drawEllipse(
            center,
            20,
            20
        )

        # =========================
        # RADAR
        # =========================

        painter.save()

        painter.translate(center)

        painter.rotate(self.radar_rotation)

        pen = QPen(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                120
            ),
            2
        )

        painter.setPen(pen)

        painter.drawLine(
            0,
            0,
            170,
            0
        )

        painter.restore()

        # =========================
        # TEXT
        # =========================

        painter.setPen(color)


        painter.drawText(
            center.x()-40,
            center.y()+110,
            "J.A.R.V.I.S"
        )
    def currentColor(self):

        return self.state_colors.get(
            self.state,
            QColor(0,255,255)
        )