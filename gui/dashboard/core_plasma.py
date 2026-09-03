import math
import random

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QRadialGradient


class CorePlasma:

    def __init__(self):

        rng = random.Random(91827)

        self.particles = []

        for _ in range(220):

            theta = rng.random() * math.tau
            phi = math.acos(
                2.0 * rng.random() - 1.0
            )

            radius = (
                0.78
                + rng.random() * 0.22
            )

            self.particles.append(
                {
                    "theta": theta,
                    "phi": phi,
                    "radius": radius,
                    "size": 0.8 + rng.random() * 2.4,
                    "speed": 0.35 + rng.random() * 1.15,
                    "phase": rng.random() * math.tau,
                }
            )

        self.time = 0.0

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, dt=0.016):

        self.time += dt

    # =========================================================
    # ATMOSPHERE
    # =========================================================

    def draw_atmosphere(
        self,
        painter,
        cx,
        cy,
        radius
    ):

        painter.save()

        # Soft layered energy field.
        gradient = QRadialGradient(
            QPointF(cx, cy),
            radius * 1.15
        )

        gradient.setColorAt(
            0.00,
            QColor(255, 255, 255, 235)
        )

        gradient.setColorAt(
            0.08,
            QColor(70, 235, 255, 205)
        )

        gradient.setColorAt(
            0.32,
            QColor(0, 170, 255, 80)
        )

        gradient.setColorAt(
            0.68,
            QColor(0, 90, 180, 25)
        )

        gradient.setColorAt(
            1.00,
            QColor(0, 0, 0, 0)
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)

        painter.drawEllipse(
            QRectF(
                cx - radius * 1.18,
                cy - radius * 1.18,
                radius * 2.36,
                radius * 2.36,
            )
        )

        # Smooth energy shells.
        for factor, alpha, width in (
            (1.00, 110, 2.2),
            (0.91, 80, 1.3),
            (0.78, 55, 1.0),
        ):

            painter.setBrush(Qt.NoBrush)

            painter.setPen(
                QPen(
                    QColor(
                        60,
                        235,
                        255,
                        alpha
                    ),
                    width
                )
            )

            painter.drawEllipse(
                QRectF(
                    cx - radius * factor,
                    cy - radius * factor,
                    radius * 2.0 * factor,
                    radius * 2.0 * factor,
                )
            )

        painter.restore()

    # =========================================================
    # PARTICLES
    # =========================================================

    def draw_particles(
        self,
        painter,
        cx,
        cy,
        radius,
        front_only=False
    ):

        painter.save()

        for p in self.particles:

            theta = (
                p["theta"]
                + self.time * p["speed"] * 0.35
            )

            phi = (
                p["phi"]
                + math.sin(
                    self.time * 0.8
                    + p["phase"]
                ) * 0.035
            )

            # Spherical projection with a subtle breathing shell.
            breathing = (
                1.0
                + math.sin(
                    self.time * 1.8
                    + p["phase"]
                ) * 0.025
            )

            r = (
                radius
                * p["radius"]
                * breathing
            )

            x3 = (
                r
                * math.sin(phi)
                * math.cos(theta)
            )

            y3 = (
                r
                * math.cos(phi)
            )

            z3 = (
                r
                * math.sin(phi)
                * math.sin(theta)
            )

            depth = (
                z3 / max(radius, 1.0)
            )

            if front_only and depth < -0.05:
                continue

            if (
                not front_only
                and depth > 0.20
            ):
                continue

            # Slight perspective scale.
            size = (
                p["size"]
                * (
                    0.70
                    + (depth + 1.0) * 0.35
                )
            )

            alpha = int(
                70
                + max(
                    0.0,
                    depth
                ) * 150
            )

            painter.setPen(Qt.NoPen)
            painter.setBrush(
                QColor(
                    130,
                    245,
                    255,
                    alpha
                )
            )

            painter.drawEllipse(
                QPointF(
                    cx + x3,
                    cy + y3
                ),
                size,
                size
            )

        painter.restore()

    # =========================================================
    # ELECTRIC FILAMENTS
    # =========================================================

    def draw_filaments(
        self,
        painter,
        cx,
        cy,
        radius
    ):

        painter.save()

        for band in range(7):

            points = []

            phase = (
                self.time * (
                    0.45
                    + band * 0.035
                )
                + band * 0.8
            )

            for i in range(25):

                t = i / 24.0

                angle = (
                    t * math.tau
                    + phase
                )

                wobble = (
                    math.sin(
                        angle * 3.0
                        + self.time * 2.0
                        + band
                    )
                    * radius
                    * 0.055
                )

                rr = (
                    radius * (
                        0.72
                        + 0.16 * math.sin(
                            angle * 2.0
                            + band
                        )
                    )
                    + wobble
                )

                points.append(
                    QPointF(
                        cx + math.cos(angle) * rr,
                        cy + math.sin(angle) * rr * 0.82,
                    )
                )

            painter.setPen(
                QPen(
                    QColor(
                        50,
                        220,
                        255,
                        35
                    ),
                    1
                )
            )

            for a, b in zip(
                points,
                points[1:]
            ):

                painter.drawLine(
                    a,
                    b
                )

        painter.restore()
