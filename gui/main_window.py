from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

from core.brain import Brain
from gui.dashboard import Dashboard


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW CONFIG
        # =========================

        self.setWindowTitle(
            "J.A.R.V.I.S"
        )

        self.resize(
            1600,
            900
        )


        # full dark background
        self.setStyleSheet("""
            QMainWindow {
                background-color: #05070a;
            }
        """)


        # =========================
        # AI BRAIN
        # =========================

        self.brain = Brain()


        # =========================
        # DASHBOARD
        # =========================

        self.dashboard = Dashboard()

        self.setCentralWidget(
            self.dashboard
        )


        # remove default frame
        self.setWindowFlags(
            Qt.FramelessWindowHint
        )