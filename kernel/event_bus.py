from collections import defaultdict


class EventBus:

    def __init__(self):

        self.events = defaultdict(list)

    def subscribe(self, event, callback):

        self.events[event].append(callback)

    def unsubscribe(self, event, callback):

        if callback in self.events[event]:

            self.events[event].remove(callback)

    def clear(self):

        self.events.clear()

    def emit(self, event, *args, **kwargs):

        if event not in self.events:
            return

        for callback in self.events[event]:

            callback(*args, **kwargs)