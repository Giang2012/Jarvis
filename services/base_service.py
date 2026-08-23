from abc import ABC, abstractmethod


class BaseService(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass