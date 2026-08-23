from PySide6.QtCore import QRectF

from gui.common.panels.glass_panel import GlassPanel

from gui.common.panels.panel_title import PanelTitle
class BasePanel:

    def __init__(self,title=""):

        self.title = title

        self.panel = GlassPanel()

        self.titleDrawer = PanelTitle()

    # ----------------------------------

    def draw(self,painter,x,y,w,h):

        rect = QRectF(
            x,
            y,
            w,
            h
        )

        self.panel.draw(
            painter,
            rect
        )

        self.drawContent(
            painter,
            rect
        )

        self.panel.draw(
            painter,
            rect
        )

        self.titleDrawer.draw(
            painter,
            rect,
            self.title
        )

        self.drawContent(
            painter,
            rect
        )

    # ----------------------------------

    def drawContent(self,painter,rect):

        pass