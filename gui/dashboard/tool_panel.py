from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont


class ToolPanel:
    """Lightweight painter-based floating tool panel."""

    def __init__(self, title="TOOL", subtitle="READY"):
        self.title = title
        self.subtitle = subtitle
        self.x = 0
        self.y = 0
        self.width = 360
        self.height = 220
        self.visible = False
        self.userMoved = False
        self.lines = []
        self.progress = 0.0

    def setPosition(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def containsHeader(self, pos):
        return QRectF(self.x, self.y, self.width, 38).contains(pos)

    def contains(self, pos):
        return QRectF(self.x, self.y, self.width, self.height).contains(pos)

    def startDrag(self, pos):
        self._drag_offset = (pos.x() - self.x, pos.y() - self.y)
        self.userMoved = True

    def dragTo(self, pos):
        ox, oy = getattr(self, "_drag_offset", (0, 0))
        self.setPosition(pos.x() - ox, pos.y() - oy)

    def stopDrag(self):
        pass

    def setResult(self, result):
        text = str(result) if result is not None else "NO RESULT"
        self.lines = text.replace("\r", "").split("\n")[-8:]
        self.subtitle = "RESULT"

    def paint(self, painter, accent=None):
        accent = QColor(accent or "#00D8FF")
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        r = QRectF(self.x, self.y, self.width, self.height)

        bg = QColor("#061018")
        bg.setAlpha(238)
        painter.setBrush(QBrush(bg))

        pen = QPen(accent)
        pen.setWidthF(1.4)
        painter.setPen(pen)
        painter.drawRoundedRect(r, 9, 9)

        # Header.
        header = QColor(accent)
        header.setAlpha(35)
        painter.setBrush(QBrush(header))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(QRectF(self.x, self.y, self.width, 38), 9, 9)
        painter.drawRect(QRectF(self.x, self.y + 22, self.width, 16))

        painter.setPen(accent)
        painter.drawLine(self.x + 14, self.y + 10, self.x + 14, self.y + 28)

        painter.setFont(QFont("Consolas", 10, QFont.Bold))
        painter.drawText(QRectF(self.x + 26, self.y + 7, self.width - 100, 22),
                         Qt.AlignVCenter, self.title)

        painter.setFont(QFont("Consolas", 8))
        painter.drawText(QRectF(self.x + self.width - 75, self.y + 7, 58, 22),
                         Qt.AlignRight | Qt.AlignVCenter, self.subtitle)

        # Body.
        painter.setPen(QColor("#A8EFFF"))
        painter.setFont(QFont("Consolas", 8))

        if not self.lines:
            self.lines = ["SYSTEM READY", "AWAITING COMMAND"]

        y = self.y + 60
        for line in self.lines:
            painter.drawText(QRectF(self.x + 18, y, self.width - 36, 20),
                             Qt.AlignLeft | Qt.AlignVCenter, line[:64])
            y += 21

        # Resize marker.
        painter.setPen(accent)
        for i in range(3):
            painter.drawLine(
                self.x + self.width - 17 + i * 4,
                self.y + self.height - 9,
                self.x + self.width - 9,
                self.y + self.height - 17 + i * 4,
            )

        painter.restore()
