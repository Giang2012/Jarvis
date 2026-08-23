from gui.engine.component import Component


class DragComponent(Component):

    def __init__(self):

        super().__init__()

        self.dragging = False

    # ------------------------

    def startDrag(self):

        self.dragging = True

    # ------------------------

    def stopDrag(self):

        self.dragging = False

    # ------------------------

    def update(self):

        if not self.dragging:

            return

        # Sau này lấy chuột hoặc camera
        pass