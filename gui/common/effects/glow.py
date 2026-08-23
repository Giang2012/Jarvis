"""
JARVIS Glow Effect System
Creates hologram energy glow layers
"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import (
    QPainter,
    QColor,
    QRadialGradient,
)



class Glow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.opacity = 120

        self.setAttribute(
            Qt.WA_TransparentForMouseEvents
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )


    def set_opacity(self, value):

        self.opacity = value
        self.update()



    def paintEvent(self,event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )


        center = self.rect().center()


        radius = min(
            self.width(),
            self.height()
        ) / 2



        # ======================
        # Outer Energy Bloom
        # ======================

        gradient = QRadialGradient(
            center,
            radius
        )


        gradient.setColorAt(
            0,
            QColor(
                0,
                220,
                255,
                self.opacity
            )
        )


        gradient.setColorAt(
            0.35,
            QColor(
                0,
                180,
                255,
                70
            )
        )


        gradient.setColorAt(
            1,
            QColor(
                0,
                100,
                255,
                0
            )
        )


        painter.setBrush(
            gradient
        )


        painter.setPen(
            Qt.NoPen
        )


        painter.drawEllipse(
            QRectF(
                center.x()-radius,
                center.y()-radius,
                radius*2,
                radius*2
            )
        )



        # ======================
        # Inner Core Glow
        # ======================

        core_gradient = QRadialGradient(
            center,
            radius*0.35
        )


        core_gradient.setColorAt(
            0,
            QColor(
                240,
                255,
                255,
                220
            )
        )


        core_gradient.setColorAt(
            0.3,
            QColor(
                0,
                230,
                255,
                120
            )
        )


        core_gradient.setColorAt(
            1,
            QColor(
                0,
                150,
                255,
                0
            )
        )


        painter.setBrush(
            core_gradient
        )


        painter.drawEllipse(
            QRectF(
                center.x()-radius*0.35,
                center.y()-radius*0.35,
                radius*0.7,
                radius*0.7
            )
        )