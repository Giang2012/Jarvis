from PySide6.QtCore import QRect


class DashboardLayout:
    """
    Layout for the minimal AI workspace.

    There are intentionally no dashboard panels here.
    The available space below the top bar belongs to the AI core.
    """

    def __init__(self):
        self.topOffset = 78
        self.bottomMargin = 18
        self.coreSize = 620

        self.center = QRect()

    def calculate(self, width, height):
        availableTop = self.topOffset
        availableHeight = max(1, height - availableTop - self.bottomMargin)

        size = min(
            self.coreSize,
            max(260, min(width - 40, availableHeight - 20))
        )

        x = (width - size) // 2
        y = availableTop + (availableHeight - size) // 2

        self.center = QRect(x, y, size, size)
