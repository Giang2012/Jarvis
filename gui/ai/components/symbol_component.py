from gui.engine.component import Component
from gui.boot.reactor.symbols import ReactorSymbols


class SymbolComponent(Component):

    def __init__(self):

        super().__init__()

        self.symbols = ReactorSymbols()

    def update(self):

        self.symbols.update()

    def render(self, painter):

        self.symbols.draw(painter)