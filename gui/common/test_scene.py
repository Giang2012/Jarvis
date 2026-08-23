from PySide6.QtWidgets import QWidget

from PySide6.QtCore import QTimer

from PySide6.QtGui import QPainter

from gui.renderer.glow import Glow
from gui.renderer.scanline import Scanline

from gui.particles.emitter import Emitter
from gui.particles.orbit import OrbitRenderer

class TestScene(QWidget):

    def __init__(self):

        super().__init__()

        self.glow = Glow()

        self.scan = Scanline()

        self.timer = QTimer()

        self.timer.timeout.connect(self.animate)

        self.timer.start(16)

        self.emitter = Emitter()

        self.orbit = OrbitRenderer()
    def animate(self):

        self.scan.update()

        self.update()

        self.emitter.update()

    def paintEvent(self,e):

        p = QPainter(self)

        p.setRenderHint(QPainter.Antialiasing)

        p.translate(

            self.width()/2,

            self.height()/2

        )

        self.glow.draw(p)

        self.scan.draw(p)
        self.orbit.draw(

            p,

            self.emitter.particles

        )