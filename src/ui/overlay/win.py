from ..ui_constant import FONT_TITLE, GAP_BIG, GAP_DEFAULT
from src.utils.colors import LIGHT_GRAY, RED, PINK, BLACK
from ..clickable import Button, InputBox
from ..non_clickable import Text
from src.utils import GameObject
from src.game import game
from typing import Any
import pygame as pg
import sys


class Win(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        title: Text = Text("YOU WIN!", area.center,
                           FONT_TITLE, gap=(0, -100), color=PINK)
        score: Text = Text(f"{game.score.current}", title.rect.midtop,
                           FONT_TITLE, "midbottom", gap=(0, -50), color=RED)
        self.input_box: InputBox = InputBox("Click to enter your name here",
                                            title.rect.midbottom, "midtop",
                                            color=LIGHT_GRAY)
        bu2: Button = Button("Continue", title.rect.midbottom,
                             "midtop", GAP_BIG, on_click=self.continue_game)
        bu: Button = Button("Back to menu", bu2.rect.midbottom,
                            "midtop", GAP_DEFAULT, self.back_to_menu)
        self.buttons: list[Button] = [bu, bu2]
        self.elements: list[Any] = [bu, bu2, title, self.input_box, score]

    def continue_game(self) -> None:
        assert game is not None
        game.remove_from_tree(self)
        game.is_paused = False
        # start new level

    def back_to_menu(self) -> None:
        assert game is not None
        from ..screens.menu import Menu
        game.remove_from_tree(self)
        game.add_to_tree(Menu())

    def process(self) -> None:
        assert game is not None
        game.display.fill(BLACK)
        for element in self.elements:
            element.draw(game.display)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            for bu in self.buttons:
                bu.handle_event(event)
            self.input_box.handle_event(event)
