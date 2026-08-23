from gui.workspace.workspace_object import WorkspaceObject

from gui.components.launch_component import LaunchComponent

class ChromeObject(WorkspaceObject):

    def __init__(self):

        super().__init__()

        self.launchComponent = LaunchComponent()

        self.name = "Chrome"

    # ------------------------

    def update(self):

        super().update()

        self.launchComponent.update()

    # ------------------------

    def render(self, painter):

        super().render(painter)

    def launch(self):

        self.launchComponent.launch()