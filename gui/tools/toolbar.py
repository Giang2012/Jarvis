from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

from .tool_space import ToolSpace


class Toolbar(QWidget):
    """
    Compatibility facade for the new Tool Space.

    Existing code can import Toolbar while the actual implementation
    remains in the dedicated full-screen Tool Space.
    """

    backRequested = Signal()

    def __init__(self, brain=None, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.toolSpace = ToolSpace(brain=brain)
        self.toolSpace.backRequested.connect(self.backRequested.emit)

        layout.addWidget(self.toolSpace)
