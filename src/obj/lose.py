import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui.uielement import Button, Text, InputBox
from src.ui import FONT_TITLE, GAP_MID
from src.utils.colors import DARK_GRAY, YELLOW, LIGHT_GRAY
from typing import Any


class Lose(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        title: Text = Text("GAME OVER", area.center,
                           FONT_TITLE, gap=(0, -100), color=YELLOW)
        score: Text = Text(f"Score:{game._score.current}", title.rect.midtop,
                           FONT_TITLE, "midbottom", gap=(0, -50), color=YELLOW)
        self.input_box: InputBox = InputBox("Click to enter your name here",
                                            title.rect.midbottom, "midtop",
                                            color=LIGHT_GRAY)
        bu: Button = Button("Back to menu", self.input_box.rect.midbottom,
                            "midtop", GAP_MID, self.back_to_menu)
        self.buttons: list[Button] = [bu]
        self.elements: list[Any] = [bu, title, self.input_box, score]

    def back_to_menu(self) -> None:
        assert game is not None
        from src.obj.menu import Menu
        game.remove_from_tree(self)
        game.add_to_tree(Menu())

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def process(self) -> None:
        assert game is not None
        game.display.fill(DARK_GRAY)
        for element in self.elements:
            element.draw(game.display)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            for bu in self.buttons:
                bu.handle_event(event)
            self.input_box.handle_event(event)
