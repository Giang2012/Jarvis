import math


class Particle:

    def __init__(self):

        self.x = 0

        self.y = 0

        self.angle = 0

        self.radius = 100

        self.speed = 2

        self.size = 3

    def update(self):

        self.angle += self.speed

        if self.angle >= 360:

            self.angle = 0

        self.x = math.cos(
            math.radians(self.angle)
        ) * self.radius

        self.y = math.sin(
            math.radians(self.angle)
        ) * self.radius