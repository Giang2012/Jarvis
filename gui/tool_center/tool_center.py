from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, QFont, QLinearGradient
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QLineEdit, QScrollArea, QFrame, QStackedWidget, QSizePolicy
)

from .tool_registry import ToolRegistry
from .tool_card import ToolCard
from .tool_detail import ToolDetail


class ToolCenter(QWidget):
    """Full Tool Space. Separate from the minimal AI Dashboard."""

    backRequested = Signal()
    toolSelected = Signal(str)

    def __init__(self, brain=None, parent=None):
        super().__init__(parent)
        self.brain = brain
        self.registry = ToolRegistry()
        self.active_category = "PRODUCTIVITY"
        self.active_tool = None
        self._phase = 0.0

        self.setObjectName("ToolCenter")
        self.setMouseTracking(True)
        self._build()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(33)

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 18, 24, 18)
        root.setSpacing(10)

        # ---------- TOP BAR ----------
        top = QHBoxLayout()
        brand = QLabel("J.A.R.V.I.S")
        brand.setObjectName("Brand")
        title = QLabel("TOOL CENTER")
        title.setObjectName("Title")
        mode = QLabel("[ AI SPACE SEPARATED ]")
        mode.setObjectName("Mode")

        self.clock = QLabel("09:45:22")
        self.clock.setObjectName("Clock")

        back = QPushButton("‹  AI")
        back.setObjectName("Back")
        back.clicked.connect(self.backRequested.emit)

        top.addWidget(brand)
        top.addSpacing(20)
        top.addWidget(title)
        top.addWidget(mode)
        top.addStretch()
        top.addWidget(self.clock)
        top.addSpacing(16)
        top.addWidget(QLabel("● ONLINE"))
        top.addWidget(back)
        root.addLayout(top)

        # ---------- WORKSPACE ----------
        workspace = QHBoxLayout()
        workspace.setSpacing(12)

        workspace.addWidget(self._sidebar(), 0)

        middle = QVBoxLayout()
        middle.setSpacing(10)
        middle.addWidget(self._category_bar())

        search_row = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search tools…")
        self.search.textChanged.connect(self._filter_tools)
        search_row.addWidget(self.search, 1)
        middle.addLayout(search_row)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.cards_host = QWidget()
        self.cards_grid = QGridLayout(self.cards_host)
        self.cards_grid.setContentsMargins(2, 2, 8, 8)
        self.cards_grid.setHorizontalSpacing(10)
        self.cards_grid.setVerticalSpacing(10)
        self.scroll.setWidget(self.cards_host)

        middle.addWidget(self.scroll, 1)
        workspace.addLayout(middle, 1)

        # ---------- DETAIL ----------
        self.detail_frame = QFrame()
        self.detail_frame.setObjectName("DetailFrame")
        self.detail_frame.setFixedWidth(360)

        detail_layout = QVBoxLayout(self.detail_frame)
        detail_layout.setContentsMargins(0, 0, 0, 0)
        self.details = QStackedWidget()
        detail_layout.addWidget(self.details)

        workspace.addWidget(self.detail_frame)
        root.addLayout(workspace, 1)

        # ---------- QUICK ACCESS ----------
        root.addWidget(self._quick_access())

        self.setStyleSheet("""
            QWidget#ToolCenter {
                background: #02070B;
                color: #C9F7FB;
            }
            QLabel#Brand {
                color: #70F4FF;
                font: 700 16pt "Segoe UI";
                letter-spacing: 3px;
            }
            QLabel#Title {
                color: #C5F9FF;
                font: 700 11pt "Segoe UI";
                letter-spacing: 2px;
            }
            QLabel#Mode {
                color: #4D9AA7;
                font: 8pt "Segoe UI";
                margin-left: 12px;
            }
            QLabel#Clock {
                color: #71F3FF;
                font: 700 15pt "Consolas";
            }
            QPushButton#Back {
                color: #A9F5FB;
                background: rgba(0, 180, 220, 28);
                border: 1px solid rgba(60, 220, 240, 100);
                border-radius: 6px;
                padding: 7px 12px;
            }
            QLineEdit {
                color: #D9FCFF;
                background: rgba(3, 18, 28, 230);
                border: 1px solid rgba(43, 187, 214, 100);
                border-radius: 7px;
                padding: 9px 12px;
                font: 9pt "Segoe UI";
            }
            QLineEdit:focus {
                border-color: #55EFFF;
            }
            QFrame#DetailFrame {
                background: rgba(3, 14, 23, 235);
                border: 1px solid rgba(34, 182, 210, 100);
                border-radius: 10px;
            }
        """)

        self._refresh_cards()
        self._show_empty_detail()

    def _sidebar(self):
        frame = QFrame()
        frame.setObjectName("Sidebar")
        frame.setFixedWidth(205)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 14, 12, 14)
        layout.setSpacing(4)

        label = QLabel("TOOLS SUITE")
        label.setStyleSheet('color:#71F4FF; font:700 9pt "Segoe UI";')
        layout.addWidget(label)
        layout.addSpacing(5)

        for cat in self.registry.categories:
            b = QPushButton(cat)
            b.setObjectName("CategoryButton")
            b.clicked.connect(lambda checked=False, c=cat: self.select_category(c))
            layout.addWidget(b)

        layout.addStretch()

        stat = QLabel("TOOL ENGINE\n\n"
                      "CATALOG     22\n"
                      "ONLINE      YES\n"
                      "BACKEND     STAGED")
        stat.setStyleSheet(
            'color:#4D8792; font:8pt "Consolas"; padding:8px;'
        )
        layout.addWidget(stat)

        frame.setStyleSheet("""
            QFrame#Sidebar {
                background: rgba(3, 14, 23, 230);
                border: 1px solid rgba(32, 180, 208, 95);
                border-radius: 10px;
            }
            QPushButton#CategoryButton {
                text-align:left;
                color:#71A8B2;
                background:transparent;
                border:0;
                border-radius:5px;
                padding:11px 10px;
                font:700 8pt "Segoe UI";
            }
            QPushButton#CategoryButton:hover {
                color:#D6FDFF;
                background:rgba(0,190,225,35);
            }
        """)
        return frame

    def _category_bar(self):
        frame = QFrame()
        frame.setObjectName("CategoryBar")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(8, 3, 8, 3)
        layout.setSpacing(1)

        for cat in self.registry.categories:
            b = QPushButton(cat)
            b.clicked.connect(lambda checked=False, c=cat: self.select_category(c))
            layout.addWidget(b)

        frame.setStyleSheet("""
            QFrame#CategoryBar {
                background:rgba(3,14,23,190);
                border:1px solid rgba(30,170,200,75);
                border-radius:8px;
            }
            QPushButton {
                color:#639AA5;
                background:transparent;
                border:0;
                padding:8px 9px;
                font:700 7pt "Segoe UI";
            }
            QPushButton:hover {
                color:#D9FDFF;
            }
        """)
        return frame

    def _quick_access(self):
        frame = QFrame()
        frame.setObjectName("Quick")
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(10, 7, 10, 7)
        layout.setSpacing(7)

        label = QLabel("QUICK ACCESS")
        label.setStyleSheet('color:#71F4FF; font:700 8pt "Segoe UI";')
        layout.addWidget(label)
        layout.addStretch()

        for key in ("ai_chat", "search", "screen_vision", "screenshot",
                    "open_app", "system", "media", "files"):
            tool = self.registry.get(key)
            b = QPushButton(f"{tool.glyph}  {tool.title}")
            b.clicked.connect(lambda checked=False, k=key: self.select_tool(k))
            layout.addWidget(b)

        frame.setStyleSheet("""
            QFrame#Quick {
                background:rgba(3,14,23,220);
                border:1px solid rgba(30,180,208,80);
                border-radius:9px;
            }
            QPushButton {
                color:#78B5BF;
                background:rgba(0,150,190,25);
                border:1px solid rgba(30,160,190,55);
                border-radius:5px;
                padding:7px 9px;
                font:700 7pt "Segoe UI";
            }
            QPushButton:hover {
                color:#E1FEFF;
                border-color:#54EFFF;
            }
        """)
        return frame

    def select_category(self, category):
        self.active_category = category
        self.search.blockSignals(True)
        self.search.clear()
        self.search.blockSignals(False)
        self._refresh_cards()

    def _filter_tools(self, text):
        self._refresh_cards(text)

    def _refresh_cards(self, query=""):
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        if query.strip():
            tools = self.registry.search(query)
        else:
            tools = self.registry.category(self.active_category)

        columns = 4
        for i, tool in enumerate(tools):
            card = ToolCard(tool)
            card.clicked.connect(self.select_tool)
            self.cards_grid.addWidget(card, i // columns, i % columns)

        rows = (len(tools) + columns - 1) // columns
        if rows:
            self.cards_grid.setRowStretch(rows, 1)

    def select_tool(self, key):
        tool = self.registry.get(key)
        if tool is None:
            return

        self.active_tool = key
        detail = ToolDetail(tool, brain=self.brain)
        self.details.addWidget(detail)
        self.details.setCurrentWidget(detail)
        self.toolSelected.emit(key)

    def _show_empty_detail(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.addWidget(QLabel("TOOL CENTER", objectName="EmptyTitle"))
        label = QLabel(
            "Select a module.\n\n"
            "The AI Dashboard stays minimal.\n"
            "This workspace contains the advanced controls."
        )
        label.setWordWrap(True)
        label.setStyleSheet('color:#6B9CA5; font:9pt "Segoe UI";')
        layout.addWidget(label)
        layout.addStretch()
        self.details.addWidget(page)
        self.details.setCurrentWidget(page)

    def _animate(self):
        self._phase += 0.035
        self.clock.setText(__import__("datetime").datetime.now().strftime("%H:%M:%S"))
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        r = self.rect()

        # Technical background grid
        p.setPen(QPen(QColor(0, 125, 155, 18), 1))
        step = 32
        for x in range(0, r.width(), step):
            p.drawLine(x, 0, x, r.height())
        for y in range(0, r.height(), step):
            p.drawLine(0, y, r.width(), y)

        # Subtle reactor rings behind the tool catalog.
        cx = int(r.width() * 0.62)
        cy = int(r.height() * 0.51)
        pulse = int(8 * (1 + __import__("math").sin(self._phase)))
        for radius, alpha in ((235, 10), (195, 14), (155, 18), (115, 23)):
            p.setPen(QPen(QColor(0, 205, 240, alpha), 1))
            p.drawEllipse(cx-radius, cy-radius, radius*2, radius*2)

        # Moving scan line.
        y = int(95 + ((self._phase * 40) % max(1, r.height()-100)))
        p.setPen(QPen(QColor(40, 220, 245, 12 + pulse), 1))
        p.drawLine(0, y, r.width(), y)

        p.end()
