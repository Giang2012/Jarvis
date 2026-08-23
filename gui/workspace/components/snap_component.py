from gui.engine.component import Component


class SnapComponent(Component):

    def __init__(self):

        super().__init__()

        self.targetX = 0
        self.targetY = 0

    # ------------------------

    def setTarget(self, x, y):

        self.targetX = x
        self.targetY = y

    # ------------------------

    def update(self):

        pass