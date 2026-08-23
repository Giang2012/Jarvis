from gui.engine.component import Component
from gui.boot.reactor.particle import ReactorParticle


class ParticleComponent(Component):

    def __init__(self):

        super().__init__()

        self.particle = ReactorParticle()

    def update(self):

        self.particle.update()

    def render(self, painter):

        self.particle.draw(painter)