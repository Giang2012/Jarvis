from .core import ReactorCore
from .particle import ReactorParticle
from .bloom import ReactorBloom


class Reactor:

    def __init__(self):

        # ==============================
        # CORE
        # ==============================

        self.core = ReactorCore()

        # ==============================
        # PLASMA PARTICLES
        # ==============================

        self.particle = ReactorParticle()

        # ==============================
        # BACKGROUND GLOW
        # ==============================

        self.bloom = ReactorBloom()


    # ==============================

    def update(self):

        self.core.update()
        self.particle.update()


    # ==============================

    def draw(self, painter):

        self.update()

        painter.save()

        # Background plasma glow
        self.bloom.draw(painter)

        # Dense free plasma particles
        self.particle.draw(painter)

        # Central reactor core
        self.core.draw(painter)

        painter.restore()