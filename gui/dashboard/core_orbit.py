import math
import random

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QBrush, QPen


class CoreOrbitSystem:
    """
    Handles mode-module deployment around the central AI core.

    Lifecycle:
        TOOLBAR SIDE
            -> LAUNCH
            -> ORBIT ENTRY
            -> CONTINUOUS ORBIT
            -> RETRACT TO SIDE
    """

    def __init__(self):

        self.states = {}
        self.time = 0.0

        self.orbit_rx = 410.0
        self.orbit_ry = 145.0

        self.deploy_speed = 0.055
        self.retract_speed = 0.065

        self.orbit_speed = 0.0085

        self._rng = random.Random(7319)

    # =========================================================
    # MODULE SET
    # =========================================================

    def set_modules(self, names, panel_map):

        wanted = list(dict.fromkeys(names))

        # Existing modules keep their orbital phase.
        for name, state in list(self.states.items()):

            if name not in wanted:
                state["active"] = False

        # Deploy newly requested modules.
        for index, name in enumerate(wanted):

            if name in self.states:

                state = self.states[name]
                state["active"] = True
                continue

            panel = panel_map.get(name)

            if panel is None:
                continue

            # Alternate launch side so modules enter from both sides.
            side = -1 if index % 2 == 0 else 1

            # Spread entry phases around the visible front arc.
            phase = (
                math.pi
                if side < 0
                else 0.0
            )

            phase += (
                (index % 3 - 1)
                * 0.22
            )

            self.states[name] = {
                "panel": panel,
                "active": True,
                "progress": 0.0,
                "angle": phase,
                "phase_offset": (
                    self._rng.random() * math.tau
                ),
                "side": side,
            }

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, dt=0.016):

        self.time += dt

        remove = []

        for name, state in self.states.items():

            if state["active"]:

                state["progress"] += self.deploy_speed

                if state["progress"] > 1.0:
                    state["progress"] = 1.0

                    state["angle"] += (
                        self.orbit_speed
                        * 60.0
                        * dt
                    )

            else:

                state["progress"] -= self.retract_speed

                if state["progress"] <= 0.0:
                    remove.append(name)

        for name in remove:
            del self.states[name]

    # =========================================================
    # MATH
    # =========================================================

    @staticmethod
    def _smoothstep(value):

        value = max(0.0, min(1.0, value))

        return (
            value
            * value
            * (3.0 - 2.0 * value)
        )

    def _orbit_point(self, cx, cy, angle):

        # Slight breathing makes the orbit feel alive instead
        # of behaving like a rigid mathematical ellipse.
        breathing = (
            math.sin(
                self.time * 1.7
            ) * 5.0
        )

        rx = self.orbit_rx + breathing
        ry = self.orbit_ry + breathing * 0.35

        return QPointF(
            cx + math.cos(angle) * rx,
            cy + math.sin(angle) * ry,
        )

    def _launch_point(self, cx, cy, side, panel):

        x = (
            cx
            + side
            * (
                self.orbit_rx
                + panel.width * 0.80
            )
        )

        y = cy + 20.0

        return QPointF(x, y)

    def _position(self, cx, cy, state):

        panel = state["panel"]
        progress = self._smoothstep(
            state["progress"]
        )

        orbit = self._orbit_point(
            cx,
            cy,
            state["angle"]
        )

        launch = self._launch_point(
            cx,
            cy,
            state["side"],
            panel
        )

        if state["active"]:

            point = QPointF(
                launch.x()
                + (
                    orbit.x()
                    - launch.x()
                )
                * progress,

                launch.y()
                + (
                    orbit.y()
                    - launch.y()
                )
                * progress,
            )

        else:

            # Retract follows the reverse launch vector.
            point = QPointF(
                launch.x()
                + (
                    orbit.x()
                    - launch.x()
                )
                * progress,

                launch.y()
                + (
                    orbit.y()
                    - launch.y()
                )
                * progress,
            )

        depth = (
            math.sin(
                state["angle"]
            ) + 1.0
        ) * 0.5

        scale = (
            0.82
            + depth * 0.18
        )

        alpha = int(
            105
            + depth * 105
        )

        return point, scale, alpha, depth

    # =========================================================
    # ORBIT HUD
    # =========================================================

    def draw_orbit(self, painter, cx, cy):

        painter.save()

        # Outer soft orbital traces.
        for factor, alpha, width in (
            (1.00, 70, 2),
            (0.88, 42, 1),
            (0.72, 28, 1),
        ):

            rect = QRectF(
                cx - self.orbit_rx * factor,
                cy - self.orbit_ry * factor,
                self.orbit_rx * 2.0 * factor,
                self.orbit_ry * 2.0 * factor,
            )

            painter.setBrush(Qt.NoBrush)
            painter.setPen(
                QPen(
                    QColor(
                        0,
                        225,
                        255,
                        alpha
                    ),
                    width
                )
            )

            painter.drawEllipse(rect)

        # Moving orbital ticks.
        for i in range(24):

            angle = (
                self.time * 0.45
                + i * math.tau / 24.0
            )

            inner = self._orbit_point(
                cx,
                cy,
                angle
            )

            outer_angle = angle + 0.018

            outer = QPointF(
                cx
                + math.cos(outer_angle)
                * (self.orbit_rx + 7.0),

                cy
                + math.sin(outer_angle)
                * (self.orbit_ry + 7.0),
            )

            painter.setPen(
                QPen(
                    QColor(
                        100,
                        245,
                        255,
                        115
                    ),
                    1
                )
            )

            painter.drawLine(
                inner,
                outer
            )

        painter.restore()

    # =========================================================
    # MODULES
    # =========================================================

    def draw_modules(self, painter, cx, cy):

        visible = []

        for name, state in self.states.items():

            if state["progress"] <= 0.001:
                continue

            point, scale, alpha, depth = (
                self._position(
                    cx,
                    cy,
                    state
                )
            )

            visible.append(
                (
                    depth,
                    name,
                    state,
                    point,
                    scale,
                    alpha
                )
            )

        # Back modules first, front modules last.
        visible.sort(
            key=lambda item: item[0]
        )

        for (
            depth,
            name,
            state,
            point,
            scale,
            alpha
        ) in visible:

            panel = state["panel"]

            screen_x = int(
                point.x()
                - panel.width * scale / 2.0
            )

            screen_y = int(
                point.y()
                - panel.height * scale / 2.0
            )

            panel.setPosition(
                screen_x,
                screen_y
            )

            old_alpha = panel.alpha
            old_x = panel.x
            old_y = panel.y

            panel.alpha = int(
                old_alpha
                * (
                    alpha / 210.0
                )
            )

            painter.save()

            painter.translate(
                point.x(),
                point.y()
            )

            painter.scale(
                scale,
                scale
            )

            panel.x = -panel.width / 2.0
            panel.y = -panel.height / 2.0

            panel.paint(
                painter
            )

            painter.restore()

            panel.x = screen_x
            panel.y = screen_y
            panel.alpha = old_alpha

    # =========================================================
    # HIT TEST
    # =========================================================

    def hit_test(self, x, y):

        candidates = []

        for name, state in self.states.items():

            if state["progress"] <= 0.55:
                continue

            panel = state["panel"]

            if panel.contains(
                x,
                y
            ):
                candidates.append(
                    (
                        state["angle"],
                        panel
                    )
                )

        if not candidates:
            return None

        candidates.sort(
            key=lambda item: math.sin(
                item[0]
            ),
            reverse=True
        )

        return candidates[0][1]
