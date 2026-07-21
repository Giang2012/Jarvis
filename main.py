import sys

from PySide6.QtWidgets import QApplication

from gui.boot_screen import BootScreen
from gui.main_window import MainWindow


app = QApplication(sys.argv)

boot = BootScreen()


def open_dashboard():
    global window

    window = MainWindow()
    window.show()

    boot.close()


boot.bootFinished.connect(open_dashboard)

boot.show()

sys.exit(app.exec())