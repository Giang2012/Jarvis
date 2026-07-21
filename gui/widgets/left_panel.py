from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QGraphicsDropShadowEffect,
)

import psutil

from .glass_panel import GlassPanel
from .hud_gauge import HUDGauge


class LeftPanel(GlassPanel):

    def __init__(self):
        super().__init__()

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setOffset(0)
        shadow.setColor(QColor(0, 220, 255, 180))
        self.setGraphicsEffect(shadow)

        self.build_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)

        self.update_info()

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(18)

        title = QLabel("SYSTEM")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
        QLabel{
            color:rgb(210,245,255);
            font-size:18px;
            font-weight:bold;
            letter-spacing:2px;
            background:transparent;
        }
        """)

        layout.addWidget(title)

        self.cpu = HUDGauge("CPU")
        self.ram = HUDGauge("RAM")
        self.disk = HUDGauge("DISK")

        layout.addWidget(self.cpu, alignment=Qt.AlignCenter)
        layout.addWidget(self.ram, alignment=Qt.AlignCenter)
        layout.addWidget(self.disk, alignment=Qt.AlignCenter)

        layout.addStretch()

    def update_info(self):

        self.cpu.setValue(int(psutil.cpu_percent(interval=None)))

        self.ram.setValue(
            int(psutil.virtual_memory().percent)
        )

        try:
            disk = psutil.disk_usage("C:\\").percent
        except Exception:
            disk = psutil.disk_usage("/").percent

        self.disk.setValue(int(disk))