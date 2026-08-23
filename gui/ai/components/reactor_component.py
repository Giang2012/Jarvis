from gui.engine.component import Component
from gui.boot.reactor.reactor import Reactor


class ReactorComponent(Component):

    def __init__(self):
        super().__init__()

        self.reactor = Reactor()

    def update(self):
        self.reactor.update()

    def render(self, painter):
        self.reactor.draw(painter)   # hoặc paint nếu Reactor của mày dùng paint()