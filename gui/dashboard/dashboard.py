from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QTimer

from gui.dashboard.layout import DashboardLayout
from gui.dashboard.animation import DashboardAnimation

# Effects
from gui.common.effects.grid import Grid
from gui.common.effects.corner_hud import CornerHUD

# Panels
from gui.panels.system_panel import SystemPanel
from gui.panels.weather_panel import WeatherPanel
from gui.panels.calendar_panel import CalendarPanel
from gui.panels.task_panel import TaskPanel
from gui.panels.music_panel import MusicPanel
from gui.panels.notification_panel import NotificationPanel
from gui.panels.ai_status_panel import AIStatusPanel
from gui.components.top_status_bar import TopStatusBar
# Components
from gui.components.status_bar import StatusBar

# Scene
from gui.scene.main_scene import MainScene
from gui.engine.renderer import Renderer


class Dashboard(QWidget):

    def __init__(self, brain=None):

        super().__init__()

        self.brain = brain

        self.draggedPanel = None

        self.hoveredPanel = None


        self.setAttribute(Qt.WA_TranslucentBackground)

        self.layoutEngine = DashboardLayout()
        self.animation = DashboardAnimation()

        # ---------- Panels ----------

        self.system = SystemPanel()
        self.weather = WeatherPanel()
        self.calendar = CalendarPanel()
        self.tasks = TaskPanel()
        self.music = MusicPanel()
        self.notification = NotificationPanel()
        self.aiStatus = AIStatusPanel()

        self.panels = [
            self.system,
            self.tasks,
            self.weather,
            self.calendar,
            self.music,
            self.notification,
            self.aiStatus
        ]

        self.statusBar = StatusBar()

        self.topStatusBar = TopStatusBar()

        # ---------- Scene ----------

        self.scene = MainScene()
        self.renderer = Renderer()

        # ---------- Timer ----------

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    # ---------------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        self.animation.update()

        w = self.width()
        h = self.height()

        self.layoutEngine.calculate(w, h)
        L = self.layoutEngine

        # ---------- Background ----------

        Grid.draw(painter, self.rect())
        CornerHUD.draw(painter, self.rect())

        self.topStatusBar.draw(
            painter,
            w
        )

        painter.save()

        # ---------- Left ----------

        if not self.system.userMoved:
            self.system.setPosition(
                L.leftTop.x(),
                L.leftTop.y()
            )

        self.system.paint(painter)

        if not self.tasks.userMoved:
            self.tasks.setPosition(
                L.leftBottom.x(),
                L.leftBottom.y()
            )

        self.tasks.paint(painter)

        # ---------- Right ----------

        if not self.weather.userMoved:
            self.weather.setPosition(
                L.rightTop.x(),
                L.rightTop.y()
            )

        self.weather.paint(painter)

        if not self.calendar.userMoved:
            self.calendar.setPosition(
                L.rightBottom.x(),
                L.rightBottom.y()
            )

        self.calendar.paint(painter)

        # ---------- Scene ----------

        self.scene.update()

        self.renderer.render(
            painter,
            self.scene
        )

        # ---------- Status ----------

        if hasattr(L, "status"):
            self.statusBar.paint(
                painter,
                L.status
            )

        # ---------- Time ----------

        painter.restore()

    # ---------------------------------------------------------
    # PANEL DRAGGING
    # ---------------------------------------------------------

    def mousePressEvent(self, event):

        if event.button() != Qt.LeftButton:
            return

        pos = event.position()

        for panel in reversed(self.panels):

            if panel.contains(
                pos.x(),
                pos.y()
            ):

                panel.startDrag(
                    pos.x(),
                    pos.y()
                )

                self.draggedPanel = panel

                for p in self.panels:
                    p.selected = False

                panel.selected = True

                self.update()

                return


    # ---------------------------------------------------------

    def mouseMoveEvent(self, event):

        pos = event.position()

        # -------------------------
        # Drag
        # -------------------------

        if self.draggedPanel is not None:

            self.draggedPanel.dragTo(
                pos.x(),
                pos.y(),
                self.width(),
                self.height(),
                self.draggedPanel.width,
                self.draggedPanel.height
            )

            self.update()

            return

        # -------------------------
        # Hover
        # -------------------------

        hovered = None

        for panel in reversed(self.panels):

            if panel.containsHeader(
                pos.x(),
                pos.y()
            ):

                hovered = panel

                break

        self.hoveredPanel = hovered

        for panel in self.panels:

            panel.hovered = (
                panel is hovered
            )

        self.update()


    # ---------------------------------------------------------

    def mouseReleaseEvent(self, event):

        if event.button() != Qt.LeftButton:
            return

        if self.draggedPanel is not None:

            self.draggedPanel.stopDrag()

            self.draggedPanel = None

        self.update()