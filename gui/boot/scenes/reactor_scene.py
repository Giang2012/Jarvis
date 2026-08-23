from PySide6.QtGui import QPainter

from gui.boot.reactor.reactor import Reactor


class ReactorScene:

    def __init__(self):

        self.reactor = Reactor()

    # ----------------------------

    def update(self):

        self.reactor.update()

    # ----------------------------

    def paint(self, painter: QPainter, rect):

        self.update()

        painter.save()

        painter.translate(

            rect.center()

        )

        self.reactor.draw(

            painter

        )

        painter.restore()