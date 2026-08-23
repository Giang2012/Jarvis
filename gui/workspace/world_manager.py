from gui.workspace.world import World


class WorldManager:

    def __init__(self):

        self.world = World()

    # ------------------------

    def add(self, obj):

        self.world.add(obj)

    # ------------------------

    def update(self):

        self.world.update()

    # ------------------------

    def render(self, painter):

        self.world.render(painter)