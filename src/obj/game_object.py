from abc import ABC, abstractmethod
from typing import Any


class GameObject(ABC):
    def __init__(self, game: Any) -> None:
        self.game = game

    @abstractmethod
    def process(self) -> None:
        ...
