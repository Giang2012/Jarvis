import os
from pathlib import Path

# Standalone preview bootstrap: PySide6 may not find qwindows.dll on Windows.
_here = Path(__file__).resolve()
site = _here.parents[2] / ".venv" / "Lib" / "site-packages" / "PySide6"
if site.exists():
    plugins = site / "plugins"
    platforms = plugins / "platforms"
    os.environ.setdefault("QT_PLUGIN_PATH", str(plugins))
    os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", str(platforms))
    os.environ.setdefault("QT_QPA_PLATFORM", "windows")

from PySide6.QtWidgets import QApplication
from .tool_center import ToolCenter

app = QApplication([])
w = ToolCenter()
w.setWindowTitle("J.A.R.V.I.S — Tool Center")
w.resize(1450, 850)
w.show()
app.exec()
