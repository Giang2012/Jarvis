from gui.engine.component import Component


class LaunchComponent(Component):

    def __init__(self):

        super().__init__()

        self.playing = False

    # ------------------------

    def launch(self):

        self.playing = True

    # ------------------------

    def update(self):

        if not self.playing:

            return