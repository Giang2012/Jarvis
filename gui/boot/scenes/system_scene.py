from PySide6.QtGui import (
    QColor,
    QFont,
    QPen
)
from PySide6.QtCore import Qt


class SystemScene:

    def __init__(self):

        self.index = 0
        self.counter = 0

        self.lines = [

            "INITIALIZING AI CORE...",
            "VOICE ENGINE .......... READY",
            "SYSTEM MONITOR ........ READY",
            "NETWORK ............... READY",
            "MEMORY ................ READY",
            "PLUGINS ............... READY",
            "J.A.R.V.I.S ONLINE"

        ]

    # ----------------------------------------

    def update(self):

        self.counter += 1

        if self.counter >= 40:

            self.counter = 0

            if self.index < len(self.lines):

                self.index += 1

    # ----------------------------------------

    def paint(self, p, rect):

        self.update()

        w = rect.width()
        h = rect.height()

        # ---------- GRID ----------

        pen = QPen(
            QColor(
                0,
                255,
                255,
                18
            )
        )

        p.setPen(pen)

        for x in range(0, w, 40):

            p.drawLine(x, 0, x, h)

        for y in range(0, h, 40):

            p.drawLine(0, y, w, y)

        # ---------- TITLE ----------

        p.setPen(
            QColor(
                0,
                255,
                255
            )
        )

        p.setFont(
            QFont(
                "Orbitron",
                30,
                QFont.Bold
            )
        )

        p.drawText(
            rect,
            Qt.AlignHCenter | Qt.AlignTop,
            "SYSTEM STARTUP"
        )

        # ---------- TERMINAL ----------

        p.setFont(
            QFont(
                "Consolas",
                15
            )
        )

        y = 180

        for i in range(self.index):

            color = QColor(
                0,
                255,
                180
            )

            if "ONLINE" in self.lines[i]:

                color = QColor(
                    255,
                    255,
                    255
                )

            p.setPen(color)

            p.drawText(
                120,
                y,
                self.lines[i]
            )

            y += 40

        # ---------- CURSOR ----------

        if self.index < len(self.lines):

            p.setPen(
                QColor(
                    0,
                    255,
                    255
                )
            )

            p.drawText(
                120,
                y,
                "_"
            )