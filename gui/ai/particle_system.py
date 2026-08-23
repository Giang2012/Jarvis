from gui.ai.particle import Particle


class ParticleSystem:

    def __init__(self):

        self.gravity = None

        self.particles = [

            Particle()

            for _ in range(500)

        ]
    def setGravity(self, gravity):

        self.gravity = gravity

    # --------------------------

    def update(self):

        for p in self.particles:

            p.update()

            if self.gravity:

                self.gravity.apply(p)

    # --------------------------

    def draw(self, painter):

        self.update()

        for p in self.particles:

            p.draw(painter)

