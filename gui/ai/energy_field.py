from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtCore import QPointF

import math


class EnergyField:

    def __init__(self):

        self.time = 0.0

        self.layers = []

        # --------------------------------
        # Các lớp năng lượng 3D
        # --------------------------------

        for i in range(18):

            self.layers.append({

                "radius": 55 + i * 6.5,

                "depth": math.sin(i * 1.7),

                "phase": i * 0.7,

                "speed": 0.35 + (i % 4) * 0.08

            })

    # --------------------------------

    def update(self):

        self.time += 0.035

        # --------------------------------
        # Chuyển động depth
        # --------------------------------

        for layer in self.layers:

            layer["phase"] += layer["speed"]

            layer["depth"] = math.sin(
                layer["phase"]
            )

    # --------------------------------

    def draw(self, painter):

        painter.save()

        # --------------------------------
        # Pulse tổng
        # --------------------------------

        pulse = (
            math.sin(self.time * 2.5)
            * 5
        )

        # --------------------------------
        # Vẽ từ xa → gần
        # --------------------------------

        layers = sorted(
            self.layers,
            key=lambda x: x["depth"]
        )

        for layer in layers:

            depth = layer["depth"]

            radius = (
                layer["radius"]
                + pulse * (
                    0.4 + depth * 0.2
                )
            )

            # --------------------------------
            # Perspective
            # --------------------------------

            scale_x = (
                0.75
                + depth * 0.12
            )

            scale_y = (
                0.42
                + depth * 0.16
            )

            width = radius * scale_x
            height = radius * scale_y

            # --------------------------------
            # Depth alpha
            # --------------------------------

            alpha = int(
                8
                + (
                    depth + 1
                ) * 14
            )

            alpha = max(
                5,
                min(
                    35,
                    alpha
                )
            )

            # --------------------------------
            # Energy field
            # --------------------------------

            painter.setPen(
                QPen(
                    QColor(
                        0,
                        230,
                        255,
                        alpha + 20
                    ),
                    1
                )
            )

            painter.setBrush(
                QColor(
                    0,
                    220,
                    255,
                    alpha
                )
            )

            painter.drawEllipse(
                QPointF(
                    0,
                    depth * 8
                ),
                width,
                height
            )

        # --------------------------------
        # Core atmosphere
        # --------------------------------

        for i in range(12):

            radius = (
                35
                + i * 10
                + pulse
            )

            alpha = max(
                2,
                30 - i * 2
            )

            painter.setPen(
                QPen(
                    QColor(
                        0,
                        255,
                        255,
                        alpha
                    ),
                    1
                )
            )

            painter.setBrush(
                QColor(
                    0,
                    255,
                    255,
                    max(
                        1,
                        alpha // 2
                    )
                )
            )

            painter.drawEllipse(
                QPointF(0, 0),
                radius,
                radius * 0.72
            )

        painter.restore()