from PySide6.QtCore import QPointF


class Transform:

    def __init__(self):

        self.position = QPointF()

        self.rotation = 0

        self.scale = 1

        self.depth = 0

        self.visible = True

        self.opacity = 1

    # ----------------------------

    def move(self, dx, dy):

        self.position += QPointF(dx, dy)

    def setPosition(self, x, y):

        self.position.setX(x)

        self.position.setY(y)


    def rotate(self, angle):

        self.rotation += angle


    def setScale(self, scale):

        self.scale = scale