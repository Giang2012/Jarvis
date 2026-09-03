from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QFont
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel


class ToolCard(QFrame):
    clicked = Signal(str)

    def __init__(self, tool, parent=None):
        super().__init__(parent)
        self.tool = tool
        self._hovered = False

        self.setObjectName("ToolCard")
        self.setFixedHeight(126)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(4)

        self.glyph = QLabel(tool.glyph)
        self.glyph.setObjectName("ToolGlyph")
        self.glyph.setAlignment(Qt.AlignCenter)
        self.glyph.setFixedSize(48, 42)

        self.title = QLabel(tool.title)
        self.title.setObjectName("ToolTitle")

        self.subtitle = QLabel(tool.subtitle)
        self.subtitle.setObjectName("ToolSubtitle")

        layout.addWidget(self.glyph, 0, Qt.AlignLeft)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

        self.setStyleSheet("""
            QFrame#ToolCard {
                background: rgba(4, 17, 27, 225);
                border: 1px solid rgba(0, 210, 240, 90);
                border-radius: 10px;
            }
            QFrame#ToolCard:hover {
                background: rgba(5, 29, 43, 245);
                border: 1px solid rgba(70, 235, 255, 210);
            }
            QLabel#ToolGlyph {
                color: #71f5ff;
                background: rgba(0, 180, 220, 28);
                border: 1px solid rgba(0, 225, 255, 110);
                border-radius: 8px;
                font: 18pt "Segoe UI";
            }
            QLabel#ToolTitle {
                color: #d9fbff;
                font: 700 10pt "Segoe UI";
            }
            QLabel#ToolSubtitle {
                color: #6daab7;
                font: 9pt "Segoe UI";
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.tool.key)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)
