from PySide6.QtCore import QPointF
from PySide6.QtGui import QPolygonF


class ArmorPiece:

    def __init__(self, points, start, target):

        self.shape = QPolygonF(points)

        self.pos = QPointF(start)

        self.target = QPointF(target)

        self.angle = 180

        self.finished = False

    def update(self):

        if self.finished:
            return

        dx = self.target.x() - self.pos.x()
        dy = self.target.y() - self.pos.y()

        self.pos += QPointF(dx * 0.12, dy * 0.12)

        self.angle *= 0.88

        if abs(dx) < 1 and abs(dy) < 1:
            self.finished = True