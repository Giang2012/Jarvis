from gui.engine.component import Component
from gui.boot.reactor.bloom import ReactorBloom


class BloomComponent(Component):

    def __init__(self):

        super().__init__()

        self.bloom = ReactorBloom()

    def update(self):

        pass

    def render(self, painter):

        self.bloom.draw(painter)