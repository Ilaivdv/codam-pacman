from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def process(self) -> None:
        ...

    def __str__(self) -> str:
        return (self.__class__.__name__)
