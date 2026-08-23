from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPen
from math import sin, cos, radians
import random


class ReactorParticle:

    def __init__(self):

        self.time = 0.0
        self.particles = []

        random.seed(47)

        # ==========================================
        # DENSE PLASMA CLOUD
        # ==========================================

        # Hạt lõi rất dày
        for i in range(520):

            angle = random.uniform(0, 360)
            a = radians(angle)

            # Phần lớn hạt nằm gần tâm
            # sqrt giúp mật độ nhìn tự nhiên hơn
            radius = (
                random.random() ** 1.8
            ) * 115

            # Cloud hơi dẹt theo chiều ngang
            flatten = random.uniform(
                0.62,
                0.92
            )

            x = cos(a) * radius
            y = sin(a) * radius * flatten

            # Noise để phá hình tròn
            x += random.gauss(0, 12)
            y += random.gauss(0, 9)

            # Ép phần lớn hạt quay về vùng lõi
            if random.random() < 0.72:

                x *= random.uniform(
                    0.55,
                    0.82
                )

                y *= random.uniform(
                    0.55,
                    0.82
                )

            self.particles.append({

                "x": x,
                "y": y,

                "base_x": x,
                "base_y": y,

                "depth": random.uniform(
                    -1.0,
                    1.0
                ),

                "size": random.uniform(
                    0.45,
                    1.65
                ),

                "phase": random.uniform(
                    0,
                    6.28
                ),

                "speed": random.uniform(
                    0.55,
                    1.25
                ),

                "brightness": random.uniform(
                    0.45,
                    1.0
                )
            })

        # ==========================================
        # OUTER PLASMA / ENERGY SPECKS
        # ==========================================

        for i in range(90):

            angle = random.uniform(
                0,
                6.283
            )

            radius = random.uniform(
                80,
                145
            )

            x = cos(angle) * radius
            y = sin(angle) * radius * random.uniform(
                0.55,
                0.85
            )

            self.particles.append({

                "x": x,
                "y": y,

                "base_x": x,
                "base_y": y,

                "depth": random.uniform(
                    -1,
                    1
                ),

                "size": random.uniform(
                    0.5,
                    1.35
                ),

                "phase": random.uniform(
                    0,
                    6.28
                ),

                "speed": random.uniform(
                    0.35,
                    0.9
                ),

                "brightness": random.uniform(
                    0.35,
                    0.9
                )
            })

    # ==========================================

    def update(self):

        self.time += 0.035

        for i, particle in enumerate(
            self.particles
        ):

            phase = (
                particle["phase"]
                + self.time
                * particle["speed"]
            )

            # ==================================
            # CHAOTIC PLASMA MOVEMENT
            # ==================================

            particle["x"] = (
                particle["base_x"]

                + sin(
                    phase * 1.73
                    + i * 0.11
                ) * 3.8

                + cos(
                    phase * 0.61
                    + i * 0.07
                ) * 2.2
            )

            particle["y"] = (
                particle["base_y"]

                + cos(
                    phase * 1.41
                    + i * 0.13
                ) * 3.4

                + sin(
                    phase * 0.73
                    + i * 0.09
                ) * 2.0
            )

            # ==================================
            # DEPTH
            # ==================================

            particle["depth"] = sin(
                phase * 0.87
                + particle["base_x"] * 0.018
                + particle["base_y"] * 0.014
            )

    # ==========================================

    def draw(self, painter):

        painter.save()

        ordered = sorted(
            self.particles,
            key=lambda p: p["depth"]
        )

        for particle in ordered:

            depth = particle["depth"]

            scale = (
                0.55
                + (depth + 1.0) * 0.34
            )

            size = (
                particle["size"]
                * scale
            )

            brightness = (
                particle["brightness"]
            )

            # ==================================
            # DYNAMIC ALPHA
            # ==================================

            alpha = int(
                (
                    38
                    + (depth + 1.0) * 70
                )
                * brightness
            )

            alpha = max(
                18,
                min(165, alpha)
            )

            x = particle["x"]
            y = particle["y"]

            # ==================================
            # MAIN PARTICLE
            # ==================================

            painter.setPen(
                QPen(
                    QColor(
                        145,
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
                QPointF(x, y)
            )

            # ==================================
            # BRIGHT PLASMA PARTICLES
            # ==================================

            if brightness > 0.82:

                glow_alpha = int(
                    alpha * 0.30
                )

                painter.setPen(
                    QPen(
                        QColor(
                            100,
                            245,
                            255,
                            glow_alpha
                        ),
                        max(
                            2.0,
                            size * 3.2
                        )
                    )
                )

                painter.drawPoint(
                    QPointF(x, y)
                )

            # ==================================
            # VERY BRIGHT CORE SPECK
            # ==================================

            if (
                brightness > 0.94
                and abs(x) < 55
                and abs(y) < 40
            ):

                painter.setPen(
                    QPen(
                        QColor(
                            220,
                            255,
                            255,
                            min(
                                210,
                                alpha + 40
                            )
                        ),
                        max(
                            1.2,
                            size * 1.5
                        )
                    )
                )

                painter.drawPoint(
                    QPointF(x, y)
                )

        painter.restore()