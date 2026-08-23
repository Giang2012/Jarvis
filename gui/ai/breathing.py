import math


class Breathing:

    def __init__(self):

        self.time = 0

        self.value = 1

    # --------------------------

    def update(self):

        self.time += 0.02

        self.value = 1 + math.sin(

            self.time

        ) * 0.015

    # --------------------------

    def get(self):

        return self.value