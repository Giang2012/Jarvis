from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QPainter

from gui.boot.scene_manager import SceneManager

from gui.boot.scenes.black_scene import BlackScene
from gui.boot.scenes.logo_scene import LogoScene
from gui.boot.scenes.reactor_scene import ReactorScene
from gui.boot.scenes.suit_scene import SuitScene
from gui.boot.scenes.system_scene import SystemScene
from gui.boot.scenes.fade_scene import FadeScene


class BootScreen(QWidget):

    bootFinished = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.setStyleSheet("""
            background:#000000;
        """)

        # -----------------------------
        # Scene Manager
        # -----------------------------

        self.manager = SceneManager()

        self.scenes = [
            BlackScene(),
            LogoScene(),
            ReactorScene(),
            SuitScene(),
            SystemScene(),
            FadeScene()
        ]

        self.currentScene = self.scenes[0]

        self.manager.sceneChanged.connect(self.changeScene)
        self.manager.finished.connect(self.bootFinished)

        # -----------------------------
        # Render Timer
        # -----------------------------

        self.renderTimer = QTimer(self)
        self.renderTimer.timeout.connect(self.update)
        self.renderTimer.start(16)

        self.manager.start()

    # --------------------------------

    def changeScene(self, index):

        print(index, type(self.scenes[index]).__name__)

        self.currentScene = self.scenes[index]

        self.update()

    # --------------------------------

    def paintEvent(self, event):


        painter = QPainter(self)

        painter.fillRect(
            self.rect(),
            Qt.black
        )

        if self.currentScene:

            self.currentScene.paint(
                painter,
                self.rect()
            )

        painter.end()

    # --------------------------------

    def resizeEvent(self, event):

        super().resizeEvent(event)
    def finishBoot(self):

        self.renderTimer.stop()

        self.close()

        self.bootFinished.emit()