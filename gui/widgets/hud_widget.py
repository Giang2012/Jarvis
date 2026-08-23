from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QTimer

from gui.common.effects.grid import Grid
from gui.common.effects.corner_hud import CornerHUD

from gui.common.hud.hud_ring import HUDRing
from gui.common.hud.hud_panel import HUDPanel
from gui.ai.ai_core import AICore


class HUDWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ring = HUDRing()

        self.aiCore = AICore()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    # ----------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # Background Grid
        Grid.draw(
            painter,
            self.rect()
        )

        # Corner HUD
        CornerHUD.draw(
            painter,
            self.rect()
        )

        # Reactor Ring
        painter.save()

        painter.translate(
            w // 2,
            h // 2
        )

        self.aiCore.draw(painter)

        painter.restore()

        # Left Panel
        HUDPanel.drawLeft(
            painter,
            35,
            90,
            250,
            260
        )

        # Right Panel
        HUDPanel.drawRight(
            painter,
            w - 285,
            90,
            250,
            260
        )