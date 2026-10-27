from abc import ABC, abstractmethod
import pygame as pg


class GameObject(ABC):
    """
    Abstract GameObject class, has required methods for process tree to run.
    """

    @abstractmethod
    def process(self) -> None:
        """
        Object's process handler, decides what happens on each updated frame.
        """
        ...

    def handle_event(self, event: pg.event.Event) -> None:
        """ Handles pygame events for object (input, mouse movement, etc.). """
        pass

    def __str__(self) -> str:
        """ Returns parent class name. """
        return (self.__class__.__name__)
