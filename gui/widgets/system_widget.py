from gui.widgets.hud_gauge import HUDGauge
from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
)

from kernel.context import context
from kernel.event_bus import event_bus
from kernel.events import (
    CPU_UPDATED,
    RAM_UPDATED,
)

from gui.widgets.glass_card import GlassCard


class SystemWidget(GlassCard):

    def __init__(self, mode_manager):

        super().__init__()
        self.mode_manager = mode_manager
        self.setMinimumHeight(420)
        layout = QVBoxLayout(self)

        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)

        self.cpu = HUDGauge(
            "CPU",
            0,
            self.mode_manager
        )

        self.ram = HUDGauge(
            "RAM",
            0,
            self.mode_manager
        )
        layout.addWidget(self.cpu)
        layout.addWidget(self.ram)

        event_bus.subscribe(
            CPU_UPDATED,
            self.update_cpu
        )

        event_bus.subscribe(
            RAM_UPDATED,
            self.update_ram
        )

        from PySide6.QtCore import QTimer

        QTimer.singleShot(100, self.debug_layout)

    def debug_layout(self):
            print("SystemWidget:", self.geometry())
            print("CPU:", self.cpu.geometry())
            print("RAM:", self.ram.geometry())

    def update_cpu(self, value):

        self.cpu.setValue(value)


    def update_ram(self, value):

        self.ram.setValue(
            value["percent"]
        )