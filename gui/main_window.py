from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

from core.brain import Brain
from gui.dashboard.dashboard import Dashboard


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW
        # =========================

        self.setWindowTitle("J.A.R.V.I.S")

        self.resize(1600, 900)

        self.setStyleSheet("""
        QMainWindow{
            background:#05070a;
        }
        """)

        # =========================
        # AI
        # =========================


        # =========================
        # UI
        # =========================

        try:
            self.brain = Brain()
        except Exception as e:
            print("Brain disabled:", e)
            self.brain = None

        self.dashboard = Dashboard(self.brain)

        self.setCentralWidget(self.dashboard)

        # =========================
        # MODE
        # =========================
        if self.brain is not None:
                self.brain.mode_manager.setMode("CODING")

        # =========================
        # WINDOW FLAGS
        # =========================

        self.setWindowFlags(
            Qt.FramelessWindowHint
        )

        print("MainWindow Loaded")