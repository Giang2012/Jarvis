from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)

import datetime


class StatusBar(QWidget):

    def __init__(self):
        super().__init__()

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setOffset(0)
        shadow.setColor(QColor(0, 255, 255, 150))

        self.setGraphicsEffect(shadow)

        self.build_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.update_time()

    def build_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(20, 8, 20, 8)
        layout.setSpacing(20)

        self.status = QLabel("SYSTEM READY")
        self.mode = QLabel("MODE : STUDY")
        self.clock = QLabel()

        style = """
        QLabel{
            color:rgb(210,250,255);
            font-size:12px;
            font-family:Consolas;
            background:transparent;
        }
        """

        self.status.setStyleSheet(style)
        self.mode.setStyleSheet(style)
        self.clock.setStyleSheet(style)

        layout.addWidget(self.status)

        layout.addStretch()

        layout.addWidget(self.mode)

        layout.addSpacing(30)

        layout.addWidget(self.clock)

        self.setStyleSheet("""
        QWidget{
            background:rgba(8,15,25,180);
            border-top:1px solid rgba(0,255,255,70);
        }
        """)

    def update_time(self):

        self.clock.setText(
            datetime.datetime.now().strftime("%H:%M:%S   %d/%m/%Y")
        )

    def setStatus(self, text):

        self.status.setText(text)

    def setMode(self, mode):

        self.mode.setText(f"MODE : {mode.upper()}")