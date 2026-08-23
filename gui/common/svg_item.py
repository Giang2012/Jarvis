from PySide6.QtCore import QRectF

from gui.common.svg_loader import SVGLoader


class SVGItem:

    def __init__(

        self,

        path,

        width,

        height

    ):

        self.renderer = SVGLoader.load(path)

        self.width = width

        self.height = height

        self.opacity = 1

        self.rotation = 0

        self.scale = 1

    # -----------------------

    def draw(

        self,

        painter,

        x,

        y

    ):

        painter.save()

        painter.translate(x, y)

        painter.rotate(self.rotation)

        painter.scale(

            self.scale,

            self.scale

        )

        painter.setOpacity(

            self.opacity

        )

        self.renderer.render(

            painter,

            QRectF(

                -self.width / 2,

                -self.height / 2,

                self.width,

                self.height

            )

        )

        painter.restore()