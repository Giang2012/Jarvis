"""
services/weather_service.py

Weather Service
"""

from PySide6.QtCore import QObject, QTimer

from kernel.event_bus import event_bus

try:
    from kernel.events import WEATHER_UPDATED
except ImportError:
    WEATHER_UPDATED = "weather.updated"


class WeatherService(QObject):

    def __init__(self):

        super().__init__()

        self.timer = QTimer()

        self.timer.setInterval(1000 * 60 * 15)

        self.timer.timeout.connect(
            self.update_weather
        )

        self.data = {
            "city": "--",
            "temperature": "--",
            "condition": "--",
            "humidity": "--",
            "wind": "--"
        }

    # ==========================
    # Control
    # ==========================

    def start(self):

        self.timer.start()

        self.update_weather()

    def stop(self):

        self.timer.stop()

    # ==========================
    # Update
    # ==========================

    def update_weather(self):

        """
        TODO:
        OpenWeather
        Gemini
        WeatherAPI

        Hiện tại dùng dữ liệu mẫu.
        """

        self.data = {

            "city": "Ho Chi Minh",

            "temperature": "30°C",

            "condition": "Sunny",

            "humidity": "71%",

            "wind": "8 km/h"

        }

        event_bus.emit(
            WEATHER_UPDATED,
            self.data
        )

    # ==========================
    # Getter
    # ==========================

    def current(self):

        return self.data