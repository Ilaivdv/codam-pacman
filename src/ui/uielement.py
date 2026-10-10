from .color import WHITE, DARK, LIGHT
import pygame as pg

font = pg.font.SysFont("Arial", 40)


class Text:
    def __init__(self, text: str, font: pg.font.Font, pos: tuple[int, int],
                 align: str = "center", color: tuple[int, int, int] = WHITE):
        font = font
        self.surface = font.render(text, True, color)
        self.rect = self.surface.get_rect(**{align: pos})

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Button:
    def __init__(self, text: str, size: tuple[int, int],
                 pos: tuple[int, int], align: str = "center"):
        self.rect = pg.Rect((0, 0), size)
        setattr(self.rect, align, pos)
        self.color = DARK
        self.text = Text(text, font, self.rect.center)

    def draw(self, screen: pg.Surface) -> None:
        hovered = self.rect.collidepoint(pg.mouse.get_pos())
        pg.draw.rect(screen, LIGHT if hovered else DARK, self.rect)
        self.text.draw(screen)


class Image():
    def __init__(self, path: str, size: tuple[int, int] | None,
                 pos: tuple[int, int], align: str = "center"):
        self.surface = pg.image.load(path).convert_alpha()
        if size is not None:
            self.surface = pg.transform.smoothscale(self.surface, size)
        self.rect = self.surface.get_rect(**{align: pos})

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)
