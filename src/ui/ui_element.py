from abc import ABC, abstractmethod
import pygame as pg


class UiElement(ABC):
    rect: pg.Rect

    @abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        ...


def add_gap(pos: tuple[int, int], gap: tuple[int, int]) -> tuple[int, int]:
    """Add a gap to the refer pos

    Returns:
        tuple[int, int]: new pos
    """
    return (pos[0] + gap[0], pos[1] + gap[1])
