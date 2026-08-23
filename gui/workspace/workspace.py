from gui.workspace.workspace_manager import WorkspaceManager
from gui.workspace.workspace_renderer import WorkspaceRenderer


class Workspace:

    def __init__(self):

        self.manager = WorkspaceManager()

        self.renderer = WorkspaceRenderer()

    # ------------------------

    def update(self):

        self.manager.update()

    # ------------------------

    def render(self, painter):

        self.renderer.render(

            painter,

            self.manager

        )