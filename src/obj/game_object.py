from abc import ABC, abstractmethod

class GameObject(ABC):
    @abstractmethod
    def process(self) -> None:
        ...
