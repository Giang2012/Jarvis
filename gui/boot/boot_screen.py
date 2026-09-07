from __future__ import annotations

import math
import random

from PySide6.QtCore import Qt, QTimer, Signal, QPointF, QRectF
from PySide6.QtGui import QPainter, QPen, QBrush, QFont, QColor, QLinearGradient
from PySide6.QtWidgets import QWidget

from gui.boot.suit.armor_3d_widget import Armor3DWidget


class BootScreen(QWidget):
    """
    JARVIS V2 cinematic boot.

    This replaces the old SceneManager-based boot with one continuous timeline:
      0.00 - 0.90s  cold start / diagnostics
      0.90 - 2.10s  reactor ignition
      2.10 - 5.90s  armor assembly
      5.90 - 7.20s  HUD lock / system online
      7.20 - 7.90s  transition to main UI

    ESC skips the boot.
    """

    bootFinished = Signal()

    DURATION = 7.9

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)
        self.showFullScreen()

        self.t = 0.0
        self.last_ms = 0
        self.finished = False
        self.rng = random.Random(42)

        # Real OpenGL 3D armor scene. It is deliberately a child overlay so the
        # cinematic HUD/background remains QPainter-based and stable.
        self.armor3d = Armor3DWidget(self)
        self.armor3d.setGeometry(
            int(self.width() * 0.24),
            int(self.height() * 0.10),
            int(self.width() * 0.52),
            int(self.height() * 0.82),
        )
        self.armor3d.show()

        self.particles = [
            (
                self.rng.uniform(-1.0, 1.0),
                self.rng.uniform(-1.0, 1.0),
                self.rng.uniform(0.25, 1.0),
                self.rng.uniform(0.4, 1.5),
            )
            for _ in range(90)
        ]

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(16)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self._finish()
            return
        super().keyPressEvent(event)

    def _tick(self):
        self.t += 0.016
        if self.t >= self.DURATION:
            self._finish()
            return
        self.update()

    def _finish(self):
        if self.finished:
            return
        self.finished = True
        self.timer.stop()
        if hasattr(self, "armor3d"):
            self.armor3d.stop()
            self.armor3d.hide()
        self.close()
        self.bootFinished.emit()

    @staticmethod
    def _ease(x: float) -> float:
        x = max(0.0, min(1.0, x))
        return 1.0 - (1.0 - x) ** 4

    @staticmethod
    def _clamp(x: float) -> float:
        return max(0.0, min(1.0, x))

    def _segment(self, start: float, end: float) -> float:
        return self._ease(self._clamp((self.t - start) / (end - start)))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "armor3d"):
            self.armor3d.setGeometry(
                int(self.width() * 0.24),
                int(self.height() * 0.10),
                int(self.width() * 0.52),
                int(self.height() * 0.82),
            )

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)
        p.fillRect(self.rect(), QColor(2, 4, 7))

        w, h = self.width(), self.height()
        cx, cy = w * 0.5, h * 0.52
        scale = min(w / 1100.0, h / 900.0)

        self._draw_background(p, w, h, cx, cy, scale)
        self._draw_header(p, w, h)
        self._draw_hud(p, w, h)
        self._draw_footer(p, w, h)

        p.end()

    def _draw_background(self, p, w, h, cx, cy, s):
        # Technical grid
        p.setPen(QPen(QColor(18, 40, 52, 115), 1))
        grid = max(34, int(48 * s))
        for x in range(0, w + grid, grid):
            p.drawLine(x, 0, x, h)
        for y in range(0, h + grid, grid):
            p.drawLine(0, y, w, y)

        # Large concentric targeting rings
        ring = min(w, h) * 0.39
        for mul, alpha in ((1.0, 75), (0.72, 50), (0.43, 35)):
            p.setPen(QPen(QColor(36, 142, 174, alpha), 1))
            d = ring * mul
            p.drawEllipse(QPointF(cx, cy), d, d)

        # Moving sweep
        sweep = (self.t * 1.7) % (2 * math.pi)
        p.setPen(QPen(QColor(74, 203, 229, 90), 2))
        p.drawLine(
            QPointF(cx, cy),
            QPointF(
                cx + math.cos(sweep) * ring,
                cy + math.sin(sweep) * ring,
            ),
        )

        # Ambient particles
        for px, py, size, speed in self.particles:
            phase = (self.t * speed + px * 3.0) % 1.0
            x = cx + px * w * 0.48
            y = cy + py * h * 0.45 - phase * 16
            a = int(30 + 55 * (0.5 + 0.5 * math.sin(self.t * speed + px * 8)))
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(75, 185, 210, a))
            p.drawEllipse(QPointF(x, y), size, size)

    def _draw_header(self, p, w, h):
        font = QFont("Consolas", max(11, int(h / 72)))
        font.setLetterSpacing(QFont.AbsoluteSpacing, 3)

        p.setFont(font)
        p.setPen(QColor(121, 211, 230, 210))
        p.drawText(42, 58, "J.A.R.V.I.S // NEURAL DEFENSE INTERFACE")

        small = QFont("Consolas", max(8, int(h / 105)))
        small.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        p.setFont(small)
        p.setPen(QColor(89, 142, 157, 190))
        p.drawText(44, 82, "BOOT SEQUENCE  /  CORE 01  /  VISUAL SYSTEM ONLINE")

        p.drawText(w - 260, 58, "BUILD 1.0.0")
        p.drawText(w - 260, 82, "SECURE CHANNEL")

    def _draw_hud(self, p, w, h):
        lock = self._segment(5.05, 6.35)
        font = QFont("Consolas", max(9, int(h / 92)))
        p.setFont(font)

        # Left diagnostic stack
        labels = [
            ("NEURAL CORE", self._segment(0.2, 1.0)),
            ("POWER SYSTEM", self._segment(1.0, 1.8)),
            ("ARMOR MATRIX", self._segment(2.0, 4.8)),
            ("TARGETING", self._segment(4.2, 5.2)),
            ("JARVIS CORE", lock),
        ]
        y = int(h * 0.30)
        for label, amount in labels:
            p.setPen(QColor(103, 181, 199, int(90 + 130*amount)))
            p.drawText(48, y, f"[ {'ONLINE' if amount > .8 else 'SYNC'} ]  {label}")
            y += 28

        # Right system readout
        p.setPen(QColor(102, 180, 199, 210))
        x = w - 290
        y = int(h * 0.30)
        for line in (
            "VISUAL LINK      100%",
            "SERVO NETWORK    100%",
            "TACTICAL BUS     100%",
            "MEMORY INDEX     READY",
            "VOICE CORE       STANDBY",
        ):
            p.drawText(x, y, line)
            y += 28

        # Central lock reticle
        if lock > 0:
            r = min(w, h) * 0.19
            p.setPen(QPen(QColor(98, 211, 229, int(55 + 130*lock)), 1))
            p.drawArc(QRectF(w*.5-r, h*.52-r, 2*r, 2*r), 25*16, 90*16)
            p.drawArc(QRectF(w*.5-r, h*.52-r, 2*r, 2*r), 205*16, 90*16)
            p.drawLine(w*.5-r-16, h*.52, w*.5-r+5, h*.52)
            p.drawLine(w*.5+r-5, h*.52, w*.5+r+16, h*.52)

    def _draw_footer(self, p, w, h):
        progress = self._clamp(self.t / self.DURATION)

        p.setPen(QColor(76, 134, 150, 180))
        p.setFont(QFont("Consolas", max(8, int(h / 105))))
        p.drawText(44, h - 56, "INITIALIZING JARVIS")

        # Progress bar
        bar_x, bar_y, bar_w, bar_h = 44, h - 39, min(520, w * 0.32), 6
        p.setPen(QPen(QColor(47, 100, 116, 170), 1))
        p.setBrush(QColor(10, 23, 29))
        p.drawRect(QRectF(bar_x, bar_y, bar_w, bar_h))

        p.setPen(Qt.NoPen)
        p.setBrush(QColor(84, 197, 218, 210))
        p.drawRect(QRectF(bar_x, bar_y, bar_w * progress, bar_h))

        p.setPen(QColor(102, 181, 198, 210))
        p.drawText(bar_x + bar_w + 14, h - 35, f"{int(progress*100):03d}%")

        status = "SYSTEM ONLINE" if progress > 0.92 else "ASSEMBLING DEFENSE SYSTEM"
        p.drawText(w - 300, h - 35, status)
