from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QColor, QPainter, QPen, QFont


class ToolBar:
    """
    Floating JARVIS tool deck.

    The toolbar is painter-based so it fits the existing Dashboard renderer.
    It has:
      - compact dock
      - expanded tool grid
      - hover/active states
      - tool categories
      - clickable buttons
    """

    TOOLS = [
        ("AI", "AI CHAT", "AI"),
        ("SR", "SEARCH", "SEARCH"),
        ("WX", "WEATHER", "WEATHER"),
        ("Σ", "CALCULATOR", "CALCULATOR"),
        ("AP", "OPEN APP", "OPEN_APP"),
        ("SY", "SYSTEM", "SYSTEM"),
        ("MU", "MUSIC", "MUSIC"),
        ("NT", "NOTIFY", "NOTIFICATION"),
    ]

    def __init__(self):
        self.expanded = True
        self.hover = None
        self.active = None
        self.x = 32
        self.y = 710
        self.width = 880
        self.height = 92

    def setGeometry(self, width, height):
        self.x = 32
        self.y = max(120, height - 104)

    def toggle(self):
        self.expanded = not self.expanded

    def buttonRects(self):
        rects = {}
        start_x = self.x + 88
        for i, (_, _, key) in enumerate(self.TOOLS):
            col = i % 8
            rects[key] = QRect(start_x + col * 96, self.y + 29, 86, 46)
        return rects

    def toggleRect(self):
        return QRect(self.x + 8, self.y + 29, 68, 46)

    def hitTest(self, pos):
        if self.toggleRect().contains(pos):
            return "__TOGGLE__"
        if not self.expanded:
            return None
        for key, rect in self.buttonRects().items():
            if rect.contains(pos):
                return key
        return None

    def paint(self, painter, accent=None):
        accent = QColor(accent or "#00D8FF")
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)

        # Deck background.
        deck = QColor("#030B10")
        deck.setAlpha(232)
        painter.setBrush(deck)
        painter.setPen(QPen(accent, 1.2))
        painter.drawRoundedRect(QRect(self.x, self.y, self.width, self.height), 10, 10)

        # Header label.
        painter.setFont(QFont("Consolas", 8, QFont.Bold))
        painter.setPen(accent)
        painter.drawText(QRect(self.x + 16, self.y + 9, 220, 16),
                         Qt.AlignLeft | Qt.AlignVCenter, "J.A.R.V.I.S  //  TOOL DECK")

        painter.setFont(QFont("Consolas", 7))
        painter.setPen(QColor("#6DADB9"))
        painter.drawText(QRect(self.x + 600, self.y + 9, 250, 16),
                         Qt.AlignRight | Qt.AlignVCenter,
                         "CLICK TOOL  •  SUMMON  •  EXECUTE")

        # Toggle.
        tr = self.toggleRect()
        painter.setPen(QPen(accent, 1.4))
        painter.setBrush(QColor(accent) if not self.expanded else Qt.NoBrush)
        painter.drawRoundedRect(tr, 5, 5)
        painter.setPen(QColor("#061018") if not self.expanded else accent)
        painter.drawText(tr, Qt.AlignCenter, "TOOLS")

        if not self.expanded:
            painter.restore()
            return

        for code, label, key in self.TOOLS:
            r = self.buttonRects()[key]
            selected = key == self.active
            hovered = key == self.hover

            fill = QColor(accent)
            fill.setAlpha(48 if selected else 22 if hovered else 10)
            painter.setBrush(fill)

            pen = QPen(accent)
            pen.setWidthF(1.8 if selected else 1.0)
            painter.setPen(pen)
            painter.drawRoundedRect(r, 5, 5)

            painter.setFont(QFont("Consolas", 8, QFont.Bold))
            painter.setPen(accent)
            painter.drawText(QRect(r.x(), r.y() + 3, r.width(), 16),
                             Qt.AlignCenter, code)

            painter.setFont(QFont("Consolas", 6))
            painter.setPen(QColor("#B7EAF3"))
            painter.drawText(QRect(r.x(), r.y() + 21, r.width(), 17),
                             Qt.AlignCenter, label)

        painter.restore()
