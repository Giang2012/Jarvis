from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

from gui.widgets.ai_core import AICore


class CentralPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("J.A.R.V.I.S CORE")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
        QLabel{
            color:rgb(220,255,255);
            font-size:24px;
            font-weight:bold;
            letter-spacing:3px;
            background:transparent;
        }
        """)

        self.core = AICore()

        layout.addStretch()

        layout.addWidget(title)

        layout.addWidget(
            self.core,
            alignment=Qt.AlignCenter
        )

        layout.addStretch()

        self.setLayout(layout)

        self.setStyleSheet("""
        QWidget{
            background:transparent;
        }
        """)