from src.utils.colors import YELLOW, DARK_GRAY, LIGHT_GRAY, GRAY, BLACK
import pygame as pg
from typing import Callable, Any
from .uiconstant import (FONT_NOTI, GAP_NOTI,
                         FONT_DEFAULT, FONT_RANK,
                         SIZE_MENU)


def add_gap(pos: tuple[int, int], gap: tuple[int, int]) -> tuple[int, int]:
    """Add a gap to the refer pos

    Returns:
        tuple[int, int]: new pos
    """
    return (pos[0] + gap[0], pos[1] + gap[1])


class Overlay:
    def __init__(self,
                 pos: tuple[int, int],
                 align: str = "center",
                 size: tuple[int, int] = SIZE_MENU,
                 color: tuple[int, int, int] = BLACK):
        self.size = size
        self.color = color
        self.surface = pg.Surface(size)
        self.rect = self.surface.get_rect(**{align: pos})
        self.surface.fill(self.color)

    def draw(self, screen: pg.Surface, color: Any = YELLOW) -> None:
        screen.blit(self.surface, self.rect)
        pg.draw.rect(screen, color, self.rect, 5)


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


class Noti:
    def __init__(self, text: str, pos: tuple[int, int],
                 align: str = "center",
                 gap: tuple[int, int] | None = GAP_NOTI):
        lines = text.split("\n")
        x, y = FONT_NOTI.size(lines[0])
        self.surface = pg.Surface((x + 20, y * len(lines)), pg.SRCALPHA)
        pg.draw.rect(self.surface, (40, 40, 40, 220),
                     self.surface.get_rect())
        if gap is not None:
            pos = add_gap(pos, gap)
        self.text = FONT_NOTI.render(text, True, (255, 255, 255))
        self.surface.blit(self.text)
        self.rect = self.surface.get_rect()
        setattr(self.rect, align, pos)

    def draw(self) -> None:
        from src.game import game
        assert game is not None
        game.display.blit(self.surface, self.rect)


class Button:
    def __init__(self, text: str, pos: tuple[int, int],
                 align: str = "center",
                 gap: tuple[int, int] | None = (0, 50),
                 on_click: Callable[[], None] | None = None,
                 font: pg.font.Font | None = FONT_DEFAULT):
        self.color = DARK_GRAY
        if not font:
            font = FONT_DEFAULT
        size = font.size(text)
        self.rect = pg.Rect((0, 0), size)
        if gap is not None:
            pos = add_gap(pos, gap)
        setattr(self.rect, align, pos)
        self.text = Text(text, self.rect.center, font=font, gap=(0, 3))
        self.on_click = on_click

    def draw(self, screen: pg.Surface) -> None:
        hovered = self.rect.collidepoint(pg.mouse.get_pos())
        outter = self.rect.inflate(20, 15)
        pg.draw.rect(screen, GRAY if hovered else BLACK, outter)
        # pg.draw.line(screen, YELLOW if hovered else BLACK, outter.bottomleft,
        #              outter.bottomright, 5)
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
                 pos: tuple[int, int], align: str = "center",
                 on_click: Callable[[], None] | None = None):
        self.surface = pg.image.load(path).convert_alpha()
        if size is not None:
            self.surface = pg.transform.scale(self.surface, size)
        self.rect = self.surface.get_rect(**{align: pos})
        self.on_click = on_click

    def draw(self, screen: pg.Surface) -> None:
        hovered = self.rect.collidepoint(pg.mouse.get_pos())
        pg.draw.rect(screen, LIGHT_GRAY if hovered else DARK_GRAY, self.rect)
        screen.blit(self.surface, self.rect)

    def handle_event(self, event: pg.event.Event) -> None:
        if (
                event.type == pg.MOUSEBUTTONDOWN
                and event.button == 1 and
                self.rect.collidepoint(event.pos) and self.on_click
                ):
            self.on_click()


class InputBox:
    def __init__(self, text: str, pos: tuple[int, int], align: str = "center",
                 gap: tuple[int, int] | None = (0, 50),
                 color: tuple[int, int, int] = GRAY):
        self.color = color
        self.text = text
        self.text_surface = FONT_RANK.render(text, True, color)
        self.rect = pg.Rect((0, 0), (800, 50))
        if gap is not None:
            pos = add_gap(pos, (-100, 50))
        setattr(self.rect, align, pos)
        self.active = False
        self.button = Button("Enter", self.rect.midright,
                             "midleft", gap=(10, 0), on_click=self.name_check)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.text_surface, self.rect)
        self.button.draw(screen)
        pg.draw.rect(screen, self.color, self.rect, 2)

    def create_new_score(self) -> None:
        from src.game import game
        assert game is not None
        game._score.set_username(self.text)
        game._score.update_rank()
        game._score.update_file()

    def name_check(self) -> None:
        result: bool = (self.text != " "
                        and all(c.isalpha() or c.isspace() for c in self.text))
        if result is True:
            if not self.text:
                self.text = "Please enter at least 1 character"
            if len(self.text) > 10:
                self.text = "Please enter a shorter name"
            else:
                self.create_new_score()
                self.text = "Your record has been saved!"
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
            self.text_surface = FONT_RANK.render(self.text,
                                                 True, self.color)
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.name_check()
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.text_surface = FONT_RANK.render(self.text,
                                                     True, self.color)
