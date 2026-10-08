from abc import ABC, abstractmethod
from pydantic import BaseModel


class GameObject(BaseModel, ABC):
    @abstractmethod
    def process(self) -> None:
        ...
