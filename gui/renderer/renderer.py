class Renderer:

    def __init__(self):

        self.effects = []

    def add(self, effect):

        self.effects.append(effect)

    def draw(self, painter):

        for effect in self.effects:

            effect.draw(painter)