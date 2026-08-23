import sys

from PySide6.QtWidgets import QApplication

from gui.boot.cinematic.ironman_suit import IronmanSuit


app = QApplication(sys.argv)

w = IronmanSuit()

w.resize(900, 900)

w.show()

sys.exit(app.exec())