from __future__ import annotations

import os
import sys
import threading
from pathlib import Path


def _bootstrap_qt() -> None:

    import PySide6

    pyside_root = Path(
        PySide6.__file__
    ).resolve().parent

    candidates = [
        pyside_root / "plugins",
        pyside_root / "Qt" / "plugins",
    ]

    plugin_root = next(
        (
            p
            for p in candidates
            if (
                p
                / "platforms"
                / "qwindows.dll"
            ).exists()
        ),
        None,
    )

    if plugin_root is None:

        raise RuntimeError(
            "PySide6 is installed, but "
            "qwindows.dll was not found. "
            f"Checked: {candidates}"
        )

    platform_dir = (
        plugin_root / "platforms"
    )

    os.environ[
        "QT_PLUGIN_PATH"
    ] = str(plugin_root)

    os.environ[
        "QT_QPA_PLATFORM_PLUGIN_PATH"
    ] = str(platform_dir)

    os.environ.setdefault(
        "QT_QPA_PLATFORM",
        "windows"
    )

    if sys.platform == "win32":

        qt_bin = (
            pyside_root
            / "Qt"
            / "bin"
        )

        if (
            qt_bin.is_dir()
            and hasattr(
                os,
                "add_dll_directory"
            )
        ):

            try:
                os.add_dll_directory(
                    str(qt_bin)
                )
            except OSError:
                pass

    print(
        f"[JARVIS] PySide6: "
        f"{pyside_root}"
    )

    print(
        f"[JARVIS] Qt plugins: "
        f"{plugin_root}"
    )

    print(
        f"[JARVIS] QWindows plugin: "
        f"{platform_dir / 'qwindows.dll'}"
    )


_bootstrap_qt()


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

    # =========================
    # START VOICE ENGINE
    # =========================

    voice = getattr(
        window.brain,
        "voice",
        None
    )

    if voice is not None:

        threading.Thread(
            target=voice.run,
            daemon=True,
            name="JARVISVoice"
        ).start()

        print(
            "[JARVIS] Voice Engine started."
        )


def main():

    global boot

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        "JARVIS"
    )

    boot = BootScreen()

    boot.bootFinished.connect(
        open_main_window
    )

    boot.show()

    return app.exec()


if __name__ == "__main__":

    raise SystemExit(
        main()
    )