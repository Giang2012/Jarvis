from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QFrame, QStackedWidget
)
from .tool_registry import ToolRegistry
from .tool_card import ToolCard
from .tool_detail import ToolDetail

class ToolCenter(QWidget):
    backRequested = Signal()
    toolSelected = Signal(str)

    def __init__(self, brain=None, parent=None):
        super().__init__(parent)
        self.brain = brain
        self.registry = ToolRegistry()
        self.active_category = "AI"
        self.active_tool = None
        self.phase = 0.0
        self._build()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(33)

    def _build(self):
        root = QVBoxLayout(self); root.setContentsMargins(20,16,20,16); root.setSpacing(9)
        top = QHBoxLayout()
        b = QLabel("J.A.R.V.I.S"); b.setStyleSheet('color:#70F4FF;font:700 16pt "Segoe UI";')
        t = QLabel("TOOL CENTER"); t.setStyleSheet('color:#D9FCFF;font:700 11pt "Segoe UI";')
        self.clock = QLabel()
        self.clock.setStyleSheet('color:#71F3FF;font:700 13pt Consolas;')
        back = QPushButton("‹ AI"); back.clicked.connect(self.backRequested.emit)
        top.addWidget(b); top.addSpacing(18); top.addWidget(t); top.addStretch(); top.addWidget(self.clock); top.addWidget(back)
        root.addLayout(top)

        work = QHBoxLayout(); work.setSpacing(10)
        side = QFrame(); side.setFixedWidth(170)
        sl = QVBoxLayout(side); sl.setContentsMargins(10,10,10,10)
        lab = QLabel("TOOLS"); lab.setStyleSheet("color:#71F4FF;font-weight:700;")
        sl.addWidget(lab)
        for cat in self.registry.categories:
            x = QPushButton(cat); x.clicked.connect(lambda _, c=cat: self.select_category(c)); sl.addWidget(x)
        sl.addStretch()
        work.addWidget(side)

        mid = QVBoxLayout()
        bar = QHBoxLayout()
        self.search = QLineEdit(); self.search.setPlaceholderText("Search tools…")
        self.search.textChanged.connect(self._filter)
        bar.addWidget(self.search); mid.addLayout(bar)
        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.NoFrame)
        self.host = QWidget(); self.grid = QGridLayout(self.host); self.grid.setSpacing(9)
        self.scroll.setWidget(self.host); mid.addWidget(self.scroll,1)
        work.addLayout(mid,1)

        self.detail_frame = QFrame(); self.detail_frame.setFixedWidth(350)
        dl = QVBoxLayout(self.detail_frame); dl.setContentsMargins(0,0,0,0)
        self.details = QStackedWidget(); dl.addWidget(self.details)
        work.addWidget(self.detail_frame)
        root.addLayout(work,1)

        self.setStyleSheet("""
            QWidget { color:#C9F7FB; }
            QFrame { background:rgba(3,14,23,220); border:1px solid rgba(32,180,208,90); border-radius:8px; }
            QPushButton { color:#9FD8E0; background:rgba(0,150,190,25); border:1px solid rgba(30,160,190,55); border-radius:5px; padding:7px 9px; }
            QPushButton:hover { color:#E1FEFF; border-color:#54EFFF; }
            QLineEdit { color:#D9FCFF; background:rgba(3,18,28,230); border:1px solid rgba(43,187,214,100); border-radius:6px; padding:8px; }
        """)
        self._refresh()
        self._empty()

    def _empty(self):
        w = QWidget(); l = QVBoxLayout(w)
        x = QLabel("SELECT A TOOL"); x.setStyleSheet("color:#70F4FF;font:700 16pt Segoe UI;")
        l.addWidget(x); l.addWidget(QLabel("Choose a module to run it.")); l.addStretch()
        self.details.addWidget(w); self.details.setCurrentWidget(w)

    def select_category(self, cat):
        self.active_category = cat; self.search.clear(); self._refresh()

    def _filter(self, text):
        self._refresh(text)

    def _refresh(self, query=""):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        tools = self.registry.search(query) if query.strip() else self.registry.category(self.active_category)
        for i, tool in enumerate(tools):
            c = ToolCard(tool); c.clicked.connect(self.select_tool)
            self.grid.addWidget(c, i//3, i%3)

    def select_tool(self, key):
        tool = self.registry.get(key)
        if not tool: return
        detail = ToolDetail(tool, brain=self.brain)
        self.details.addWidget(detail); self.details.setCurrentWidget(detail)
        self.active_tool = key; self.toolSelected.emit(key)

    def _animate(self):
        import datetime
        self.phase += 0.04
        self.clock.setText(datetime.datetime.now().strftime("%H:%M:%S"))
        self.update()

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        r = self.rect()
        p.setPen(QPen(QColor(0,125,155,18),1))
        for x in range(0,r.width(),32): p.drawLine(x,0,x,r.height())
        for y in range(0,r.height(),32): p.drawLine(0,y,r.width(),y)
        p.end()
