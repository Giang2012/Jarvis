import math


class HeartBeat:

    def __init__(self):

        self.time = 0

        self.scale = 1

    # --------------------------

    def update(self):

        self.time += 0.05

        self.scale = 1 + math.sin(

            self.time * 2

        ) * 0.03

    # --------------------------

    def getScale(self):

        return self.scale