from gui.workspace.workspace_object import WorkspaceObject

from gui.panels.weather_panel import WeatherPanel

from gui.workspace.components.drag_component import DragComponent
from gui.workspace.components.hover_component import HoverComponent


class WeatherObject(WorkspaceObject):

    def __init__(self):

        super().__init__(

            WeatherPanel()

        )

        self.addComponent(

            DragComponent()

        )

        self.addComponent(

            HoverComponent()

        )