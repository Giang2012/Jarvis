from PySide6.QtGui import (
    QColor,
    QFont,
    QPen,
    QLinearGradient
)
from PySide6.QtCore import Qt


class LogoScene:

    def __init__(self):

        self.alpha = 0
        self.scanX = -500

    # --------------------------------

    def update(self):

        if self.alpha < 255:
            self.alpha += 2

        self.scanX += 8

    # --------------------------------

    def paint(self, p, rect):

        self.update()

        w = rect.width()
        h = rect.height()

        # ==========================
        # LOGO GLOW
        # ==========================

        for i in range(12):

            pen = QPen(
                QColor(
                    0,
                    220,
                    255,
                    max(0, self.alpha // 8 - i * 2)
                )
            )

            pen.setWidth(1)

            p.setPen(pen)

            font = QFont(
                "Orbitron",
                40 + i,
                QFont.Bold
            )

            p.setFont(font)

            p.drawText(
                rect,
                Qt.AlignCenter,
                "STARK INDUSTRIES"
            )

        # ==========================
        # MAIN LOGO
        # ==========================

        p.setPen(
            QColor(
                220,
                255,
                255,
                self.alpha
            )
        )

        p.setFont(
            QFont(
                "Orbitron",
                42,
                QFont.Bold
            )
        )

        p.drawText(
            rect,
            Qt.AlignCenter,
            "STARK INDUSTRIES"
        )

        # ==========================
        # SUBTITLE
        # ==========================

        p.setPen(
            QColor(
                0,
                220,
                255,
                self.alpha
            )
        )

        p.setFont(
            QFont(
                "Consolas",
                12
            )
        )

        p.drawText(
            0,
            h // 2 + 55,
            w,
            30,
            Qt.AlignCenter,
            "ARTIFICIAL INTELLIGENCE DEFENSE SYSTEM"
        )

        # ==========================
        # SCAN LINE
        # ==========================

        gradient = QLinearGradient(
            self.scanX,
            0,
            self.scanX + 220,
            0
        )

        gradient.setColorAt(
            0,
            QColor(0, 0, 0, 0)
        )

        gradient.setColorAt(
            0.5,
            QColor(0, 255, 255, 120)
        )

        gradient.setColorAt(
            1,
            QColor(0, 0, 0, 0)
        )

        p.fillRect(
            rect,
            gradient
        )