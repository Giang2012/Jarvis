from PySide6.QtGui import *
from PySide6.QtCore import *


class ProgressBar:

    def draw(self,painter,x,y,w,h,value):

        painter.save()

        # Background

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(0,255,255,18)
        )

        painter.drawRoundedRect(
            QRectF(x,y,w,h),
            4,
            4
        )

        # Fill

        fill = w * value

        grad = QLinearGradient(
            x,
            y,
            x+w,
            y
        )

        grad.setColorAt(
            0,
            QColor(0,255,255)
        )

        grad.setColorAt(
            1,
            QColor(120,255,255)
        )

        painter.setBrush(grad)

        painter.drawRoundedRect(
            QRectF(
                x,
                y,
                fill,
                h
            ),
            4,
            4
        )

        # Glow

        painter.setBrush(
            QColor(
                180,
                255,
                255,
                180
            )
        )

        painter.drawEllipse(
            QPointF(
                x+fill,
                y+h/2
            ),
            3,
            3
        )

        painter.restore()