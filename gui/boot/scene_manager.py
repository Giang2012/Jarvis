from PySide6.QtCore import QObject, Signal, QTimer


class SceneManager(QObject):

    sceneChanged = Signal(int)
    finished = Signal()

    def __init__(self):
        super().__init__()

        self.scene = 0

        self.timeline = [

            1200,   # Black

            4500,   # Logo

            4500,   # Reactor

            10000,   # Suit

            5000,   # System

            1800    # Fade

        ]

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.nextScene
        )

    def start(self):

        self.scene = 0

        self.sceneChanged.emit(0)

        self.timer.start(
            self.timeline[0]
        )

    def nextScene(self):

        self.scene += 1

        if self.scene >= len(self.timeline):

            self.timer.stop()

            self.finished.emit()

            return

        self.sceneChanged.emit(
            self.scene
        )

        self.timer.start(
            self.timeline[self.scene]
        )
