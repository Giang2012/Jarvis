from kernel.state import JarvisState
from kernel.event_bus import EventBus


class Kernel:

    def __init__(self):

        self.state = JarvisState()

        self.events = EventBus()


kernel = Kernel()