from ..ui_constant import GAP_DEFAULT, FONT_TITLE, FONT_AUTHOR
from ..clickable import Button, Image
from src.utils.colors import DARK_GRAY, YELLOW, LIGHT_GRAY, BLACK
from ..non_clickable import Overlay, Text
from src.game import game, settings
from ..ui_element import add_gap
from typing import Callable, Any
from src.utils import GameObject
import pygame as pg
import sys


class Menu(GameObject):
    """
    A Menu screen showing start page of game.
    """

    def __init__(self) -> None:
        assert game is not None and settings is not None

        area = game.display.get_rect()
        bg: Overlay = Overlay(add_gap(area.center, (0, 120)), size=(600, 500))
        path = "assets/player.png"
        logo: Text = Text("Pac-Man", area.center, FONT_TITLE, gap=(0, -500),
                          color=YELLOW)
        logo2: Text = Text("Pac-Man", add_gap(logo.rect.center, (15, 15)),
                           FONT_TITLE, gap=None,
                           color=BLACK)
        start_im: Image = Image(path, (2000, 120),
                                add_gap(logo.rect.midbottom, (45, -20)),
                                "midtop")
        our_name: Text = Text("made by ilai & yawen",
                              add_gap(logo.rect.midbottom, (0, 120)),
                              FONT_AUTHOR, color=LIGHT_GRAY)
        defs: list[tuple[str, Callable[[], None]]] = [
            ("Play", self.start_game),
            ("Rank", self.show_rank),
            ("How to play", self.instructions),
            ("Quit", self.quit_game)
        ]
        self.elements: list[Any] = [start_im, bg, logo2, logo, our_name]
        self.buttons: list[Button] = []
        x, y = add_gap(area.center, (0, -50))
        for label, method in defs:
            bu = Button(label, (x, y), "midbottom", on_click=method)
            self.buttons.append(bu)
            self.elements.append(bu)
            x, y = add_gap(bu.rect.midbottom, GAP_DEFAULT)

    def instructions(self) -> None:
        """ Displays intruction overlay. """

        assert game is not None
        from ..overlay.instruction import Instruction
        game.add_to_tree(Instruction(), False)
        game.remove_from_tree(self)

    def start_game(self) -> None:
        """ Starts the new game(always). """

        assert game is not None
        from src.level import LevelManager
        if game.is_paused:
            game.is_paused = False
        game.current_level = 0
        game.remove_from_tree(self)
        game.add_to_tree(LevelManager())

    def quit_game(self) -> None:
        pg.quit()
        sys.exit()

    def show_rank(self) -> None:
        """ Displays the rank screen. """

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
