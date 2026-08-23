from abc import ABC, abstractmethod


class Plugin(ABC):

    name = ""

    version = "1.0"

    author = ""

    @abstractmethod
    def on_load(self):
        pass

    @abstractmethod
    def on_unload(self):
        pass