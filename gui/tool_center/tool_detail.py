import json
import ast
import operator as op
import platform
import subprocess
import urllib.parse
import urllib.request

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QFrame
)

class OllamaWorker(QThread):
    finished = Signal(str)
    failed = Signal(str)

    def __init__(self, prompt, model, host="http://127.0.0.1:11434", parent=None):
        super().__init__(parent)
        self.prompt, self.model, self.host = prompt, model, host.rstrip("/")

    def run(self):
        try:
            payload = (
                '{"model":' + json.dumps(self.model, ensure_ascii=False) +
                ',"prompt":' + json.dumps(self.prompt, ensure_ascii=False) +
                ',"stream":false}'
            ).encode("utf-8")
            req = urllib.request.Request(
                self.host + "/api/generate",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.loads(r.read().decode("utf-8"))
            self.finished.emit(data.get("response", "").strip() or "(Ollama returned no text.)")
        except Exception as e:
            self.failed.emit(f"Ollama error: {e}")

class ToolDetail(QWidget):
    def __init__(self, tool, brain=None, parent=None):
        super().__init__(parent)
        self.tool = tool
        self.brain = brain
        self.worker = None
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(18, 16, 18, 18)
        self.root.setSpacing(10)
        self._build()
        self.setStyleSheet("""
            QFrame#DetailBody { background: rgba(2,14,23,225); border:1px solid rgba(43,196,220,90); border-radius:9px; }
            QLineEdit, QTextEdit, QComboBox { color:#D9FBFF; background:rgba(4,23,34,235); border:1px solid rgba(53,203,226,100); border-radius:6px; padding:8px; }
            QPushButton { color:#BDF8FF; background:rgba(0,180,220,34); border:1px solid rgba(60,220,240,115); border-radius:6px; padding:8px 12px; font-weight:700; }
            QPushButton:hover { background:rgba(0,200,240,70); }
            QLabel { color:#75AAB4; }
        """)

    def _button(self, body, text, callback):
        b = QPushButton(text)
        b.clicked.connect(callback)
        body.addWidget(b)
        return b

    def _build(self):
        top = QHBoxLayout()
        glyph = QLabel(self.tool.glyph)
        glyph.setStyleSheet('color:#6FF5FF; font:22pt "Segoe UI Symbol";')
        title = QLabel(self.tool.title)
        title.setStyleSheet('color:#E4FDFF; font:700 16pt "Segoe UI";')
        top.addWidget(glyph); top.addWidget(title); top.addStretch()
        self.root.addLayout(top)
        d = QLabel(self.tool.description); d.setWordWrap(True); self.root.addWidget(d)

        frame = QFrame(); frame.setObjectName("DetailBody")
        body = QVBoxLayout(frame); body.setContentsMargins(14,14,14,14); body.setSpacing(9)
        self.root.addWidget(frame, 1)

        self.output = QTextEdit(); self.output.setReadOnly(True)

        if self.tool.key == "ai_chat":
            self.prompt = QLineEdit()
            self.prompt.setPlaceholderText("Ask JARVIS anything…")
            self.model = QComboBox()
            self._load_models()
            body.addWidget(QLabel("OLLAMA MODEL"))
            body.addWidget(self.model)
            body.addWidget(self.prompt)
            self._button(body, "SEND TO OLLAMA", self._chat)

        elif self.tool.key == "calculator":
            self.prompt = QLineEdit()
            self.prompt.setPlaceholderText("2 + 2 * 8")
            body.addWidget(self.prompt)
            self._button(body, "CALCULATE", self._calculate)

        elif self.tool.key == "system":
            self._button(body, "REFRESH", self._system)

        elif self.tool.key == "screenshot":
            self._button(body, "CAPTURE SCREEN", self._screenshot)

        elif self.tool.key == "open_app":
            self.prompt = QLineEdit()
            self.prompt.setPlaceholderText("notepad / calc / mspaint")
            body.addWidget(self.prompt)
            self._button(body, "OPEN", self._open_app)

        elif self.tool.key == "search":
            self.prompt = QLineEdit()
            self.prompt.setPlaceholderText("Search query…")
            body.addWidget(self.prompt)
            self._button(body, "SEARCH", self._search)

        body.addWidget(self.output, 1)

    def _load_models(self):
        try:
            with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=3) as r:
                data = json.loads(r.read().decode("utf-8"))
            names = [m.get("name") for m in data.get("models", []) if m.get("name")]
            self.model.addItems(names or ["llama3.2"])
        except Exception:
            self.model.addItem("llama3.2")
            self.output.setPlainText(
                "Không lấy được danh sách model.\n"
                "Hãy kiểm tra Ollama đang chạy và đã có model."
            )

    def _chat(self):
        prompt = self.prompt.text().strip()
        if not prompt:
            return
        model = self.model.currentText().strip()
        self.output.setPlainText(f"[JARVIS → Ollama: {model}]\nĐang xử lý…")
        self.worker = OllamaWorker(prompt, model, parent=self)
        self.worker.finished.connect(lambda s: self.output.setPlainText(s))
        self.worker.failed.connect(lambda s: self.output.setPlainText(s))
        self.worker.start()

    def _calculate(self):
        expr = self.prompt.text().strip()
        try:
            tree = ast.parse(expr, mode="eval")
            allowed = {
                ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
                ast.Div: op.truediv, ast.FloorDiv: op.floordiv,
                ast.Mod: op.mod, ast.Pow: op.pow,
                ast.USub: op.neg, ast.UAdd: op.pos,
            }
            def ev(n):
                if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
                    return n.value
                if isinstance(n, ast.UnaryOp):
                    return allowed[type(n.op)](ev(n.operand))
                if isinstance(n, ast.BinOp):
                    return allowed[type(n.op)](ev(n.left), ev(n.right))
                raise ValueError("Expression not allowed")
            self.output.setPlainText(str(ev(tree.body)))
        except Exception as e:
            self.output.setPlainText(f"Invalid expression: {e}")

    def _system(self):
        try:
            import psutil
            text = (
                f"Platform: {platform.platform()}\n"
                f"CPU: {psutil.cpu_percent(interval=0.3)}%\n"
                f"RAM: {psutil.virtual_memory().percent}%"
            )
        except Exception:
            text = f"Platform: {platform.platform()}"
        self.output.setPlainText(text)

    def _screenshot(self):
        try:
            from PySide6.QtGui import QGuiApplication
            screen = QGuiApplication.primaryScreen()
            if screen is None:
                raise RuntimeError("No screen")
            path = "jarvis_screenshot.png"
            if screen.grabWindow(0).save(path):
                self.output.setPlainText(f"Saved: {path}")
            else:
                self.output.setPlainText("Screenshot failed.")
        except Exception as e:
            self.output.setPlainText(f"Screenshot error: {e}")

    def _open_app(self):
        name = self.prompt.text().strip().lower()
        apps = {
            "notepad": ["notepad.exe"],
            "calc": ["calc.exe"],
            "calculator": ["calc.exe"],
            "mspaint": ["mspaint.exe"],
            "paint": ["mspaint.exe"],
        }
        if name not in apps:
            self.output.setPlainText("Only safe built-in apps: notepad, calc, mspaint.")
            return
        try:
            subprocess.Popen(apps[name])
            self.output.setPlainText(f"Launched: {name}")
        except Exception as e:
            self.output.setPlainText(f"Launch error: {e}")

    def _search(self):
        q = self.prompt.text().strip()
        if not q:
            return
        url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(q)
        try:
            import webbrowser
            webbrowser.open(url)
            self.output.setPlainText(f"Opened search for: {q}")
        except Exception as e:
            self.output.setPlainText(f"Search error: {e}")
