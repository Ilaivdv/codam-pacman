import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui import GAP_DEFAULT
from src.ui.uielement import Button, add_gap
from src.utils.colors import DARK_GRAY
from typing import Callable


class Pause(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        defs: list[tuple[str, Callable[[], None]]] = [
            ("Continue", self.continue_game),
            ("Rank", self.show_rank),
            ("Quit", self.quit_game)
        ]
        self.buttons: list[Button] = []
        x, y = area.center
        for label, method in defs:
            bu = Button(label, (x, y), "midbottom", on_click=method)
            self.buttons.append(bu)
            x, y = add_gap(bu.rect.midbottom, GAP_DEFAULT)

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def continue_game(self) -> None:
        assert game is not None
        game.remove_from_tree(self)
        from src.obj.level import Level
        from src.obj.level_add import Level_add
        game.add_to_tree(Level_add())
        game.add_to_tree(Level())

    def quit_game(self) -> None:
        pg.quit()
        sys.exit()

    def show_rank(self) -> None:
        assert game is not None
        game.remove_from_tree(self)
        from src.obj.rank import Rank
        game.add_to_tree(Rank())

    def process(self) -> None:
        assert game is not None
        game.display.fill(DARK_GRAY)
        for bu in self.buttons:
            bu.draw(game.display)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            for bu in self.buttons:
                bu.handle_event(event)
