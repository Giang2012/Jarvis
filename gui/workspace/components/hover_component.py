from gui.engine.component import Component


class HoverComponent(Component):

    def __init__(self):

        super().__init__()

        self.hover = False

    # ------------------------

    def enter(self):

        self.hover = True

        self.owner.transform.setScale(1.08)

    # ------------------------

    def leave(self):

        self.hover = False

        self.owner.transform.setScale(1.0)