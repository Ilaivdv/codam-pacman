from .color import WHITE, DARK, LIGHT
import pygame as pg
from typing import Callable

FONT_DEFAULT = pg.font.SysFont("Arial", 40)


class Text:
    def __init__(self, text: str,  pos: tuple[int, int],
                 font: pg.font.Font = FONT_DEFAULT,
                 align: str = "center",
                 color: tuple[int, int, int] = WHITE):
        self.font = font
        self.surface = font.render(text, True, color)
        self.rect = self.surface.get_rect(**{align: pos})

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Button:
    def __init__(self, text: str, pos: tuple[int, int], align: str = "center",
                 on_click: Callable[[], None] | None = None):
        self.color = DARK
        self.rect = pg.Rect((0, 0), FONT_DEFAULT.size(text))
        setattr(self.rect, align, pos)
        self.text = Text(text, self.rect.center)
        self.on_click = on_click

    def draw(self, screen: pg.Surface) -> None:
        hovered = self.rect.collidepoint(pg.mouse.get_pos())
        pg.draw.rect(screen, LIGHT if hovered else DARK, self.rect)
        self.text.draw(screen)

    def handle_event(self, event: pg.event.Event) -> None:
        if (
                event.type == pg.MOUSEBUTTONDOWN
                and event.button == 1 and
                self.rect.collidepoint(event.pos) and self.on_click
                ):
            self.on_click()


class Image:
    def __init__(self, path: str, size: tuple[int, int] | None,
                 pos: tuple[int, int], align: str = "center"):
        self.surface = pg.image.load(path).convert_alpha()
        if size is not None:
            self.surface = pg.transform.smoothscale(self.surface, size)
        self.rect = self.surface.get_rect(**{align: pos})

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)
