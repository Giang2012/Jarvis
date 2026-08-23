from PySide6.QtCore import QRect


class DashboardLayout:

    def __init__(self):

        # =========================
        # PANEL
        # =========================

        self.margin = 35

        self.panelWidth = 300
        self.panelHeight = 220

        self.space = 35
        self.topOffset = 80

        # =========================
        # AI CORE
        # =========================

        self.centerSize = 620

        self.coreOffsetY = 0

        # =========================
        # STATUS
        # =========================

        self.bottomHeight = 45
        self.statusMargin = 25

    # ====================================================
    # CALCULATE
    # ====================================================

    def calculate(self, width, height):

        # =================================================
        # AI CORE
        # =================================================

        coreX = (
            width - self.centerSize
        ) // 2

        coreY = (
            height - self.centerSize
        ) // 2

        coreY += self.coreOffsetY

        self.center = QRect(
            coreX,
            coreY,
            self.centerSize,
            self.centerSize
        )

        # =================================================
        # PANELS
        # =================================================

        # LEFT

        leftX = self.margin

        self.leftTop = QRect(
            leftX,
            self.topOffset,
            self.panelWidth,
            self.panelHeight
        )

        self.leftBottom = QRect(
            leftX,
            self.topOffset
            + self.panelHeight
            + self.space,
            self.panelWidth,
            self.panelHeight
        )

        # RIGHT

        rightX = (
            width
            - self.margin
            - self.panelWidth
        )

        self.rightTop = QRect(
            rightX,
            self.topOffset,
            self.panelWidth,
            self.panelHeight
        )

        self.rightBottom = QRect(
            rightX,
            self.topOffset
            + self.panelHeight
            + self.space,
            self.panelWidth,
            self.panelHeight
        )

        # =================================================
        # STATUS BAR
        # =================================================

        self.status = QRect(
            self.statusMargin,
            height - 60,
            width - self.statusMargin * 2,
            self.bottomHeight
        )