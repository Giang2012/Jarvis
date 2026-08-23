from gui.engine.component import Component
from gui.boot.reactor.ring import ReactorRing


class RingComponent(Component):

    def __init__(self):

        super().__init__()

        self.rings = [

            ReactorRing(42,0.6),

            ReactorRing(60,-1),

            ReactorRing(82,1.5)

        ]

    def update(self):

        for ring in self.rings:

            ring.update()

    def render(self,painter):

        for ring in reversed(self.rings):

            ring.draw(painter)