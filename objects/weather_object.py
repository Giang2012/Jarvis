from gui.engine.object import SceneObject

from gui.panels.weather_panel import WeatherPanel


class WeatherObject(SceneObject):

    def __init__(self):

        super().__init__()

        self.panel = WeatherPanel()

    # ------------------------

    def render(self, painter):

        self.panel.paint(

            painter,

            self.transform.position.x(),

            self.transform.position.y()

        )