from PySide6.QtCore import *


class MouseTracker:

    def __init__(self):

        self.position = QPointF()

        self.smooth = QPointF()

    # ----------------------------

    def setPosition(self, pos):

        self.position = pos

    # ----------------------------

    def update(self):

        self.smooth += (

            self.position - self.smooth

        ) * 0.15

    # ----------------------------

    def get(self):

        return self.smooth