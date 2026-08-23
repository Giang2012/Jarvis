from abc import ABC, abstractmethod


class BaseSkill(ABC):

    name = ""

    @abstractmethod
    def execute(self, text: str):

        pass