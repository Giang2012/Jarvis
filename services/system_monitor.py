"""
services/system_monitor.py

Realtime System Monitor
"""

import psutil

from PySide6.QtCore import QObject, QTimer

from kernel.event_bus import event_bus
from kernel.events import (
    CPU_UPDATED,
    RAM_UPDATED,
    NETWORK_UPDATED,
)


class SystemMonitor(QObject):

    def __init__(self):

        super().__init__()

        self.timer = QTimer()

        self.timer.setInterval(1000)

        self.timer.timeout.connect(
            self.update_system
        )

        self.last_sent = psutil.net_io_counters().bytes_sent
        self.last_recv = psutil.net_io_counters().bytes_recv

    # ==========================
    # Control
    # ==========================

    def start(self):

        self.timer.start()

    def stop(self):

        self.timer.stop()

    # ==========================
    # Update
    # ==========================

    def update_system(self):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory()

        net = psutil.net_io_counters()

        upload = (
            net.bytes_sent -
            self.last_sent
        ) / 1024

        download = (
            net.bytes_recv -
            self.last_recv
        ) / 1024

        self.last_sent = net.bytes_sent
        self.last_recv = net.bytes_recv

        event_bus.emit(
            CPU_UPDATED,
            cpu
        )

        event_bus.emit(
            RAM_UPDATED,
            {
                "percent": ram.percent,
                "used": ram.used,
                "total": ram.total,
            }
        )

        event_bus.emit(
            NETWORK_UPDATED,
            {
                "upload": upload,
                "download": download,
            }
        )

    # ==========================
    # Snapshot
    # ==========================

    def snapshot(self):

        disk = psutil.disk_usage("/")

        return {

            "cpu": psutil.cpu_percent(),

            "ram": psutil.virtual_memory().percent,

            "disk": disk.percent,

            "battery": (
                psutil.sensors_battery().percent
                if psutil.sensors_battery()
                else None
            )
        }