from gui.engine.component import Component
from gui.boot.reactor.electric import ElectricBolt


class ElectricComponent(Component):

    def __init__(self):

        super().__init__()

        self.bolts = [

            ElectricBolt(),

            ElectricBolt(),

            ElectricBolt(),

            ElectricBolt()

        ]

    def update(self):

        for bolt in self.bolts:

            bolt.update()

    def render(self,painter):

        for bolt in self.bolts:

            bolt.draw(painter)