"""
kernel/context.py

Global Runtime Context
"""

from typing import Dict, Any

from kernel.event_bus import event_bus
from kernel.events import (
    CPU_UPDATED,
    RAM_UPDATED,
    NETWORK_UPDATED,
    WEATHER_UPDATED,
    MUSIC_UPDATED,
    MODE_CHANGED,
    THEME_CHANGED,
)


class Context:

    def __init__(self):

        self.data: Dict[str, Any] = {

            "mode": "study",

            "theme": "iron_man",

            "cpu": 0,

            "ram": {},

            "network": {},

            "weather": {},

            "music": {},

            "conversation": [],

            "memory": []
        }

        event_bus.subscribe(
            CPU_UPDATED,
            self._cpu
        )

        event_bus.subscribe(
            RAM_UPDATED,
            self._ram
        )

        event_bus.subscribe(
            NETWORK_UPDATED,
            self._network
        )

        event_bus.subscribe(
            WEATHER_UPDATED,
            self._weather
        )

        event_bus.subscribe(
            MUSIC_UPDATED,
            self._music
        )

        event_bus.subscribe(
            MODE_CHANGED,
            self._mode
        )

        event_bus.subscribe(
            THEME_CHANGED,
            self._theme
        )

    # -------------------------

    def _cpu(self, value):

        self.data["cpu"] = value

    def _ram(self, value):

        self.data["ram"] = value

    def _network(self, value):

        self.data["network"] = value

    def _weather(self, value):

        self.data["weather"] = value

    def _music(self, value):

        self.data["music"] = value

    def _mode(self, value):

        self.data["mode"] = value

    def _theme(self, value):

        self.data["theme"] = value

    # -------------------------

    def add_message(
        self,
        role,
        message
    ):

        self.data["conversation"].append({

            "role": role,

            "message": message

        })

    def add_memory(self, memory):

        self.data["memory"].append(memory)

    def get(self, key):

        return self.data.get(key)

    def all(self):

        return self.data


context = Context()