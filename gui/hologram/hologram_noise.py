from PySide6.QtGui import *
from PySide6.QtCore import *

import random


class HologramNoise:

    def draw(self, painter, rect):

        painter.save()

        painter.setPen(

            QColor(

                0,

                255,

                255,

                25

            )

        )

        for _ in range(35):

            x = random.randint(

                int(rect.left()),

                int(rect.right())

            )

            y = random.randint(

                int(rect.top()),

                int(rect.bottom())

            )

            painter.drawPoint(

                x,

                y

            )

        painter.restore()