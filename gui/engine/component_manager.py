class ComponentManager:

    def __init__(self):

        self.components = []

    # -------------------------

    def add(self, component, owner):

        print(component)
        print(type(component))
        print(hasattr(component, "attach"))

        component.attach(owner)

        component.start()

        self.components.append(component)

    # -------------------------

    def remove(self, componentType):

        self.components = [

            c for c in self.components

            if not isinstance(

                c,

                componentType

            )

        ]

    # -------------------------

    def get(self, componentType):

        for component in self.components:

            if isinstance(

                component,

                componentType

            ):

                return component

        return None

    # -------------------------

    def update(self):

        for component in self.components:

            if component.enabled:

                component.update()

    # -------------------------

    def render(self, painter):

        for component in self.components:

            if component.enabled:

                component.render(painter)