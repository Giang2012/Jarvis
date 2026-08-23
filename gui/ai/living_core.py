class LivingCore:

    def __init__(self):

        self.modules = []

    # -----------------------

    def add(self, module):

        self.modules.append(module)

    # -----------------------

    def update(self):

        for module in self.modules:

            if hasattr(module, "update"):

                module.update()

    # -----------------------

    def draw(self, painter):

        for module in self.modules:

            if hasattr(module, "draw"):

                module.draw(painter)