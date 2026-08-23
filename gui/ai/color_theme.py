from PySide6.QtGui import QColor

from gui.ai.core_state import CoreState


class CoreColor:

    @staticmethod
    def color(state):

        if state == CoreState.IDLE:

            return QColor(0,255,255)

        if state == CoreState.LISTENING:

            return QColor(255,255,0)

        if state == CoreState.THINKING:

            return QColor(170,80,255)

        if state == CoreState.SPEAKING:

            return QColor(255,255,255)

        if state == CoreState.ERROR:

            return QColor(255,0,0)

        return QColor(80,80,80)