from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


class OrbitRenderer:

    def draw(self,painter,particles):

        painter.setPen(Qt.NoPen)

        for p in particles:

            painter.setBrush(

                QColor(

                    0,

                    255,

                    255,

                    180

                )

            )

            painter.drawEllipse(

                p.x,

                p.y,

                p.size,

                p.size

            )