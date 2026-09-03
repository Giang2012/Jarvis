import json
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QFrame


class ToolDetail(QWidget):
    """Functional Tool Center detail panel backed by the Brain."""

    def __init__(self, tool, brain=None, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.brain = brain
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(22, 18, 22, 20)
        self.root.setSpacing(12)
        self._build()
        self.setStyleSheet("""
            QFrame#DetailBody { background: rgba(2,14,23,225); border:1px solid rgba(43,196,220,90); border-radius:9px; }
            QLineEdit, QTextEdit, QComboBox { color:#D9FBFF; background:rgba(4,23,34,235); border:1px solid rgba(53,203,226,100); border-radius:6px; padding:9px; }
            QPushButton { color:#BDF8FF; background:rgba(0,180,220,34); border:1px solid rgba(60,220,240,115); border-radius:6px; padding:8px 13px; font-weight:700; }
            QPushButton:hover { background:rgba(0,200,240,70); border-color:#62F3FF; }
            QLabel { color:#75AAB4; }
        """)

    def _build(self):
        top = QHBoxLayout()
        glyph = QLabel(self.tool.glyph)
        glyph.setStyleSheet('color:#6FF5FF; font:24pt "Segoe UI Symbol";')
        title = QLabel(self.tool.title)
        title.setStyleSheet('color:#E4FDFF; font:700 17pt "Segoe UI";')
        top.addWidget(glyph); top.addWidget(title); top.addStretch(); self.root.addLayout(top)
        desc = QLabel(self.tool.description); desc.setWordWrap(True); self.root.addWidget(desc)
        frame = QFrame(); frame.setObjectName("DetailBody"); body = QVBoxLayout(frame); body.setContentsMargins(16,16,16,16); body.setSpacing(10); self.root.addWidget(frame, 1)
        self.output = QTextEdit(); self.output.setReadOnly(True)
        self._build_body(body)

    def _button(self, body, text, callback):
        b = QPushButton(text); b.clicked.connect(callback); body.addWidget(b); return b

    def _build_body(self, body):
        key = self.tool.key
        if key == "ai_chat":
            inp = QLineEdit(); inp.setPlaceholderText("Ask JARVIS…"); body.addWidget(inp)
            self._button(body, "SEND", lambda: self._show(self.brain.process(inp.text()) if self.brain else "Brain unavailable."))
        elif key == "search":
            inp = QLineEdit(); inp.setPlaceholderText("Search the web…"); body.addWidget(inp)
            self._button(body, "SEARCH", lambda: self._show(self.brain.process("tìm " + inp.text()) if self.brain else "Brain unavailable."))
        elif key == "weather":
            inp = QLineEdit(); inp.setPlaceholderText("Location / weather query…"); body.addWidget(inp)
            self._button(body, "CHECK", lambda: self._show(self.brain.process("thời tiết " + inp.text()) if self.brain else "Brain unavailable."))
        elif key == "calculator":
            inp = QLineEdit(); inp.setPlaceholderText("2 + 2 * 8"); body.addWidget(inp)
            self._button(body, "CALCULATE", lambda: self._show(self.brain.process("tính " + inp.text()) if self.brain else "Brain unavailable."))
        elif key == "open_app":
            inp = QLineEdit(); inp.setPlaceholderText("chrome / edge / notepad / …"); body.addWidget(inp)
            self._button(body, "OPEN", lambda: self._show(self.brain.process("mở " + inp.text()) if self.brain else "Brain unavailable."))
        elif key == "screenshot":
            self._button(body, "CAPTURE SCREEN", lambda: self._show(self.brain.process("chụp màn hình") if self.brain else "Brain unavailable."))
        elif key == "screen_vision":
            self._button(body, "INSPECT SCREEN", lambda: self._show_json(self.brain.inspect_screen(semantic=True) if self.brain else {"error":"Brain unavailable."}))
        elif key == "clipboard":
            self._button(body, "READ CLIPBOARD", lambda: self._show_json(self.brain.services.get("clipboard").get() if self.brain else {"error":"Brain unavailable."}))
            inp = QLineEdit(); inp.setPlaceholderText("Text to copy…"); body.addWidget(inp)
            self._button(body, "WRITE CLIPBOARD", lambda: self._show(self.brain.services.get("clipboard").set(inp.text()) if self.brain else "Brain unavailable."))
        elif key == "system":
            self._button(body, "REFRESH STATUS", lambda: self._show_json(self.brain.system_status() if self.brain else {"error":"Brain unavailable."}))
        elif key == "media":
            row = QHBoxLayout()
            for label, command in (("PLAY","play"),("PAUSE","pause"),("PREV","previous"),("NEXT","next"),("MUTE","mute")):
                b = QPushButton(label); b.clicked.connect(lambda checked=False, c=command: self._show(self.brain.process(c) if self.brain else "Brain unavailable.")); row.addWidget(b)
            body.addLayout(row)
        elif key == "files":
            inp = QLineEdit(); inp.setPlaceholderText("filename / folder keyword…"); body.addWidget(inp)
            self._button(body, "SEARCH FILES", lambda: self._show(self.brain.process("tìm file " + inp.text()) if self.brain else "Brain unavailable."))
        elif key == "screen_awareness":
            self._button(body, "ENABLE AWARENESS", lambda: self._show(self.brain.enable_screen_awareness(semantic=False, interval=5) if self.brain else "Brain unavailable."))
            self._button(body, "DISABLE AWARENESS", lambda: self._show(self.brain.disable_screen_awareness() if self.brain else "Brain unavailable."))
        else:
            body.addWidget(QLabel("No backend action registered."))
        body.addWidget(self.output, 1)

    def _show(self, value):
        self.output.setPlainText(str(value))

    def _show_json(self, value):
        try:
            self.output.setPlainText(json.dumps(value, ensure_ascii=False, indent=2, default=str))
        except Exception:
            self._show(value)
