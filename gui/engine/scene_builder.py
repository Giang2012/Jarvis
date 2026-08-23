from gui.engine.scene import Scene

from gui.objects.weather_object import WeatherObject
from gui.objects.music_object import MusicObject
from gui.objects.calendar_object import CalendarObject
from gui.objects.system_object import SystemObject
from gui.objects.ai_object import AIObject


class SceneBuilder:

    def build(self):

        scene = Scene()

        scene.add(
            AIObject()
        )

        scene.add(
            WeatherObject()
        )

        scene.add(
            MusicObject()
        )

        scene.add(
            CalendarObject()
        )

        scene.add(
            SystemObject()
        )

        return scene