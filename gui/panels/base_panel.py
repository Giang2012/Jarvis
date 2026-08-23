from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QBrush,
    QFont,
)


class BasePanel:

    def __init__(self, title="SYSTEM"):

        self.title = title

        self.width = 300
        self.height = 220

        self.x = 0
        self.y = 0

        self.userMoved = False

        self.hovered = False
        self.selected = False

        self.dragging = False
        self.dragOffsetX = 0
        self.dragOffsetY = 0

        self.alpha = 185
        self.headerHeight = 42

    # =====================================================
    # POSITION
    # =====================================================

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    # =====================================================
    # HIT TEST
    # =====================================================

    def contains(self, x, y):

        return (
            self.x <= x <= self.x + self.width
            and
            self.y <= y <= self.y + self.height
        )

    def containsHeader(self, x, y, width=None, headerHeight=46):

        return (
            self.x <= x <= self.x + self.width
            and
            self.y <= y <= self.y + headerHeight
        )

    # =====================================================
    # PAINT
    # =====================================================

    def paint(self, painter):

        painter.save()

        rect = QRectF(
            self.x,
            self.y,
            self.width,
            self.height
        )

        # =================================================
        # OUTER GLOW
        # =================================================

        if self.selected:

            for i in range(7):

                alpha = 34 - i * 4

                glowRect = rect.adjusted(
                    -i * 3,
                    -i * 3,
                    i * 3,
                    i * 3
                )

                painter.setPen(
                    QPen(
                        QColor(
                            0,
                            230,
                            255,
                            max(alpha, 0)
                        ),
                        2
                    )
                )

                painter.setBrush(Qt.NoBrush)

                painter.drawRoundedRect(
                    glowRect,
                    12,
                    12
                )

        elif self.hovered:

            painter.setPen(
                QPen(
                    QColor(
                        0,
                        220,
                        255,
                        120
                    ),
                    2
                )
            )

            painter.setBrush(Qt.NoBrush)

            painter.drawRoundedRect(
                rect.adjusted(-3, -3, 3, 3),
                10,
                10
            )

        # =================================================
        # MAIN GLASS
        # =================================================

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                3,
                15,
                25,
                self.alpha
            )
        )

        painter.drawRoundedRect(
            rect,
            10,
            10
        )

        # =================================================
        # INNER GLASS
        # =================================================

        inner = rect.adjusted(
            2,
            2,
            -2,
            -2
        )

        painter.setBrush(
            QColor(
                10,
                40,
                55,
                65
            )
        )

        painter.drawRoundedRect(
            inner,
            8,
            8
        )

        # =================================================
        # TOP GLASS HIGHLIGHT
        # =================================================

        painter.setPen(
            QPen(
                QColor(
                    100,
                    245,
                    255,
                    55
                ),
                1
            )
        )

        painter.drawLine(
            self.x + 18,
            self.y + 2,
            self.x + self.width - 18,
            self.y + 2
        )

        # =================================================
        # BORDER
        # =================================================

        borderAlpha = 150

        if self.hovered:
            borderAlpha = 220

        if self.selected:
            borderAlpha = 255

        painter.setPen(
            QPen(
                QColor(
                    0,
                    220,
                    255,
                    borderAlpha
                ),
                1.5
            )
        )

        painter.setBrush(Qt.NoBrush)

        painter.drawRoundedRect(
            rect,
            10,
            10
        )

        # =================================================
        # HEADER
        # =================================================

        header = QRectF(
            self.x,
            self.y,
            self.width,
            self.headerHeight
        )

        painter.setPen(Qt.NoPen)

        painter.setBrush(
            QColor(
                0,
                190,
                230,
                28 if not self.hovered else 48
            )
        )

        painter.drawRoundedRect(
            header,
            10,
            10
        )

        # =================================================
        # HEADER LINE
        # =================================================

        painter.setPen(
            QPen(
                QColor(
                    0,
                    240,
                    255,
                    100 if not self.hovered else 220
                ),
                1
            )
        )

        painter.drawLine(
            self.x + 14,
            self.y + self.headerHeight,
            self.x + self.width - 14,
            self.y + self.headerHeight
        )

        # =================================================
        # HEADER ENERGY LINE
        # =================================================

        painter.setPen(
            QPen(
                QColor(
                    0,
                    255,
                    255,
                    230
                ),
                2
            )
        )

        painter.drawLine(
            self.x + 14,
            self.y + 11,
            self.x + 14,
            self.y + 29
        )

        painter.setPen(
            QPen(
                QColor(
                    0,
                    255,
                    255,
                    80
                ),
                1
            )
        )

        painter.drawLine(
            self.x + 17,
            self.y + 11,
            self.x + 17,
            self.y + 29
        )

        # =================================================
        # TITLE
        # =================================================

        font = QFont(
            "Segoe UI",
            10,
            QFont.Bold
        )

        painter.setFont(font)

        painter.setPen(
            QColor(
                190,
                248,
                255,
                250
            )
        )

        painter.drawText(
            self.x + 27,
            self.y + 27,
            self.title.upper()
        )

        # =================================================
        # STATUS INDICATOR
        # =================================================

        dotX = self.x + self.width - 28
        dotY = self.y + 20

        painter.setPen(Qt.NoPen)

        # glow
        painter.setBrush(
            QColor(
                0,
                255,
                190,
                35
            )
        )

        painter.drawEllipse(
            QRectF(
                dotX - 4,
                dotY - 4,
                14,
                14
            )
        )

        # core
        painter.setBrush(
            QColor(
                0,
                255,
                180,
                240
            )
        )

        painter.drawEllipse(
            QRectF(
                dotX,
                dotY,
                6,
                6
            )
        )

        # =================================================
        # CORNER HUD
        # =================================================

        painter.setPen(
            QPen(
                QColor(
                    0,
                    230,
                    255,
                    170
                ),
                1
            )
        )

        corner = 13

        # top-left
        painter.drawLine(
            self.x,
            self.y + corner,
            self.x,
            self.y
        )

        painter.drawLine(
            self.x,
            self.y,
            self.x + corner,
            self.y
        )

        # top-right
        painter.drawLine(
            self.x + self.width - corner,
            self.y,
            self.x + self.width,
            self.y
        )

        painter.drawLine(
            self.x + self.width,
            self.y,
            self.x + self.width,
            self.y + corner
        )

        # bottom-left
        painter.drawLine(
            self.x,
            self.y + self.height - corner,
            self.x,
            self.y + self.height
        )

        painter.drawLine(
            self.x,
            self.y + self.height,
            self.x + corner,
            self.y + self.height
        )

        # bottom-right
        painter.drawLine(
            self.x + self.width - corner,
            self.y + self.height,
            self.x + self.width,
            self.y + self.height
        )

        painter.drawLine(
            self.x + self.width,
            self.y + self.height - corner,
            self.x + self.width,
            self.y + self.height
        )

        # =================================================
        # CONTENT
        # =================================================

        self.drawContent(
            painter,
            rect
        )

        painter.restore()

    # =====================================================
    # CONTENT HOOK
    # =====================================================

    def drawContent(self, painter, rect):

        if hasattr(self, "drawBody"):
            self.drawBody(
                painter,
                rect
            )

    # =====================================================
    # DRAG
    # =====================================================

    def startDrag(self, x, y):

        self.dragging = True

        self.dragOffsetX = x - self.x
        self.dragOffsetY = y - self.y

        self.userMoved = True

    # -----------------------------------------------------

    def dragTo(
        self,
        x,
        y,
        screenWidth,
        screenHeight,
        width,
        height
    ):

        if not self.dragging:
            return

        newX = x - self.dragOffsetX
        newY = y - self.dragOffsetY

        newX = max(
            0,
            min(
                newX,
                screenWidth - width
            )
        )

        newY = max(
            0,
            min(
                newY,
                screenHeight - height
            )
        )

        self.x = newX
        self.y = newY

    # -----------------------------------------------------

    def stopDrag(self):

        self.dragging = False