from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor


class ModeManager(QObject):

    modeChanged = Signal(str)

    def __init__(self):

        super().__init__()

        self.current_mode = "CODING"

        self.themes = {

            "CODING": {
                "background": QColor("#05070A"),
                "accent": QColor("#00D8FF"),
            },

            "STUDY": {
                "background": QColor("#081018"),
                "accent": QColor("#7FCFFF"),
            },

            "GAMING": {
                "background": QColor("#0A0712"),
                "accent": QColor("#C77DFF"),
            },

            "RELAX": {
                "background": QColor("#101820"),
                "accent": QColor("#FFB86B"),
            },

            "DEFAULT": {
                "background": QColor("#05070A"),
                "accent": QColor("#00D8FF"),
            },
        }

    # =========================
    # MODE
    # =========================

    def setMode(self, mode: str):

        mode = str(mode).upper()

        if mode not in self.themes:
            mode = "DEFAULT"

        if mode == self.current_mode:
            return

        self.current_mode = mode

        self.modeChanged.emit(mode)

    # =========================
    # THEME
    # =========================

    def theme(self):
        return self.current_mode

    # =========================
    # COLORS
    # =========================

    def color(self):

        return self.themes[
            self.current_mode
        ]["accent"]

    def background(self):

        return self.themes[
            self.current_mode
        ]["background"]

    # =========================
    # LOADOUT
    # =========================

    def loadout(self):

        loadouts = {

            "CODING": [
                "AI_STATUS",
            ],

            "STUDY": [
                "AI_STATUS",
            ],

            "GAMING": [
                "MUSIC",
                "NOTIFICATION",
            ],

            "RELAX": [
                "MUSIC",
                "NOTIFICATION",
            ],

            "DEFAULT": []
        }

        return loadouts.get(
            self.current_mode,
            []
        )