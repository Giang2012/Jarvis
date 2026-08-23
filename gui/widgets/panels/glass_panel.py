from PySide6.QtGui import *
from PySide6.QtCore import *
from gui.common.panels.glow_border import GlowBorder

class GlassPanel:

    def __init__(self):

        self.glow = GlowBorder()

        self.radius = 20

        self.borderColor = QColor(0,255,255,90)

        self.background = QColor(15,25,40,85)

    # ----------------------------------

    def draw(self,painter,rect):

        painter.save()

        path = QPainterPath()

        path.addRoundedRect(
            rect,
            self.radius,
            self.radius
        )

        painter.fillPath(
            path,
            self.background
        )

        pen = QPen(
            self.borderColor,
            1.5
        )

        painter.setPen(pen)

        painter.drawPath(path)

        # Highlight

        grad = QLinearGradient(
            rect.topLeft(),
            rect.bottomLeft()
        )

        grad.setColorAt(
            0,
            QColor(255,255,255,40)
        )

        grad.setColorAt(
            0.2,
            QColor(255,255,255,10)
        )

        grad.setColorAt(
            1,
            QColor(255,255,255,0)
        )

        painter.fillPath(
            path,
            grad
        )

        self.glow.draw(
            painter,
            rect
        )

        painter.restore()