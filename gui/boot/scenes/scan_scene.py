from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QPainter,
    QColor,
    QFont,
    QPen
)
from PySide6.QtCore import Qt, QTimer


class ScanScene(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scanY = -40

        self.progress = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    # -------------------------------------------------

    def animate(self):

        self.scanY += 6

        if self.scanY > self.height() + 40:

            self.scanY = -40

        if self.progress < 100:

            self.progress += 0.25

        self.update()

    # -------------------------------------------------

    def paintEvent(self, e):

        p = QPainter(self)

        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        # =======================================
        # GRID
        # =======================================

        pen = QPen(
            QColor(0,220,255,25)
        )

        p.setPen(pen)

        step = 40

        for x in range(0, w, step):

            p.drawLine(
                x,
                0,
                x,
                h
            )

        for y in range(0, h, step):

            p.drawLine(
                0,
                y,
                w,
                y
            )

        # =======================================
        # SCAN LINE
        # =======================================

        pen = QPen(
            QColor(0,255,255,180)
        )

        pen.setWidth(2)

        p.setPen(pen)

        p.drawLine(
            0,
            int(self.scanY),
            w,
            int(self.scanY)
        )

        # glow

        for i in range(10):

            pen = QPen(
                QColor(
                    0,
                    255,
                    255,
                    max(0,40-i*4)
                )
            )

            p.setPen(pen)

            p.drawLine(
                0,
                int(self.scanY+i),
                w,
                int(self.scanY+i)
            )

        # =======================================
        # TITLE
        # =======================================

        p.setPen(
            QColor(0,255,255)
        )

        p.setFont(
            QFont(
                "Orbitron",
                22,
                QFont.Bold
            )
        )

        p.drawText(
            60,
            80,
            "SYSTEM DIAGNOSTICS"
        )

        # =======================================
        # INFO
        # =======================================

        p.setFont(
            QFont(
                "Consolas",
                13
            )
        )

        infos = [

            "AI CORE ............. READY",

            "OPTICAL SENSOR ...... READY",

            "AUDIO ENGINE ........ READY",

            "NETWORK ............. READY",

            "VOICE MODULE ........ READY",

            "SECURITY ............ READY",

            f"BOOT PROGRESS ....... {int(self.progress)}%"

        ]

        y = 160

        for txt in infos:

            p.drawText(
                80,
                y,
                txt
            )

            y += 38

        # =======================================
        # RIGHT PANEL
        # =======================================

        p.drawRect(
            w-340,
            120,
            250,
            250
        )

        p.drawLine(
            w-215,
            120,
            w-215,
            370
        )

        p.drawLine(
            w-340,
            245,
            w-90,
            245
        )

        p.drawText(
            w-310,
            395,
            "BIOMETRIC SCAN"
        )