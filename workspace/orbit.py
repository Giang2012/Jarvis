import math


class Orbit:

    def __init__(self,radius,speed):

        self.radius = radius

        self.speed = speed

        self.angle = 0

    def update(self):

        self.angle += self.speed

    def position(self,cx,cy):

        x = cx + math.cos(self.angle)*self.radius

        y = cy + math.sin(self.angle)*self.radius

        return x,y