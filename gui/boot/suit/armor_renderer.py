from PySide6.QtGui import *
from PySide6.QtCore import *

from gui.boot.suit.armor_piece import ArmorPiece


class ArmorRenderer:

    def __init__(self):

        self.parts = []

        self.create()

    # =====================================

    def create(self):

        cyan = QColor(0,255,255)

        # ---------------- Helmet ----------------

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-28,-55),

                    QPointF(28,-55),

                    QPointF(38,-25),

                    QPointF(-38,-25)

                ],

                QPointF(-600,-300),

                QPointF(0,-170)

            )

        )

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-32,-25),

                    QPointF(32,-25),

                    QPointF(24,25),

                    QPointF(-24,25)

                ],

                QPointF(650,-280),

                QPointF(0,-115)

            )

        )

        # ---------------- Chest ----------------

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-70,-40),

                    QPointF(70,-40),

                    QPointF(55,50),

                    QPointF(-55,50)

                ],

                QPointF(-700,0),

                QPointF(0,0)

            )

        )

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-45,50),

                    QPointF(45,50),

                    QPointF(35,120),

                    QPointF(-35,120)

                ],

                QPointF(700,50),

                QPointF(0,80)

            )

        )

        # ---------------- Shoulder ----------------

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-25,-20),

                    QPointF(25,-20),

                    QPointF(20,20),

                    QPointF(-20,20)

                ],

                QPointF(-600,-50),

                QPointF(-95,-10)

            )

        )

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-25,-20),

                    QPointF(25,-20),

                    QPointF(20,20),

                    QPointF(-20,20)

                ],

                QPointF(600,-50),

                QPointF(95,-10)

            )

        )

        # ---------------- Arms ----------------

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-12,-45),

                    QPointF(12,-45),

                    QPointF(12,45),

                    QPointF(-12,45)

                ],

                QPointF(-700,100),

                QPointF(-125,70)

            )

        )

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-12,-45),

                    QPointF(12,-45),

                    QPointF(12,45),

                    QPointF(-12,45)

                ],

                QPointF(700,100),

                QPointF(125,70)

            )

        )

        # ---------------- Legs ----------------

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-15,-60),

                    QPointF(15,-60),

                    QPointF(15,60),

                    QPointF(-15,60)

                ],

                QPointF(-300,700),

                QPointF(-35,210)

            )

        )

        self.parts.append(

            ArmorPiece(

                [

                    QPointF(-15,-60),

                    QPointF(15,-60),

                    QPointF(15,60),

                    QPointF(-15,60)

                ],

                QPointF(300,700),

                QPointF(35,210)

            )

        )

    # =====================================

    def update(self):

        for p in self.parts:

            p.update()

    # =====================================

    def draw(self,painter):

        self.update()

        painter.save()

        pen = QPen(QColor(0,255,255),3)

        painter.setPen(pen)

        painter.setBrush(Qt.NoBrush)

        for part in self.parts:

            painter.save()

            painter.translate(part.pos)

            painter.rotate(part.angle)

            painter.drawPolygon(part.shape)

            painter.restore()

        painter.restore()