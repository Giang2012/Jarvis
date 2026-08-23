from math import sin, cos, radians

from gui.engine.component import Component


class OrbitComponent(Component):

    def __init__(self, radius=250, speed=0.5, angle=0):

        super().__init__()

        self.radius = radius

        self.speed = speed

        self.angle = angle

        self.centerX = 0

        self.centerY = 0

    # ----------------------------

    def setCenter(self, x, y):

        self.centerX = x

        self.centerY = y

    # ----------------------------

    def update(self):

        self.angle += self.speed

        rad = radians(self.angle)

        x = self.centerX + cos(rad) * self.radius

        y = self.centerY + sin(rad) * self.radius

        self.owner.transform.setPosition(x, y)