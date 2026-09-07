from PySide6.QtWidgets import QMainWindow, QMenuBar
from PySide6.QtCore import Qt

from core.brain import Brain
from gui.dashboard.dashboard import Dashboard
from gui.settings.voice_settings import VoiceSettingsDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW
        # =========================

        self.setWindowTitle(
            "J.A.R.V.I.S"
        )

        self.resize(
            1600,
            900
        )

        self.setStyleSheet(
            """
            QMainWindow {
                background: #05070a;
            }
            """
        )

        # =========================
        # BRAIN
        # =========================

        self.brain = Brain()

        # =========================
        # DASHBOARD
        # =========================

        self.dashboard = Dashboard(
            self.brain
        )

        self.setCentralWidget(
            self.dashboard
        )

        # =========================
        # MODE
        # =========================

        self.brain.mode_manager.setMode(
            "CODING"
        )

        # =========================
        # SETTINGS MENU
        # =========================

        self._build_settings_menu()

        # =========================
        # WINDOW FLAGS
        # =========================

        self.setWindowFlags(
            Qt.FramelessWindowHint
        )

        print(
            "MainWindow Loaded"
        )

    # =========================
    # SETTINGS
    # =========================

    def _build_settings_menu(self):

        menu_bar = QMenuBar(self)

        menu_bar.setStyleSheet(
            """
            QMenuBar {
                background: #080c12;
                color: #d9e7f5;
                padding: 4px;
            }

            QMenuBar::item:selected {
                background: #162332;
            }

            QMenu {
                background: #080c12;
                color: #d9e7f5;
                border: 1px solid #26384b;
            }

            QMenu::item:selected {
                background: #162332;
            }
            """
        )

        settings_menu = menu_bar.addMenu(
            "Settings"
        )

        voice_action = settings_menu.addAction(
            "Voice"
        )

        voice_action.triggered.connect(
            self.open_voice_settings
        )

        self.setMenuBar(
            menu_bar
        )

    def open_voice_settings(self):

        dialog = VoiceSettingsDialog(
            self.brain,
            self
        )

        dialog.exec()

    # =========================
    # CLOSE
    # =========================

    def closeEvent(self, event):

        try:

            voice = getattr(
                self.brain,
                "voice",
                None
            )

            if voice:
                voice.stop()

        finally:

            event.accept()