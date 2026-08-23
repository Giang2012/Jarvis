from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPainter, QPen
from math import sin, cos, radians


class ReactorRing:

    def __init__(
        self,
        radius=85,
        speed=1.0,
        tilt=0.45,
        rotation=0
    ):

        self.radius = radius
        self.speed = speed
        self.tilt = tilt

        self.angle = rotation

    # ----------------------------------

    def update(self):

        # Không xoay.
        # Ring chỉ đứng như HUD cố định.
        self.angle = 0

    # ----------------------------------

    def draw(self, painter: QPainter):

        painter.save()

        painter.rotate(self.angle)

        pen = QPen(
            QColor(
                150,
                255,
                255,
                150
            )
        )

        pen.setWidthF(1.2)

        painter.setPen(pen)

        painter.setBrush(
            QColor(0, 0, 0, 0)
        )

        painter.save()

        painter.scale(
            1.0,
            self.tilt
        )

        painter.drawEllipse(
            QPointF(0, 0),
            self.radius,
            self.radius
        )

        painter.restore()

        # --------------------------------
        # Orbit particles
        # --------------------------------

        for i in range(3):

            a = radians(
                self.angle * 1.5
                + i * 120
            )

            x = cos(a) * self.radius
            y = (
                sin(a)
                * self.radius
                * self.tilt
            )

            painter.setPen(
                QPen(
                    QColor(
                        210,
                        255,
                        255,
                        220
                    ),
                    2
                )
            )

            painter.drawPoint(
                QPointF(x, y)
            )

        painter.restore()