class Component:

    def __init__(self):

        self.owner = None

        self.enabled = True

    # --------------------------------

    def attach(self, owner):

        self.owner = owner

    # --------------------------------

    def start(self):

        pass

    # --------------------------------

    def update(self):

        pass

    # --------------------------------

    def render(self, painter):

        pass

    # --------------------------------

    def destroy(self):

        pass