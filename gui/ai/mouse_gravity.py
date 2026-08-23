from PySide6.QtCore import QPointF
import math


class MouseGravity:

    def __init__(self):

        self.mouse = QPointF(0, 0)

        self.radius = 180

        self.force = 0.12

    # -----------------------

    def setMouse(self, pos):

        self.mouse = pos

    # -----------------------

    def apply(self, particle):

        dx = self.mouse.x() - particle.pos.x()

        dy = self.mouse.y() - particle.pos.y()

        dist = math.sqrt(dx*dx + dy*dy)

        if dist > self.radius:

            return

        strength = (1 - dist/self.radius) * self.force

        particle.pos.setX(
            particle.pos.x() + dx * strength
        )

        particle.pos.setY(
            particle.pos.y() + dy * strength
        )