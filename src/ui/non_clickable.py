from .ui_constant import FONT_NOTI, GAP_NOTI, FONT_DEFAULT, SIZE_MENU
from .ui_element import UiElement, add_gap
from src.utils.colors import YELLOW, BLACK
from typing import Any
import pygame as pg


class Overlay(UiElement):
    def __init__(self,
                 pos: tuple[int, int],
                 align: str = "center",
                 size: tuple[int, int] = SIZE_MENU,
                 color: tuple[int, int, int] = BLACK):
        self.size: tuple[int, int] = size
        self.color: tuple[int, int, int] = color
        self.surface: pg.Surface = pg.Surface(size)
        self.rect: pg.Rect = self.surface.get_rect(**{align: pos})
        self.surface.fill(self.color)

    def draw(self, screen: pg.Surface, color: Any = YELLOW) -> None:
        screen.blit(self.surface, self.rect)
        pg.draw.rect(screen, color, self.rect, 5)


class Text(UiElement):
    def __init__(self, text: str,  pos: tuple[int, int],
                 font: pg.font.Font = FONT_DEFAULT,
                 align: str = "center",
                 gap: tuple[int, int] | None = (0, 50),
                 color: tuple[int, int, int] = YELLOW):
        self.font: pg.Font = font
        self.surface: pg.Surface = font.render(text, True, color)
        if gap is not None:
            pos = add_gap(pos, gap)
        self.rect: pg.Rect = self.surface.get_rect(**{align: pos})

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Noti(UiElement):
    def __init__(self, text: str, pos: tuple[int, int],
                 align: str = "center",
                 gap: tuple[int, int] | None = GAP_NOTI):
        lines = text.split("\n")
        x, y = FONT_NOTI.size(lines[0])
        self.surface: pg.Surface = pg.Surface(
                (x + 20, y * len(lines)), pg.SRCALPHA)
        pg.draw.rect(self.surface, (40, 40, 40, 220),
                     self.surface.get_rect())
        if gap is not None:
            pos = add_gap(pos, gap)
        self.text: pg.Surface = FONT_NOTI.render(text, True, (255, 255, 255))
        self.surface.blit(self.text)
        self.rect: pg.Rect = self.surface.get_rect()
        setattr(self.rect, align, pos)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)
