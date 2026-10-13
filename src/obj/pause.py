import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui import Button
from src.utils.colors import DARK_GRAY
from typing import Callable

BUTTON_GAP = 50


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
        y: int = area.centery
        for label, method in defs:
            bu = Button(label, (area.centerx, y), "center", method)
            self.buttons.append(bu)
            y += bu.rect.height + BUTTON_GAP

    def continue_game(self) -> None:
        ...

    def quit_game(self) -> None:
        pg.quit()
        sys.exit()

    def show_rank(self) -> None:
        ...

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
