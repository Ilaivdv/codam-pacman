from src.utils.colors import YELLOW, DARK_GRAY, LIGHT_GRAY, GRAY
import pygame as pg
from typing import Callable

GAP_DEFAULT = (0, 50)
GAP_MID = (0, 100)
FONT_DEFAULT = pg.font.SysFont("Arial", 40)
FONT_TITLE = pg.font.SysFont("Arial", 80)
GAP_BIG = (0, 150)


def add_gap(pos: tuple[int, int], gap: tuple[int, int]) -> tuple[int, int]:
    """Add a gap to the refer pos

    Returns:
        tuple[int, int]: new pos
    """
    return (pos[0] + gap[0], pos[1] + gap[1])


class Text:
    def __init__(self, text: str,  pos: tuple[int, int],
                 font: pg.font.Font = FONT_DEFAULT,
                 align: str = "center",
                 gap: tuple[int, int] | None = (0, 50),
                 color: tuple[int, int, int] = YELLOW):
        self.font = font
        self.surface = font.render(text, True, color)
        if gap is not None:
            pos = add_gap(pos, gap)
        self.rect = self.surface.get_rect(**{align: pos})

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.surface, self.rect)


class Button:
    def __init__(self, text: str, pos: tuple[int, int], align: str = "center",
                 gap: tuple[int, int] | None = (0, 50),
                 on_click: Callable[[], None] | None = None):
        self.color = DARK_GRAY
        self.rect = pg.Rect((0, 0), FONT_DEFAULT.size(text))
        if gap is not None:
            pos = add_gap(pos, gap)
        setattr(self.rect, align, pos)
        self.text = Text(text, self.rect.center, gap=None)
        self.on_click = on_click

    def draw(self, screen: pg.Surface) -> None:
        hovered = self.rect.collidepoint(pg.mouse.get_pos())
        pg.draw.rect(screen, LIGHT_GRAY if hovered else DARK_GRAY, self.rect)
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


class InputBox:
    def __init__(self, text: str, pos: tuple[int, int], align: str = "center",
                 gap: tuple[int, int] | None = (0, 50),
                 color: tuple[int, int, int] = GRAY):
        self.color = color
        self.text = text
        self.text_surface = FONT_DEFAULT.render(text, True, color)
        self.rect = pg.Rect((0, 0), (800, 50))
        if gap is not None:
            pos = add_gap(pos, gap)
        setattr(self.rect, align, pos)
        self.active = False
        self.button = Button("Enter", self.rect.midright,
                             "midleft", None, self.name_check)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.text_surface, self.rect)
        self.button.draw(screen)
        pg.draw.rect(screen, self.color, self.rect, 2)

    def create_new_score(self) -> None:
        """[TO DO]store the name and the score.
        and output a local file at .local/share
        """
        ...

    def name_check(self) -> None:
        result: bool = (self.text != " "
                        and all(c.isalpha() or c.isspace() for c in self.text))
        if result is True:
            if len(self.text) > 10:
                self.text = "Please enter a shorter name"
            else:
                self.create_new_score()
                self.text = "Saved!"
        else:
            self.text = "Only alphanumeric and space are allowed!"
        self.active = False

    def handle_event(self, event: pg.event.Event) -> None:
        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
            if self.button.rect.collidepoint(event.pos):
                self.button.handle_event(event)
            elif self.rect.collidepoint(event.pos):
                self.active = True
                self.text = ""
            else:
                self.active = False
            self.text_surface = FONT_DEFAULT.render(self.text,
                                                    True, self.color)
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.name_check()
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.text_surface = FONT_DEFAULT.render(self.text,
                                                        True, self.color)
