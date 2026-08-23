import sys
from PySide6.QtWidgets import QApplication

from gui.boot.boot_screen import BootScreen
from gui.main_window import MainWindow

window = None
boot = None


def open_main_window():

    global window

    window = MainWindow()

    window.show()

    QApplication.processEvents()

    # ========= START VOICE =========

    if window.brain and hasattr(window.brain, "voice"):

        import threading

        threading.Thread(
            target=window.brain.voice.run,
            daemon=True
        ).start()

    # ===============================


def main():

    global boot

    app = QApplication(sys.argv)

    boot = BootScreen()

    boot.bootFinished.connect(open_main_window)

    boot.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()