from abc import ABC, abstractmethod
import pygame as pg


class GameObject(ABC):
    @abstractmethod
    def process(self) -> None:
        ...

    @abstractmethod
    def handle_events(self, event: pg.event.Event) -> None:
        ...
