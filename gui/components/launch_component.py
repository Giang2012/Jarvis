from gui.engine.component import Component


class LaunchComponent(Component):

    def __init__(self):

        super().__init__()

        self.progress = 0.0

        self.speed = 0.04

        self.running = False

    # --------------------------------

    def launch(self):

        self.progress = 0.0

        self.running = True

    # --------------------------------

    def update(self):

        if not self.running:

            return

        self.progress += self.speed

        if self.progress >= 1:

            self.progress = 1

            self.running = False

    # --------------------------------

    def render(self, painter):

        pass