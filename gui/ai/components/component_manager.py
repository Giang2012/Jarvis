class ComponentManager:

    def __init__(self):

        self.components = []

    # --------------------------

    def add(self, component):

        self.components.append(component)

        component.start()

    # --------------------------

    def update(self):

        for component in self.components:

            if component.enabled:

                component.update()

    # --------------------------

    def draw(self, painter):

        for component in self.components:

            if component.enabled:

                component.draw(painter)