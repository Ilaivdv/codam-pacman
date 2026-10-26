from src.utils.colors import YELLOW, DARK_GRAY, LIGHT_GRAY, GRAY, BLACK
from .ui_constant import FONT_DEFAULT, FONT_RANK, SIZE_LIFE
from .ui_element import UiElement, add_gap
from .non_clickable import Text
from typing import Callable
import pygame as pg


class Clickable(UiElement):
    on_click: Callable[[], None] | None = None

    def handle_event(self, event: pg.event.Event) -> None:
        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and
                self.rect.collidepoint(event.pos) and self.on_click):
            self.on_click()

    def draw(self, screen: pg.Surface) -> None:
        ...


class Button(Clickable):
    def __init__(self, text: str, pos: tuple[int, int],
                 align: str = "center",
                 gap: tuple[int, int] | None = (0, 50),
                 on_click: Callable[[], None] | None = None,
                 color_bu: tuple[int, int, int] | None = YELLOW,
                 font: pg.font.Font | None = FONT_DEFAULT):
        self.color: tuple[int, int, int] = DARK_GRAY
        if not font:
            font = FONT_DEFAULT
        size = font.size(text)
        self.rect: pg.Rect = pg.Rect((0, 0), size)
        if gap is not None:
            pos = add_gap(pos, gap)
        setattr(self.rect, align, pos)
        if color_bu:
            self.text: Text = Text(text, self.rect.center,
                                   font=font, gap=(0, 3),
                                   color=color_bu)
        else:
            self.text = Text(text, self.rect.center,
                             font=font, gap=(0, 3))
        self.on_click = on_click

    def draw(self, screen: pg.Surface) -> None:
        hovered = self.rect.collidepoint(pg.mouse.get_pos())
        outer = self.rect.inflate(20, 15)
        pg.draw.rect(screen, GRAY if hovered else BLACK, outer)
        self.text.draw(screen)


class Image(Clickable):
    def __init__(self, path: str, size: tuple[int, int] | None,
                 pos: tuple[int, int], align: str = "center",
                 on_click: Callable[[], None] | None = None,
                 hover: bool = False):
        self.surface = pg.image.load(path).convert_alpha()
        if size is not None:
            self.surface = pg.transform.scale(self.surface, size)
        self.rect = self.surface.get_rect(**{align: pos})
        self.on_click = on_click
        self.hover = hover

    def draw(self, screen: pg.Surface) -> None:
        hovered = self.rect.collidepoint(pg.mouse.get_pos())
        if self.hover is False:
            pg.draw.rect(screen, DARK_GRAY, self.rect)
        else:
            pg.draw.rect(screen, LIGHT_GRAY if hovered else DARK_GRAY, self.rect)
        screen.blit(self.surface, self.rect)


class CheckBox(Clickable):
    def __init__(self, text: str, pos: tuple[int, int], align: str = "center",
                 gap: tuple[int, int] | None = (0, 50),
                 color: tuple[int, int, int] = YELLOW):
        self.text = text
        self.text_surface = FONT_RANK.render(text, True, color)
        self.rect = pg.Rect((0, 0), SIZE_LIFE)
        if gap is not None:
            pos = add_gap(pos, gap)
        setattr(self.rect, align, pos)
        self.checked = False
        self.color = color
        self.on_click = self.cheat_option

    def cheat_option(self) -> None:
        self.checked = not self.checked
        from src.game import game
        assert game is not None
        bool_option: bool = game.cheat_options[self.text]
        game.cheat_options[self.text] = not bool_option

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, self.color, self.rect, 3)
        pos: tuple[int, int] = add_gap(self.rect.midright, (10, 2))
        text_rect = self.text_surface.get_rect(midleft=pos)
        screen.blit(self.text_surface, text_rect)
        if self.checked:
            inner = self.rect.inflate(-10, -10)
            pg.draw.line(screen, self.color,
                         inner.topleft, inner.bottomright, 3)
            pg.draw.line(screen, self.color,
                         inner.topright, inner.bottomleft, 3)


class InputBox(UiElement):
    def __init__(self, text: str, pos: tuple[int, int], align: str = "center",
                 gap: tuple[int, int] | None = (0, 50),
                 color: tuple[int, int, int] = GRAY):
        self.color: tuple[int, int, int] = color
        self.text: str = text
        self.text_surface: pg.Surface = FONT_RANK.render(text, True, color)
        self.rect: pg.Rect = pg.Rect((0, 0), (800, 50))
        if gap is not None:
            pos = add_gap(pos, (-100, 50))
        setattr(self.rect, align, pos)
        self.active: bool = False
        self.button: Button = Button("Enter", self.rect.midright,
                                     "midleft", gap=(10, 0),
                                     on_click=self.name_check)

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.text_surface, self.rect)
        self.button.draw(screen)
        pg.draw.rect(screen, self.color, self.rect, 2)

    def create_new_score(self) -> None:
        from src.game import game
        assert game is not None
        game.score.set_username(self.text)
        game.score.update_rank()
        game.score.update_file()

    def name_check(self) -> None:
        name = self.text.strip()
        if not name:
            self.text = "Please enter at least 1 character"
        elif len(name) > 10:
            self.text = "Please enter a shorter name"
        elif all(c.isalpha() or c.isspace() for c in name) is False:
            self.text = "Only alphanumeric and space are allowed!"
        else:
            self.create_new_score()
            self.text = "Your record has been saved!"
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
