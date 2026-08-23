from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
)

from PySide6.QtCore import Qt


class SystemCard(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setSpacing(12)

        title = QLabel("SYSTEM")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
        QLabel{

            color:#00DDFF;

            font-size:18px;

            font-weight:bold;

            background:transparent;

        }
        """)

        layout.addWidget(title)

        self.cpu = self.makeBar("CPU")

        self.ram = self.makeBar("RAM")

        self.gpu = self.makeBar("GPU")

        layout.addWidget(self.cpu)

        layout.addWidget(self.ram)

        layout.addWidget(self.gpu)

    def makeBar(self, name):

        widget = QWidget()

        layout = QVBoxLayout(widget)

        label = QLabel(name)

        label.setStyleSheet("""
        color:white;
        background:transparent;
        """)

        bar = QProgressBar()

        bar.setRange(0,100)

        bar.setValue(45)

        bar.setTextVisible(True)

        bar.setStyleSheet("""

        QProgressBar{

            border:1px solid #00DDFF;

            background:#111;

            height:16px;

            color:white;

        }

        QProgressBar::chunk{

            background:#00DDFF;

        }

        """)

        layout.addWidget(label)

        layout.addWidget(bar)

        return widget