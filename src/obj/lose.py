import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui import Button, Text, InputBox
from src.utils.colors import DARK_GRAY, YELLOW
from typing import Any

TEXT_GAP = 50
FONT_TITLE = pg.font.SysFont("Arial", 80)
FONT_DEFAULT = pg.font.SysFont("Arial", 40)


class Lose(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        bx, by = area.bottomright
        bu: Button = Button("Back to menu", (bx - 100, by - 100),
                            "bottomright", self.back_to_menu)
        y: int = area.centery
        _, font_height = FONT_TITLE.size("GAME OVER")
        title: Text = Text("GAME OVER",
                           (area.centerx, y),
                           FONT_TITLE, color=YELLOW)
        self.input_box: InputBox = InputBox((area.centerx, y + font_height),
                                            "Click to enter your name here")
        self.buttons: list[Button] = [bu]
        self.elements: list[Any] = [bu, title, self.input_box]

    def back_to_menu(self) -> None:
        ...

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
