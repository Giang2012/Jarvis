from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (
    QPainter,
    QColor,
    QPen,
    QFont
)
from PySide6.QtCore import Qt, QTimer


class AssembleScene(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.progress = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)

    # ------------------------------------------------

    def animate(self):

        if self.progress < 100:

            self.progress += 0.35

        self.update()

    # ------------------------------------------------

    def paintEvent(self, e):

        p = QPainter(self)

        p.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()

        cx = w // 2
        cy = h // 2

        pen = QPen(QColor(0,230,255))
        pen.setWidth(2)

        p.setPen(pen)

        # =====================================
        # HUD FRAME
        # =====================================

        p.drawRect(
            cx-180,
            cy-260,
            360,
            520
        )

        # =====================================
        # HEAD
        # =====================================

        if self.progress > 5:

            p.drawEllipse(
                cx-35,
                cy-210,
                70,
                70
            )

        # =====================================
        # CHEST
        # =====================================

        if self.progress > 20:

            p.drawRoundedRect(
                cx-65,
                cy-120,
                130,
                140,
                10,
                10
            )

        # =====================================
        # LEFT ARM
        # =====================================

        if self.progress > 40:

            p.drawLine(
                cx-65,
                cy-80,
                cx-135,
                cy+30
            )

        # =====================================
        # RIGHT ARM
        # =====================================

        if self.progress > 55:

            p.drawLine(
                cx+65,
                cy-80,
                cx+135,
                cy+30
            )

        # =====================================
        # BODY
        # =====================================

        if self.progress > 70:

            p.drawLine(
                cx,
                cy+20,
                cx,
                cy+130
            )

        # =====================================
        # LEFT LEG
        # =====================================

        if self.progress > 82:

            p.drawLine(
                cx,
                cy+130,
                cx-55,
                cy+235
            )

        # =====================================
        # RIGHT LEG
        # =====================================

        if self.progress > 90:

            p.drawLine(
                cx,
                cy+130,
                cx+55,
                cy+235
            )

        # =====================================
        # STATUS
        # =====================================

        p.setFont(
            QFont(
                "Orbitron",
                18,
                QFont.Bold
            )
        )

        p.drawText(
            60,
            70,
            "ASSEMBLING MARK XLII"
        )

        p.setFont(
            QFont(
                "Consolas",
                13
            )
        )

        p.drawText(
            60,
            105,
            f"Progress : {int(self.progress)}%"
        )

        # =====================================
        # PROGRESS BAR
        # =====================================

        p.drawRect(
            60,
            h-80,
            420,
            18
        )

        p.fillRect(
            62,
            h-78,
            int(self.progress*4.16),
            14,
            QColor(0,220,255)
        )

        # =====================================
        # MODULE STATUS
        # =====================================

        modules = [

            ("Helmet",5),

            ("Chest",20),

            ("Left Arm",40),

            ("Right Arm",55),

            ("Body",70),

            ("Left Leg",82),

            ("Right Leg",90)

        ]

        y = 150

        for name, need in modules:

            if self.progress >= need:

                txt = "[OK]"

                color = QColor(0,255,180)

            else:

                txt = "[--]"

                color = QColor(100,100,100)

            p.setPen(color)

            p.drawText(

                60,

                y,

                f"{txt}  {name}"

            )

            y += 28