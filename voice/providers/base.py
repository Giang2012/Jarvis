from abc import ABC, abstractmethod

class TTSProvider(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        pass
