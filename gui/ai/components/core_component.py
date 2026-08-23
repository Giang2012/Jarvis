from gui.engine.component import Component
from gui.boot.reactor.core import ReactorCore


class CoreComponent(Component):

    def __init__(self):

        super().__init__()

        self.core = ReactorCore()

    def update(self):

        self.core.update()

    def render(self, painter):

        self.core.draw(painter)