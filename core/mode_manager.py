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

    def setMode(self, mode: str):
        mode = mode.upper()

        if mode not in self.themes:
            mode = "DEFAULT"

        self.current_mode = mode
        self.modeChanged.emit(mode)

    def theme(self):
        return self.current_mode

    def color(self):
        return self.themes[self.current_mode]["accent"]