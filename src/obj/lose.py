import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui import Button, Text, InputBox
from src.ui.color import DARK, WHITE
from typing import Any
from src.config import Config

TEXT_GAP = 50
FONT_TITLE = pg.font.SysFont("Arial", 80)
FONT_DEFAULT = pg.font.SysFont("Arial", 40)

def get_lower_pos(button: Button) -> tuple[int, int]:
    """return the lower pos
    """
    x, y = button.pos
    height = button.rect.height
    y += height + TEXT_GAP
    return (x, y)
    


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
                           (area.centerx, y - font_height - TEXT_GAP),
                           FONT_TITLE, color=WHITE)
        # hint: Text = Text("Enter your name",
        #                   (area.centerx, y - font_height))
        # _, font_height2 = FONT_DEFAULT.size("Click to enter your name")
        self.input_box: InputBox = InputBox((area.centerx, y - font_height), text="Click to enter your name")
        self.buttons: list[Button] = [bu]
        self.elements: list[Any] = [bu, title, self.input_box]

        

    def back_to_menu(self) -> None:
        ...

    def process(self) -> None:
        assert game is not None
        game.display.fill(DARK)
        for element in self.elements:
            element.draw(game.display)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            for bu in self.buttons:
                bu.handle_event(event)
            self.input_box.handle_event(event)
