from src.utils.colors import BLUE, LIGHT_GRAY
from ..clickable import Button, CheckBox
from ..non_clickable import Overlay
from ..ui_constant import GAP_BIG
from ..ui_element import add_gap
from src.utils import GameObject
from src.game import game
from typing import Any
import pygame as pg
import sys


class CheatOption(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        self.bg: Overlay = Overlay(add_gap(area.center, GAP_BIG),
                                   size=(500, 500))
        bu_continue: Button = Button("Continue",
                                     add_gap(self.bg.rect.midbottom,
                                             (0, -200)),
                                     "midtop", on_click=self.continue_game,
                                     color_bu=LIGHT_GRAY)
        back_continue: Button = Button("Menu", bu_continue.rect.midbottom,
                                       "midtop", on_click=self.back_to_menu,
                                       color_bu=LIGHT_GRAY)
        defs: list[str] = [x for x in game.cheat_options.keys()]
        self.elements: list[Any] = [bu_continue, back_continue]
        x, y = add_gap(self.bg.rect.topleft, (100, 70))
        for text in defs:
            checkb = CheckBox(text, (x, y), "topleft", gap=None, color=BLUE)
            self.elements.append(checkb)
            _, y = add_gap(checkb.rect.midbottom, (0, 50))

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def continue_game(self) -> None:
        assert game is not None
        game.remove_from_tree(self)
        game.is_paused = False

    def quit_game(self) -> None:
        pg.quit()
        sys.exit()

    def back_to_menu(self) -> None:
        assert game is not None
        game.remove_from_tree(self)
        from ..screens.menu import Menu
        game.add_to_tree(Menu())

    def process(self) -> None:
        assert game is not None
        self.bg.draw(game.display)
        for bu in self.elements:
            bu.draw(game.display)

    def handle_event(self, event: pg.event.Event) -> None:
        for bu in self.elements:
            bu.handle_event(event)
