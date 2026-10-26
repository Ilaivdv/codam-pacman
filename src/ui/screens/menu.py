from ..ui_constant import GAP_DEFAULT, GAP_BIG
from ..clickable import Button, Image
from src.utils.colors import DARK_GRAY
from ..non_clickable import Overlay
from src.game import game, settings
from ..ui_element import add_gap
from typing import Callable, Any
from src.utils import GameObject
import pygame as pg
import sys


class Menu(GameObject):
    def __init__(self) -> None:
        assert game is not None and settings is not None

        area = game.display.get_rect()
        bg: Overlay = Overlay(add_gap(area.center, GAP_BIG), size=(600, 600))
        path = "assets/pacman-outfit-0.jpg"
        start_im = Image(path, None, area.midtop, "midtop")
        defs: list[tuple[str, Callable[[], None]]] = [
            ("Play", self.start_game),
            ("Rank", self.show_rank),
            ("How to play", self.instructions),
            ("Quit", self.quit_game)
        ]
        self.elements: list[Any] = [start_im, bg]
        self.buttons: list[Button] = []
        x, y = add_gap(area.center, (0, -50))
        for label, method in defs:
            bu = Button(label, (x, y), "midbottom", on_click=method)
            self.buttons.append(bu)
            self.elements.append(bu)
            x, y = add_gap(bu.rect.midbottom, GAP_DEFAULT)

    def instructions(self) -> None:
        assert game is not None
        from ..overlay.instruction import Instruction
        game.add_to_tree(Instruction())
        game.remove_from_tree(self)

    def cheat(self) -> None:
        assert game is not None
        game.cheat = True
        self.start_game()

    def start_game(self) -> None:
        assert game is not None
        game.remove_from_tree(self)

        from src.level import LevelManager
        game.add_to_tree(LevelManager())

    def quit_game(self) -> None:
        pg.quit()
        sys.exit()

    def show_rank(self) -> None:
        assert game is not None
        game.remove_from_tree(self)
        from .rank import Rank
        game.add_to_tree(Rank(), False)

    def process(self) -> None:
        assert game is not None
        game.display.fill(DARK_GRAY)
        for element in self.elements:
            element.draw(game.display)

    def handle_event(self, event: pg.event.Event) -> None:
        for bu in self.buttons:
            bu.handle_event(event)
