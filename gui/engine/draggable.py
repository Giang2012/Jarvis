from PySide6.QtCore import QPointF


class Draggable:

    def __init__(self):

        self.position = QPointF(0, 0)
        self.target = QPointF(0, 0)

        self.speed = 0.45

        self.dragging = False
        self.dragOffset = QPointF(0, 0)

        self.userMoved = False

    # --------------------------------

    def setPosition(self, x, y):

        self.position.setX(x)
        self.position.setY(y)

        self.target.setX(x)
        self.target.setY(y)

    # --------------------------------

    def moveTo(self, x, y):

        self.target.setX(x)
        self.target.setY(y)

    # --------------------------------
    # DRAG
    # --------------------------------

    def startDrag(self, mouseX, mouseY):

        self.dragging = True
        self.userMoved = True

        self.dragOffset = QPointF(
            mouseX - self.position.x(),
            mouseY - self.position.y()
        )

    # --------------------------------

    def dragTo(
        self,
        mouseX,
        mouseY,
        screenWidth=None,
        screenHeight=None,
        width=None,
        height=None
    ):

        if not self.dragging:
            return

        x = mouseX - self.dragOffset.x()
        y = mouseY - self.dragOffset.y()

        # --------------------------------
        # Screen bounds
        # --------------------------------

        if screenWidth is not None and width is not None:

            x = max(
                5,
                min(
                    x,
                    screenWidth - width - 5
                )
            )

        if screenHeight is not None and height is not None:

            y = max(
                5,
                min(
                    y,
                    screenHeight - height - 5
                )
            )

        self.position.setX(x)
        self.position.setY(y)

        self.target.setX(x)
        self.target.setY(y)

    # --------------------------------

    def stopDrag(self):

        self.dragging = False

        self.target.setX(
            self.position.x()
        )

        self.target.setY(
            self.position.y()
        )

    # --------------------------------

    def contains(
        self,
        x,
        y,
        width,
        height
    ):

        return (
            self.position.x()
            <= x
            <= self.position.x() + width
            and
            self.position.y()
            <= y
            <= self.position.y() + height
        )

    # --------------------------------

    def containsHeader(
        self,
        x,
        y,
        width,
        headerHeight=46
    ):

        return (
            self.position.x()
            <= x
            <= self.position.x() + width
            and
            self.position.y()
            <= y
            <= self.position.y() + headerHeight
        )

    # --------------------------------

    def update(self):

        if self.dragging:
            return

        dx = self.target.x() - self.position.x()
        dy = self.target.y() - self.position.y()

        self.position.setX(
            self.position.x() + dx * self.speed
        )

        self.position.setY(
            self.position.y() + dy * self.speed
        )