from PySide6.QtCore import QPointF


class Camera:

    def __init__(self):

        self.position = QPointF()

        self.zoom = 1

        self.rotation = 0