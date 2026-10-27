from abc import ABC, abstractmethod
import pygame as pg


class UiElement(ABC):
    """
    A UIElement abstract class about all the ui elements that used.

    Attributes:
        rect (pg.Rect): pos and size info about the element.
    """

    rect: pg.Rect

    @abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        """
        Draw the element on the surface.

        Args:
            screen (pg.Surface): surface to draw on.
        """

        ...


def add_gap(pos: tuple[int, int], gap: tuple[int, int]) -> tuple[int, int]:
    """
    Add a gap to the current pos.

    Returns:
        tuple[int, int]: new pos
    """

    return (pos[0] + gap[0], pos[1] + gap[1])
