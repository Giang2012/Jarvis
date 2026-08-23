class EventBus:

    def __init__(self):

        self.listeners = {}

    # -----------------------

    def subscribe(self, eventName, callback):

        if eventName not in self.listeners:

            self.listeners[eventName] = []

        self.listeners[eventName].append(callback)

    # -----------------------

    def emit(self, event):

        if event.name not in self.listeners:

            return

        for callback in self.listeners[event.name]:

            callback(event)