from .particle import Particle


class Emitter:

    def __init__(self):

        self.particles = []

        for i in range(80):

            p = Particle()

            p.angle = i * 4.5

            self.particles.append(p)

    def update(self):

        for p in self.particles:

            p.update()