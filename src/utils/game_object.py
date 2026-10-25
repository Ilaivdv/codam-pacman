from abc import ABC, abstractmethod
import pygame as pg


class GameObject(ABC):
    @abstractmethod
    def process(self) -> None:
        ...

    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def __str__(self) -> str:
        return (self.__class__.__name__)
