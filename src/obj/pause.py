import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui.ui_constant import GAP_DEFAULT, GAP_BIG
from src.ui import Button, add_gap, Overlay
from typing import Callable


class Pause(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        self.bg: Overlay = Overlay(add_gap(area.center, GAP_BIG))
        defs: list[tuple[str, Callable[[], None]]] = [
            ("Continue", self.continue_game),
            ("Cheat mode", self.cheat),
            ("Menu", self.back_to_menu)
        ]
        self.buttons: list[Button] = []
        x, y = add_gap(area.center, (0, 30))
        for label, method in defs:
            bu = Button(label, (x, y), "midbottom", on_click=method)
            self.buttons.append(bu)
            x, y = add_gap(bu.rect.midbottom, GAP_DEFAULT)

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def cheat(self) -> None:
        assert game is not None
        game.cheat = True
        from src.obj.cheat_option import CheatOption
        game.add_to_tree(CheatOption())
        game.remove_from_tree(self)

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
        from src.obj.menu import Menu
        game.add_to_tree(Menu())

    def process(self) -> None:
        assert game is not None
        self.bg.draw(game.display)
        for bu in self.buttons:
            bu.draw(game.display)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            for bu in self.buttons:
                bu.handle_event(event)
