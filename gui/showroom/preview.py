import os
from pathlib import Path
try:
    import PySide6
    site=Path(PySide6.__file__).resolve().parent
    os.environ.setdefault('QT_PLUGIN_PATH',str(site/'plugins'))
    os.environ.setdefault('QT_QPA_PLATFORM_PLUGIN_PATH',str(site/'plugins'/'platforms'))
    os.environ.setdefault('QT_QPA_PLATFORM','windows')
    if (site/'Qt'/'bin').exists(): os.add_dll_directory(str(site/'Qt'/'bin'))
except Exception: pass
from PySide6.QtWidgets import QApplication
from .showroom import ShowroomWindow
app=QApplication([]); w=ShowroomWindow(); w.show(); app.exec()
