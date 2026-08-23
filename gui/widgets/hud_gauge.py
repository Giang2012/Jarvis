import math

from PySide6.QtCore import (
    Qt,
    QTimer,
    QSize,
)

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QFont,
)

from PySide6.QtWidgets import QWidget


class HUDGauge(QWidget):

    def __init__(self, title, value, mode_manager):
        super().__init__()

        self.mode_manager = mode_manager

        self.title = title
        self.value = value

        self.mode_manager.modeChanged.connect(
            self.update
        )
        self.rotation = 0
        self.pulse = 0
        self.pulse_dir = 1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)



    def animate(self):

        self.rotation += 1.2

        if self.rotation >= 360:
            self.rotation = 0

        self.pulse += self.pulse_dir

        if self.pulse > 15:
            self.pulse_dir = -1

        if self.pulse < 0:
            self.pulse_dir = 1

        self.update()

    def setValue(
        self,
        value
    ):

        self.value = max(
            0,
            min(
                100,
                value
            )
        )

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        cx = self.width() / 2
        cy = self.height() / 2
        color = self.mode_manager.color()

        radius = min(
            self.width(),
            self.height()
        ) / 2 - 20

        painter.translate(cx, cy)
        painter.rotate(self.rotation)

        # =============================
        # Glow Ring
        # =============================

        glow = QColor(
            color.red(),
            color.green(),
            color.blue(),
            25 + self.pulse * 2
        )

        painter.setPen(
            QPen(
                glow,
                16
            )
        )

        painter.drawEllipse(
            int(-radius),
            int(-radius),
            int(radius * 2),
            int(radius * 2)
        )

        # =============================
        # Outer Ring
        # =============================

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    45
                ),
                8
            )
        )

        painter.drawEllipse(
            int(-radius),
            int(-radius),
            int(radius * 2),
            int(radius * 2)
        )

        # =============================
        # Tick Marks
        # =============================

        for i in range(60):

            angle = math.radians(i * 6)

            if i % 5 == 0:
                inner = radius - 14
                outer = radius
                width = 2
            else:
                inner = radius - 8
                outer = radius
                width = 1

            x1 = math.cos(angle) * inner
            y1 = math.sin(angle) * inner

            x2 = math.cos(angle) * outer
            y2 = math.sin(angle) * outer

            painter.setPen(
                QPen(
                    QColor(
                        color.red(),
                        color.green(),
                        color.blue(),
                        120
                    ),
                    width
                )
            )

            painter.drawLine(
                int(x1),
                int(y1),
                int(x2),
                int(y2)
            )

        # =============================
        # Progress Arc
        # =============================

        painter.setPen(
            QPen(
                    color,
                10
            )
        )

        rect = (
            int(-radius + 12),
            int(-radius + 12),
            int((radius - 12) * 2),
            int((radius - 12) * 2)
        )

        painter.drawArc(
            *rect,
            90 * 16,
            -int(
                self.value *
                360 /
                100
            ) * 16
        )

        painter.resetTransform()
        # =============================
        # Center Glow
        # =============================

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        center_radius = 42 + self.pulse * 0.3

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                color.red(),
                color.green(),
                color.blue(),
                40
            )
        )

        painter.drawEllipse(
            int(cx - center_radius),
            int(cy - center_radius),
            int(center_radius * 2),
            int(center_radius * 2)
        )

        bg = self.mode_manager.background()

        painter.setBrush(
            QColor(
                bg.red(),
                bg.green(),
                bg.blue(),
                220
            )
        )
        painter.drawEllipse(
            int(cx - 36),
            int(cy - 36),
            72,
            72
        )

        # =============================
        # Value
        # =============================

        painter.setPen(
            QColor(
                255,
                255,
                255
            )
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                18,
                QFont.Bold
            )
        )

        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            f"{self.value:.0f}%"
        )

        # =============================
        # Title
        # =============================

        painter.setPen(
            color
        )

        painter.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Bold
            )
        )

        painter.drawText(
            0,
            self.height() - 18,
            self.width(),
            20,
            Qt.AlignHCenter,
            self.title
        )

        # =============================
        # Scan Ring
        # =============================

        painter.save()

        painter.translate(
            cx,
            cy
        )

        painter.rotate(
            self.rotation * 2
        )

        painter.setPen(
            QPen(
                QColor(
                    color.red(),
                    color.green(),
                    color.blue(),
                    180
                ),
                2
            )
        )

        painter.drawLine(
            0,
            0,
            0,
            -int(radius * 0.7)
        )

        painter.restore()
    def sizeHint(self):
        return QSize(180, 180)

    def minimumSizeHint(self):
        return QSize(180, 180)