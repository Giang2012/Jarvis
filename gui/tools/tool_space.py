from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QLinearGradient, QFont
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QStackedWidget, QScrollArea, QGridLayout
)

from .tool_registry import ToolRegistry
from .tool_card import ToolCard
from .tool_panels import build_tool_detail


class ToolSpace(QWidget):
    """
    Full-screen Tool Space.

    This is intentionally a separate workspace from the minimal AI Dashboard.
    It owns the dense/advanced UI; the AI Dashboard does not.
    """

    backRequested = Signal()
    toolExecuted = Signal(str, object)

    def __init__(self, brain=None, parent=None):
        super().__init__(parent)
        self.brain = brain
        self.registry = ToolRegistry()
        self.current_category = "PRODUCTIVITY"
        self.current_key = None

        self.setObjectName("ToolSpace")
        self.setMouseTracking(True)

        self._build_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(33)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 18)
        root.setSpacing(12)

        # Header
        header = QHBoxLayout()
        brand = QLabel("J.A.R.V.I.S")
        brand.setObjectName("Brand")
        title = QLabel("  /  TOOL COMMAND CENTER")
        title.setObjectName("PageTitle")

        back = QPushButton("‹  AI")
        back.setObjectName("BackButton")
        back.clicked.connect(self.backRequested.emit)

        header.addWidget(brand)
        header.addWidget(title)
        header.addStretch()
        header.addWidget(QLabel("SYSTEM ONLINE"))
        header.addWidget(back)
        root.addLayout(header)

        # Main split
        split = QHBoxLayout()
        split.setSpacing(14)

        self.sidebar = self._build_sidebar()
        split.addWidget(self.sidebar, 0)

        center = QVBoxLayout()
        self.category_bar = self._build_categories()
        center.addWidget(self.category_bar)

        self.cards_scroll = QScrollArea()
        self.cards_scroll.setWidgetResizable(True)
        self.cards_scroll.setFrameShape(QFrame.NoFrame)

        self.cards_host = QWidget()
        self.cards_grid = QGridLayout(self.cards_host)
        self.cards_grid.setContentsMargins(4, 4, 4, 4)
        self.cards_grid.setSpacing(12)

        self.cards_scroll.setWidget(self.cards_host)
        center.addWidget(self.cards_scroll, 1)
        split.addLayout(center, 1)

        self.detail = QFrame()
        self.detail.setObjectName("DetailPanel")
        detail_layout = QVBoxLayout(self.detail)
        detail_layout.setContentsMargins(0, 0, 0, 0)

        self.detail_stack = QStackedWidget()
        detail_layout.addWidget(self.detail_stack)
        split.addWidget(self.detail, 0)

        self.detail.setFixedWidth(330)
        root.addLayout(split, 1)

        self._refresh_cards()
        self._show_overview()

        self.setStyleSheet("""
            QWidget#ToolSpace {
                background: #02070b;
                color: #cceff3;
            }
            QLabel#Brand {
                color: #79f5ff;
                font: 700 17pt "Segoe UI";
                letter-spacing: 3px;
            }
            QLabel#PageTitle {
                color: #9acbd2;
                font: 10pt "Segoe UI";
            }
            QHBoxLayout QLabel {
                color: #5e9da8;
            }
            QPushButton#BackButton {
                color: #8debf4;
                background: rgba(0, 170, 210, 25);
                border: 1px solid rgba(0, 220, 240, 100);
                border-radius: 7px;
                padding: 7px 14px;
                font: 700 9pt "Segoe UI";
            }
            QScrollArea {
                background: transparent;
            }
            QFrame#DetailPanel {
                background: rgba(3, 16, 26, 220);
                border: 1px solid rgba(0, 210, 240, 95);
                border-radius: 11px;
            }
        """)

    def _build_sidebar(self):
        frame = QFrame()
        frame.setFixedWidth(190)
        frame.setStyleSheet("""
            QFrame {
                background: rgba(3, 14, 23, 220);
                border: 1px solid rgba(0, 205, 235, 85);
                border-radius: 11px;
            }
            QPushButton {
                text-align: left;
                color: #79aeb8;
                background: transparent;
                border: 0;
                padding: 11px 14px;
                font: 9pt "Segoe UI";
            }
            QPushButton:hover {
                color: #bffcff;
                background: rgba(0, 200, 235, 28);
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(3)

        label = QLabel("TOOLS")
        label.setStyleSheet(
            'color:#71f4ff; font:700 10pt "Segoe UI"; padding:4px 8px;'
        )
        layout.addWidget(label)

        for category in self.registry.CATEGORIES:
            button = QPushButton(category)
            button.clicked.connect(
                lambda checked=False, c=category: self.select_category(c)
            )
            layout.addWidget(button)

        layout.addStretch()

        info = QLabel(
            "ADVANCED WORKSPACE\n\n"
            "Tools live here.\n"
            "The AI dashboard stays clean."
        )
        info.setStyleSheet(
            'color:#4d7f89; font:8pt "Segoe UI"; padding:8px;'
        )
        info.setWordWrap(True)
        layout.addWidget(info)
        return frame

    def _build_categories(self):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: rgba(3, 13, 21, 175);
                border: 1px solid rgba(0, 190, 220, 70);
                border-radius: 9px;
            }
            QPushButton {
                color: #6faab4;
                background: transparent;
                border: 0;
                padding: 8px 12px;
                font: 700 8pt "Segoe UI";
            }
            QPushButton:hover {
                color: #d4fdff;
            }
        """)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 4, 10, 4)

        for category in self.registry.CATEGORIES:
            button = QPushButton(category)
            button.clicked.connect(
                lambda checked=False, c=category: self.select_category(c)
            )
            layout.addWidget(button)

        layout.addStretch()
        return frame

    def select_category(self, category):
        self.current_category = category
        self._refresh_cards()

    def _refresh_cards(self):
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        tools = self.registry.by_category(self.current_category)

        columns = 3
        for index, tool in enumerate(tools):
            card = ToolCard(tool)
            card.clicked.connect(self.select_tool)
            self.cards_grid.addWidget(card, index // columns, index % columns)

        self.cards_grid.setRowStretch((len(tools) + columns - 1) // columns, 1)

    def select_tool(self, key):
        tool = self.registry.get(key)
        if tool is None:
            return

        self.current_key = key
        detail = build_tool_detail(key, tool)
        self.detail_stack.addWidget(detail)
        self.detail_stack.setCurrentWidget(detail)

    def _show_overview(self):
        overview = QWidget()
        layout = QVBoxLayout(overview)
        layout.setContentsMargins(22, 20, 22, 20)

        title = QLabel("TOOL SPACE")
        title.setStyleSheet(
            'color:#dffcff; font:700 18pt "Segoe UI";'
        )
        layout.addWidget(title)

        text = QLabel(
            "Select a module to open its dedicated workspace.\n\n"
            "No command dialogs. No crowded dashboard.\n"
            "Advanced controls belong here."
        )
        text.setWordWrap(True)
        text.setStyleSheet(
            'color:#76aeb8; font:10pt "Segoe UI"; line-height:140%;'
        )
        layout.addWidget(text)
        layout.addStretch()

        self.detail_stack.addWidget(overview)
        self.detail_stack.setCurrentWidget(overview)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.rect()

        # Fine technical grid
        painter.setPen(QPen(QColor(0, 135, 165, 22), 1))
        step = 32
        for x in range(0, rect.width(), step):
            painter.drawLine(x, 0, x, rect.height())
        for y in range(0, rect.height(), step):
            painter.drawLine(0, y, rect.width(), y)

        # Header energy line
        gradient = QLinearGradient(0, 0, rect.width(), 0)
        gradient.setColorAt(0.0, QColor(0, 225, 255, 0))
        gradient.setColorAt(0.5, QColor(0, 225, 255, 150))
        gradient.setColorAt(1.0, QColor(0, 225, 255, 0))
        painter.setPen(QPen(gradient, 1))
        painter.drawLine(30, 70, rect.width() - 30, 70)

        # Center-right reactor-like background element
        cx = int(rect.width() * 0.69)
        cy = int(rect.height() * 0.58)
        for radius, alpha in ((230, 12), (190, 16), (150, 22), (110, 28)):
            painter.setPen(QPen(QColor(0, 215, 245, alpha), 1))
            painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)

        painter.end()
