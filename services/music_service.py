"""
services/music_service.py
"""

from PySide6.QtCore import QObject

from kernel.event_bus import event_bus

try:
    from kernel.events import MUSIC_UPDATED
except ImportError:
    MUSIC_UPDATED = "music.updated"


class MusicService(QObject):

    def __init__(self):

        super().__init__()

        self.track = {
            "title": "Nothing Playing",
            "artist": "",
            "duration": 0,
            "position": 0,
            "playing": False
        }

    def play(self):

        self.track["playing"] = True
        event_bus.emit(
            MUSIC_UPDATED,
            self.track
        )

    def pause(self):

        self.track["playing"] = False
        event_bus.emit(
            MUSIC_UPDATED,
            self.track
        )

    def set_track(
        self,
        title,
        artist
    ):

        self.track["title"] = title
        self.track["artist"] = artist

        event_bus.emit(
            MUSIC_UPDATED,
            self.track
        )

    def current(self):

        return self.track