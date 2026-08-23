from PySide6.QtGui import *
from PySide6.QtCore import *
from datetime import datetime


class TopStatusBar:

    def draw(self, painter, width):

        now = datetime.now()

        painter.save()

        # =====================================================
        # BAR
        # =====================================================

        bar_y = 18
        bar_h = 58

        painter.setPen(
            QPen(
                QColor(0, 220, 255, 90),
                1
            )
        )

        painter.setBrush(
            QColor(3, 15, 24, 145)
        )

        painter.drawRoundedRect(
            24,
            bar_y,
            width - 48,
            bar_h,
            8,
            8
        )

        # =====================================================
        # LEFT : JARVIS
        # =====================================================

        painter.setPen(
            QColor(170, 245, 255, 240)
        )

        painter.setFont(
            QFont(
                "Consolas",
                12,
                QFont.Bold
            )
        )

        painter.drawText(
            42,
            bar_y + 24,
            "J.A.R.V.I.S"
        )

        painter.setPen(
            QColor(0, 255, 255, 150)
        )

        painter.setFont(
            QFont(
                "Consolas",
                7
            )
        )

        painter.drawText(
            43,
            bar_y + 42,
            "AI CORE // V3.0.0"
        )

        # =====================================================
        # CENTER LEFT : FRIDAY
        # =====================================================

        center_x = width * 0.38

        painter.setPen(
            QColor(0, 255, 255, 180)
        )

        painter.setFont(
            QFont(
                "Consolas",
                8,
                QFont.Bold
            )
        )

        painter.drawText(
            center_x,
            bar_y + 19,
            "FRIDAY"
        )

        painter.setPen(
            QColor(130, 210, 225, 160)
        )

        painter.setFont(
            QFont(
                "Consolas",
                7
            )
        )

        painter.drawText(
            center_x,
            bar_y + 37,
            now.strftime("%d %b %Y").upper()
        )

        # =====================================================
        # CLOCK
        # =====================================================

        clock_x = width * 0.50

        painter.setPen(
            QColor(190, 255, 255, 245)
        )

        painter.setFont(
            QFont(
                "Consolas",
                17,
                QFont.Bold
            )
        )

        painter.drawText(
            clock_x,
            bar_y + 34,
            now.strftime("%H:%M:%S")
        )

        painter.setPen(
            QColor(0, 255, 255, 150)
        )

        painter.setFont(
            QFont(
                "Consolas",
                7
            )
        )

        painter.drawText(
            clock_x + 105,
            bar_y + 33,
            "LOCAL"
        )

        # =====================================================
        # MODE
        # =====================================================

        mode_x = width * 0.67

        painter.setPen(
            QColor(0, 255, 255, 210)
        )

        painter.setFont(
            QFont(
                "Consolas",
                8,
                QFont.Bold
            )
        )

        painter.drawText(
            mode_x,
            bar_y + 21,
            "[ CODING MODE ]"
        )

        painter.setPen(
            QColor(100, 220, 235, 130)
        )

        painter.setFont(
            QFont(
                "Consolas",
                7
            )
        )

        painter.drawText(
            mode_x,
            bar_y + 39,
            "AI ASSISTANT ACTIVE"
        )

        # =====================================================
        # STATUS
        # =====================================================

        status_x = width - 245

        # Voice
        painter.setPen(
            QPen(
                QColor(0, 255, 180, 210),
                2
            )
        )

        painter.drawLine(
            status_x,
            bar_y + 22,
            status_x,
            bar_y + 34
        )

        painter.drawLine(
            status_x + 4,
            bar_y + 18,
            status_x + 4,
            bar_y + 38
        )

        painter.drawLine(
            status_x + 8,
            bar_y + 24,
            status_x + 8,
            bar_y + 32
        )

        # Network
        net_x = status_x + 32

        painter.setPen(
            QColor(0, 255, 180, 210)
        )

        painter.setFont(
            QFont(
                "Consolas",
                7,
                QFont.Bold
            )
        )

        painter.drawText(
            net_x,
            bar_y + 24,
            "NET"
        )

        painter.setPen(
            QColor(130, 220, 230, 170)
        )

        painter.drawText(
            net_x,
            bar_y + 38,
            "ONLINE"
        )

        # Battery
        bat_x = net_x + 48

        painter.setPen(
            QPen(
                QColor(0, 255, 180, 210),
                1
            )
        )

        painter.setBrush(Qt.NoBrush)

        painter.drawRect(
            bat_x,
            bar_y + 22,
            22,
            11
        )

        painter.drawRect(
            bat_x + 22,
            bar_y + 25,
            3,
            5
        )

        painter.setBrush(
            QColor(0, 255, 180, 190)
        )

        painter.drawRect(
            bat_x + 3,
            bar_y + 25,
            16,
            5
        )

        painter.setPen(
            QColor(130, 220, 230, 170)
        )

        painter.setFont(
            QFont(
                "Consolas",
                7
            )
        )

        painter.drawText(
            bat_x,
            bar_y + 43,
            "100%"
        )

        # =====================================================
        # BOTTOM ACCENT
        # =====================================================

        painter.setPen(
            QPen(
                QColor(0, 255, 255, 80),
                1
            )
        )

        painter.drawLine(
            42,
            bar_y + bar_h - 5,
            width - 42,
            bar_y + bar_h - 5
        )

        painter.restore()