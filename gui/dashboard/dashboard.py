from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QTimer

from gui.dashboard.layout import DashboardLayout
from gui.common.effects.grid import Grid
from gui.common.effects.corner_hud import CornerHUD
from gui.components.top_status_bar import TopStatusBar

# Central AI core scene
from gui.scene.main_scene import MainScene
from gui.engine.renderer import Renderer


class Dashboard(QWidget):
    """
    Minimal AI workspace.

    The Dashboard intentionally contains only:
        - background HUD/grid
        - top status bar
        - central AI core

    Tools, utility panels, weather, music, tasks, notifications, etc.
    are deliberately kept out of this workspace and will live in the
    separate Tool Space later.
    """

    def __init__(self, brain=None):
        super().__init__()

        self.brain = brain

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.layoutEngine = DashboardLayout()
        self.topStatusBar = TopStatusBar()

        # Central AI core
        self.scene = MainScene()
        self.renderer = Renderer()

        # Keep the core animated at ~60 FPS.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    # ---------------------------------------------------------
    # FRAME LOOP
    # ---------------------------------------------------------

    def _tick(self):
        self.scene.update()
        self.update()

    # ---------------------------------------------------------
    # PAINT
    # ---------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        width = self.width()
        height = self.height()

        self.layoutEngine.calculate(width, height)

        # Background stays subtle. The AI core is the visual focus.
        Grid.draw(painter, self.rect())
        CornerHUD.draw(painter, self.rect())

        # Top status layer
        self.topStatusBar.draw(painter, width)

        # Central AI core
        painter.save()
        self.renderer.render(painter, self.scene)
        painter.restore()

        painter.end()
