from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor

from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QGraphicsDropShadowEffect,
)

import psutil
import datetime

from .glass_panel import GlassPanel


class InfoLabel(QLabel):

    def __init__(self, title):
        super().__init__()

        self.title = title

        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.setStyleSheet("""
        QLabel{
            color:white;
            font-size:13px;
            padding:10px;
            border-radius:10px;
            background:rgba(0,255,255,18);
            border:1px solid rgba(0,255,255,50);
        }
        """)

    def setData(self, value):

        self.setText(f"{self.title}\n{value}")


class RightPanel(GlassPanel):

    def __init__(self):
        super().__init__()

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(40)
        shadow.setOffset(0)
        shadow.setColor(QColor(0,220,255,180))

        self.setGraphicsEffect(shadow)

        self.build_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)
        self.timer.start(1000)

        self.update_info()

    def build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(18,18,18,18)
        layout.setSpacing(14)

        title = QLabel("SYSTEM INFO")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
        QLabel{
            color:white;
            font-size:18px;
            font-weight:bold;
            background:transparent;
        }
        """)

        layout.addWidget(title)

        self.time = InfoLabel("TIME")
        self.network = InfoLabel("NETWORK")
        self.boot = InfoLabel("UPTIME")
        self.battery = InfoLabel("BATTERY")

        layout.addWidget(self.time)
        layout.addWidget(self.network)
        layout.addWidget(self.boot)
        layout.addWidget(self.battery)

        layout.addStretch()

    def update_info(self):

        now = datetime.datetime.now()

        self.time.setData(
            now.strftime("%H:%M:%S")
        )

        net = psutil.net_io_counters()

        self.network.setData(
            f"↑ {net.bytes_sent//1024//1024} MB\n"
            f"↓ {net.bytes_recv//1024//1024} MB"
        )

        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(
            psutil.boot_time()
        )

        hours = uptime.seconds // 3600
        mins = (uptime.seconds % 3600) // 60

        self.boot.setData(
            f"{uptime.days}d {hours}h {mins}m"
        )

        battery = psutil.sensors_battery()

        if battery:
            self.battery.setData(
                f"{battery.percent:.0f}%"
            )
        else:
            self.battery.setData("Desktop")