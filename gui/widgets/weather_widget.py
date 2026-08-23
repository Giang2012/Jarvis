from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout

from gui.widgets.glass_card import GlassCard

from kernel.event_bus import event_bus
from kernel.events import WEATHER_UPDATED


class WeatherWidget(GlassCard):

    def __init__(self):
        super().__init__()

        self.setMinimumHeight(170)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(6)

        title = QLabel("🌤 WEATHER")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
        QLabel{
            color:#00E5FF;
            font-size:15px;
            font-weight:bold;
            background:transparent;
        }
        """)

        self.city = QLabel("--")
        self.temp = QLabel("--°")
        self.condition = QLabel("--")

        self.city.setAlignment(Qt.AlignCenter)
        self.temp.setAlignment(Qt.AlignCenter)
        self.condition.setAlignment(Qt.AlignCenter)

        self.city.setStyleSheet("""
        QLabel{
            color:white;
            font-size:16px;
            background:transparent;
        }
        """)

        self.temp.setStyleSheet("""
        QLabel{
            color:#00E5FF;
            font-size:34px;
            font-weight:bold;
            background:transparent;
        }
        """)

        self.condition.setStyleSheet("""
        QLabel{
            color:#9CCFFF;
            font-size:14px;
            background:transparent;
        }
        """)

        layout.addWidget(title)
        layout.addWidget(self.city)
        layout.addWidget(self.temp)
        layout.addWidget(self.condition)

        event_bus.subscribe(
            WEATHER_UPDATED,
            self.update_weather
        )

    def update_weather(self, data):

        self.city.setText(data["city"])
        self.temp.setText(f'{data["temperature"]}°')
        self.condition.setText(data["condition"])