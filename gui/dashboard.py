from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QGridLayout,
)

from gui.widgets.left_panel import LeftPanel
from gui.widgets.central_panel import CentralPanel
from gui.widgets.right_panel import RightPanel
from gui.widgets.hud_background import HUDBackground


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
        QWidget{
            background:#05070A;
        }
        """)

        self.background = HUDBackground()

        self.left = LeftPanel()
        self.center = CentralPanel()
        self.right = RightPanel()

        container = QWidget()

        layout = QHBoxLayout(container)

        layout.setContentsMargins(25,25,25,25)
        layout.setSpacing(20)

        layout.addWidget(self.left,1)
        layout.addWidget(self.center,3)
        layout.addWidget(self.right,1)

        root = QGridLayout(self)

        root.setContentsMargins(0,0,0,0)

        root.addWidget(self.background,0,0)
        root.addWidget(container,0,0)