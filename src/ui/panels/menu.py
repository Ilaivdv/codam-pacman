import pygame as pg
from src.game import game, settings
import sys
from src.utils import GameObject
from src.ui import Button, Image, add_gap, Overlay
from src.ui.ui_constant import GAP_DEFAULT, GAP_BIG
from src.utils.colors import DARK_GRAY
from typing import Callable, Any


class Menu(GameObject):
    def __init__(self) -> None:
        assert game is not None
        assert settings is not None
        area = game.display.get_rect()
        bg: Overlay = Overlay(add_gap(area.center, GAP_BIG), size=(600, 600))
        path = "assets/pacman-outfit-0.jpg"
        start_im = Image(path, None, area.midtop, "midtop")
        defs: list[tuple[str, Callable[[], None]]] = [
            ("Play", self.start_game),
            ("Rank", self.show_rank),
            ("How to play", self.instructions),
            ("Cheat", self.cheat),
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
        from src.obj.instruction import Instruction
        game.add_to_tree(Instruction())
        game.remove_from_tree(self)

    def cheat(self) -> None:
        assert game is not None
        game.cheat = True
        self.start_game()

    def start_game(self) -> None:
        assert game is not None
        from src.level.level import Level
        from src.level.level_overlay import LevelOverlay
        level: Level = Level()
        game.add_to_tree(LevelOverlay())
        game.add_to_tree(level)
        game.remove_from_tree(self)

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
        for element in self.elements:
            element.draw(game.display)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
            for bu in self.buttons:
                bu.handle_event(event)
