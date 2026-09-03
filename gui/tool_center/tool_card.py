from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont
from PySide6.QtWidgets import QWidget


class ToolCard(QWidget):
    clicked = Signal(str)

    def __init__(self, tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.hovered = False
        self.selected = False
        self.setMinimumSize(178, 132)
        self.setMaximumHeight(145)
        self.setCursor(Qt.PointingHandCursor)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.hovered = True
        self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.tool.key)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.rect().adjusted(1, 1, -1, -1)

        border = QColor("#5EF2FF" if self.hovered or self.selected else "#145C6B")
        fill = QColor(5, 20, 30, 245 if self.hovered else 220)

        p.setPen(QPen(border, 1.4 if self.hovered else 1))
        p.setBrush(QBrush(fill))
        p.drawRoundedRect(r, 9, 9)

        # Sci-fi corner cuts
        p.setPen(QPen(QColor("#50EFFF"), 2))
        p.drawLine(r.left()+2, r.top()+15, r.left()+2, r.top()+3)
        p.drawLine(r.left()+2, r.top()+3, r.left()+15, r.top()+3)
        p.drawLine(r.right()-15, r.bottom()-3, r.right()-2, r.bottom()-3)
        p.drawLine(r.right()-2, r.bottom()-15, r.right()-2, r.bottom()-3)

        # Icon well
        cx, cy = r.left()+42, r.top()+45
        p.setPen(QPen(QColor(55, 210, 235, 85), 1))
        p.setBrush(QBrush(QColor(0, 130, 170, 25)))
        p.drawEllipse(cx-27, cy-27, 54, 54)
        p.setPen(QPen(QColor("#67F4FF"), 1.5))
        p.drawEllipse(cx-21, cy-21, 42, 42)

        p.setPen(QColor("#75F5FF"))
        p.setFont(QFont("Segoe UI Symbol", 18))
        p.drawText(cx-18, cy-17, 36, 34, Qt.AlignCenter, self.tool.glyph)

        p.setPen(QColor("#D8FBFF"))
        p.setFont(QFont("Segoe UI", 9, QFont.Bold))
        p.drawText(r.adjusted(14, 84, -14, -30), Qt.AlignLeft | Qt.AlignVCenter, self.tool.title)

        p.setPen(QColor("#6D9FAA"))
        p.setFont(QFont("Segoe UI", 8))
        p.drawText(r.adjusted(14, 104, -14, -5), Qt.AlignLeft | Qt.AlignVCenter, self.tool.subtitle)

        # Tiny status mark
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(QColor("#55EEFF")))
        p.drawEllipse(r.right()-16, r.top()+12, 4, 4)
        p.end()
