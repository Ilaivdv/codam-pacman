import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui import Button, Image
from src.utils.colors import DARK_GRAY
from typing import Callable, Any

BUTTON_SZ = (140, 50)
BUTTON_GAP = 50


class Menu(GameObject):
    def __init__(self) -> None:
        assert game is not None
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
        y: int = area.centery
        for label, method in defs:
            bu = Button(label, (area.centerx, y), "midtop", method)
            self.buttons.append(bu)
            self.elements.append(bu)
            y += bu.rect.height + BUTTON_GAP

    def start_game(self) -> None:
        ...

    def quit_game(self) -> None:
        pg.quit()
        sys.exit()

    def show_rank(self) -> None:
        ...

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
