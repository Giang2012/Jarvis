from gui.engine.object import Object

class WorkspaceObject(Object):

    def __init__(self):

        super().__init__()

        self.selected = False

        self.visible = True

    # ------------------------

    def update(self):

        super().update()

    # ------------------------

    def render(self, painter):

        super().render(painter)