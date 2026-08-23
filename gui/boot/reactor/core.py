from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPen
from math import sin, cos
import random


class ReactorCore:

    def __init__(self):

        self.time = 0.0
        self.particles = []

        random.seed(91)

        # ==========================================
        # DENSE CORE PLASMA
        # ==========================================

        for i in range(320):

            # Phần lớn hạt tập trung cực gần tâm
            radius = (
                random.random() ** 2.4
            ) * 58

            angle = random.uniform(
                0.0,
                6.28318
            )

            x = cos(angle) * radius
            y = sin(angle) * radius * random.uniform(
                0.62,
                0.95
            )

            # phá hình tròn
            x += random.gauss(0, 5)
            y += random.gauss(0, 4)

            self.particles.append({
                "x": x,
                "y": y,

                "base_x": x,
                "base_y": y,

                "size": random.uniform(
                    0.6,
                    2.0
                ),

                "phase": random.uniform(
                    0,
                    6.28
                ),

                "speed": random.uniform(
                    0.7,
                    1.7
                ),

                "brightness": random.uniform(
                    0.35,
                    1.0
                )
            })

    # ==========================================

    def update(self):

        self.time += 0.045

        for i, p in enumerate(
            self.particles
        ):

            phase = (
                p["phase"]
                + self.time * p["speed"]
            )

            # Plasma chuyển động hỗn loạn
            p["x"] = (
                p["base_x"]
                + sin(
                    phase * 1.9
                    + i * 0.17
                ) * 4.0
                + cos(
                    phase * 0.73
                    + i * 0.11
                ) * 2.0
            )

            p["y"] = (
                p["base_y"]
                + cos(
                    phase * 1.6
                    + i * 0.13
                ) * 3.5
                + sin(
                    phase * 0.61
                    + i * 0.09
                ) * 2.0
            )

    # ==========================================

    def draw(self, painter):

        painter.save()

        # ==========================================
        # INNER PLASMA PARTICLES
        # ==========================================

        for i, p in enumerate(
            self.particles
        ):

            brightness = p["brightness"]

            pulse = (
                0.72
                + 0.28 * sin(
                    self.time * 2.5
                    + p["phase"]
                )
            )

            alpha = int(
                45
                + brightness
                * 150
                * pulse
            )

            alpha = max(
                25,
                min(220, alpha)
            )

            size = (
                p["size"]
                * (
                    0.75
                    + brightness * 0.55
                )
            )

            # --------------------------------------
            # glow
            # --------------------------------------

            if brightness > 0.72:

                painter.setPen(
                    QPen(
                        QColor(
                            80,
                            240,
                            255,
                            int(alpha * 0.22)
                        ),
                        max(
                            2.0,
                            size * 3.5
                        )
                    )
                )

                painter.drawPoint(
                    QPointF(
                        p["x"],
                        p["y"]
                    )
                )

            # --------------------------------------
            # particle
            # --------------------------------------

            painter.setPen(
                QPen(
                    QColor(
                        165,
                        250,
                        255,
                        alpha
                    ),
                    max(
                        1.0,
                        size
                    )
                )
            )

            painter.drawPoint(
                QPointF(
                    p["x"],
                    p["y"]
                )
            )

        # ==========================================
        # WHITE ENERGY CENTER
        # ==========================================

        pulse = (
            1.0
            + sin(self.time * 3.0) * 0.08
        )

        # Không dùng ellipse/ring.
        # Chỉ dùng các điểm cực sáng ở tâm.

        for i in range(70):

            angle = (
                i * 2.399
                + self.time * 0.4
            )

            radius = (
                (i / 70.0) ** 1.8
            ) * 18 * pulse

            x = cos(angle) * radius
            y = sin(angle) * radius * 0.65

            alpha = int(
                210
                - (i / 70.0) * 150
            )

            painter.setPen(
                QPen(
                    QColor(
                        220,
                        255,
                        255,
                        alpha
                    ),
                    max(
                        1.0,
                        2.0 - i / 55
                    )
                )
            )

            painter.drawPoint(
                QPointF(x, y)
            )

        # ==========================================
        # HOT WHITE CORE
        # ==========================================

        for i in range(24):

            angle = (
                i * 2.618
                + self.time
            )

            radius = (
                i / 24.0
            ) * 7

            x = cos(angle) * radius
            y = sin(angle) * radius

            painter.setPen(
                QPen(
                    QColor(
                        245,
                        255,
                        255,
                        220 - i * 5
                    ),
                    2.2
                )
            )

            painter.drawPoint(
                QPointF(x, y)
            )

        painter.restore()