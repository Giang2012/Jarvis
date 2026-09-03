import sys
from PySide6.QtWidgets import QApplication
from .tool_center import ToolCenter


def main():
    app = QApplication(sys.argv)
    window = ToolCenter()
    window.resize(1600, 900)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
