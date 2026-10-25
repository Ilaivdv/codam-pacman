from ..ui_constant import GAP_DEFAULT, GAP_BIG
from ..non_clickable import Overlay
from src.utils import GameObject
from ..ui_element import add_gap
from ..clickable import Button
from typing import Callable
from src.game import game
import pygame as pg
import sys


class Pause(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        self.bg: Overlay = Overlay(add_gap(area.center, GAP_BIG))
        defs: list[tuple[str, Callable[[], None]]] = [
            ("Continue", self.continue_game),
            ("Cheats", self.cheat),
            ("Menu", self.back_to_menu)
        ]
        self.buttons: list[Button] = []
        x, y = add_gap(area.center, (0, 30))
        for label, method in defs:
            bu = Button(label, (x, y), "midbottom", on_click=method)
            x, y = add_gap(bu.rect.midbottom, GAP_DEFAULT)
            self.buttons.append(bu)

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def cheat(self) -> None:
        assert game is not None
        game.cheat = True
        from .cheat_option import CheatOption
        game.add_to_tree(CheatOption(), False)
        game.remove_from_tree(self)

    def continue_game(self) -> None:
        assert game is not None
        game.is_paused = False
        game.remove_from_tree(self)

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
        for bu in self.buttons:
            bu.draw(game.display)

    def handle_event(self, event: pg.event.Event) -> None:
        for bu in self.buttons:
            bu.handle_event(event)
