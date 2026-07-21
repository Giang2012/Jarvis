"""
JARVIS Reactor V3
Arc Reactor core animation widget
"""

import math
import random

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QPointF
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QBrush,
)


class ReactorEffect:

    def __init__(self):

        self.angle = 0
        self.pulse = 0
        self.energy = 0.8

        self.particles = []

        for i in range(80):
            self.particles.append(
                {
                    "angle": random.uniform(0, 360),
                    "radius": random.randint(50, 120),
                    "speed": random.uniform(0.5, 2),
                    "size": random.randint(1, 3)
                }
            )



    # ==========================
    # Animation
    # ==========================

    def update_animation(self):

        self.angle += 2

        self.pulse += 0.08

        if self.pulse > math.pi * 2:
            self.pulse = 0


        for p in self.particles:
            p["angle"] += p["speed"]




    # ==========================
    # Painting
    # ==========================

    def draw(self, painter):

        # dùng painter được truyền từ BootScreen

        painter.setRenderHint(
            QPainter.Antialiasing
        )


        cx = painter.viewport().center().x()
        cy = painter.viewport().center().y() - 40

        size = 220


        # ----------------------
        # Energy pulse
        # ----------------------

        pulse_size = (
            math.sin(self.pulse)
            + 1
        ) * 8


        painter.setPen(
            QPen(
                QColor(0,180,255,120),
                3
            )
        )


        painter.drawEllipse(
            QPointF(cx,cy),
            size/4 + pulse_size,
            size/4 + pulse_size
        )



        # ----------------------
        # Outer Rings
        # ----------------------

        rings = [
            0.28,
            0.34,
            0.40
        ]


        for i,r in enumerate(rings):

            pen = QPen(
                QColor(
                    0,
                    200,
                    255,
                    180 - i*40
                ),
                2
            )

            painter.setPen(pen)

            painter.drawEllipse(
                QPointF(cx,cy),
                size*r,
                size*r
            )



        # ----------------------
        # Rotating Energy Arcs
        # ----------------------

        painter.save()

        painter.translate(
            cx,
            cy
        )


        painter.rotate(
            self.angle
        )


        painter.setPen(
            QPen(
                QColor(
                    0,
                    240,
                    255
                ),
                5
            )
        )


        painter.drawArc(
            -size*0.22,
            -size*0.22,
            size*0.44,
            size*0.44,
            30*16,
            100*16
        )


        painter.drawArc(
            -size*0.30,
            -size*0.30,
            size*0.60,
            size*0.60,
            210*16,
            80*16
        )


        painter.restore()



        # ----------------------
        # Orbit particles
        # ----------------------

        painter.setPen(
            Qt.NoPen
        )


        for p in self.particles:


            angle = math.radians(
                p["angle"]
            )


            radius = (
                size *
                0.25
                +
                p["radius"]*0.3
            )


            x = (
                cx +
                math.cos(angle)
                *
                radius
            )

            y = (
                cy +
                math.sin(angle)
                *
                radius
            )


            painter.setBrush(
                QColor(
                    0,
                    220,
                    255,
                    160
                )
            )


            painter.drawEllipse(
                QPointF(x,y),
                p["size"],
                p["size"]
            )



        # ----------------------
        # Core
        # ----------------------

        gradient_size = size*0.12


        painter.setBrush(
            QColor(
                0,
                230,
                255,
                230
            )
        )


        painter.drawEllipse(
            QPointF(cx,cy),
            gradient_size,
            gradient_size
        )


        painter.setBrush(
            QColor(
                220,
                250,
                255
            )
        )


        painter.drawEllipse(
            QPointF(cx,cy),
            gradient_size*0.45,
            gradient_size*0.45
        )