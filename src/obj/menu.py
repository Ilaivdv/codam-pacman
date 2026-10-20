import pygame as pg
from src.game import game, settings
import sys
from src.obj import GameObject
from src.ui.uielement import Button, Image, add_gap
from src.ui import GAP_DEFAULT
from src.utils.colors import DARK_GRAY
from typing import Callable, Any


class Menu(GameObject):
    def __init__(self) -> None:
        assert game is not None
        assert settings is not None
        area = game.display.get_rect()
        path = "assets/pacman-outfit-0.jpg"
        start_im = Image(path, None, area.midtop, "midtop")
        defs: list[tuple[str, Callable[[], None]]] = [
            ("Play", self.start_game),
            ("Rank", self.show_rank),
            ("Quit", self.quit_game)
        ]
        self.elements: list[Any] = [start_im]
        self.buttons: list[Button] = []
        x, y = area.center
        for label, method in defs:
            bu = Button(label, (x, y), "midbottom", on_click=method)
            self.buttons.append(bu)
            self.elements.append(bu)
            x, y = add_gap(bu.rect.midbottom, GAP_DEFAULT)

    def start_game(self) -> None:
        assert game is not None
        game.remove_from_tree(self)
        from src.obj.level import Level
        from src.obj.level_add import Level_add
        game.add_to_tree(Level())
        game.add_to_tree(Level_add())

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
