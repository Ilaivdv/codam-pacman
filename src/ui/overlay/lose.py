from src.utils.colors import LIGHT_GRAY, BLUE, YELLOW, BLACK
from src.ui.ui_constant import FONT_TITLE, GAP_BIG
from ..clickable import Button, InputBox
from ..non_clickable import Text
from src.utils import GameObject
from src.game import game
from typing import Any
import pygame as pg


class Lose(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        title: Text = Text("GAME OVER", area.center,
                           FONT_TITLE, gap=(0, -100), color=BLUE)
        score: Text = Text(f"{game.score.current}", title.rect.midtop,
                           FONT_TITLE, "midbottom", gap=(0, -50), color=YELLOW)
        self.input_box: InputBox = InputBox("Click to enter your name here",
                                            title.rect.midbottom, "midtop",
                                            color=LIGHT_GRAY)
        bu: Button = Button("Back to menu", title.rect.midbottom,
                            "midtop", GAP_BIG, self.back_to_menu,
                            color_bu=LIGHT_GRAY)
        self.buttons: list[Button] = [bu]
        self.elements: list[Any] = [bu, title, self.input_box, score]

    def back_to_menu(self) -> None:
        assert game is not None
        from ..screens.menu import Menu
        game.reset_stats()
        game.remove_from_tree(self)
        game.add_to_tree(Menu(), False)

    def process(self) -> None:
        assert game is not None
        game.display.fill(BLACK)
        for element in self.elements:
            element.draw(game.display)

    def handle_event(self, event: pg.event.Event) -> None:
        for bu in self.buttons:
            bu.handle_event(event)
        self.input_box.handle_event(event)
