from gui.engine.event_bus import EventBus
from gui.actions.action_manager import ActionManager

class Engine:

    def __init__(self):

        self.bus = EventBus()
        self.actionManager = ActionManager()


engine = Engine()