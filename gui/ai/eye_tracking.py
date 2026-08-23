from PySide6.QtCore import *
import math


class EyeTracking:

    def __init__(self):

        self.offset = QPointF()

    # --------------------------

    def update(self, mouse):

        self.offset = QPointF(

            mouse.x() * 0.015,

            mouse.y() * 0.015

        )

    # --------------------------

    def left(self):

        return QPointF(

            -18,

            -8

        ) + self.offset

    # --------------------------

    def right(self):

        return QPointF(

            18,

            -8

        ) + self.offset