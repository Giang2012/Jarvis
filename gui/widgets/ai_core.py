from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, Qt, QSize
from PySide6.QtGui import QPainter, QColor, QPen
import math


class AICore(QWidget):

    def __init__(self, mode_manager):
        super().__init__()

        self.mode_manager = mode_manager
        self.angle = 0
        self.state = "READY"

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    def setState(self, state: str):
        self.state = state
        self.update()

    def animate(self):
        self.angle += 2
        if self.angle >= 360:
            self.angle = 0
        self.update()

    def _state_color(self):
        if self.state == "LISTENING":
            return QColor("#4DFFB5")
        if self.state == "THINKING":
            return QColor("#FFD166")
        if self.state == "EXECUTING":
            return QColor("#FF7A7A")
        if self.state == "SPEAKING":
            return QColor("#C77DFF")
        return QColor("#00D8FF")

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h / 2

        p.translate(cx, cy)

        base = self._state_color()

        pen = QPen(base)
        pen.setWidth(4)
        p.setPen(pen)
        p.rotate(self.angle)
        p.drawEllipse(-120, -120, 240, 240)

        p.rotate(-self.angle * 2)
        pen.setColor(QColor(base.red(), base.green(), base.blue(), 180))
        pen.setWidth(2)
        p.setPen(pen)
        p.drawEllipse(-90, -90, 180, 180)

        p.setPen(Qt.NoPen)
        p.setBrush(base)
        p.drawEllipse(-12, -12, 24, 24)

        p.setBrush(QColor(base.red(), base.green(), base.blue(), 35))
        p.drawEllipse(-60, -60, 120, 120)

    def sizeHint(self):
        return QSize(600, 600)