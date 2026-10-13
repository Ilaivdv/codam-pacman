import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui.uielement import (Button, Text, add_gap,
                              FONT_TITLE, GAP_BIG, GAP_DEFAULT)
from src.utils.colors import DARK_GRAY, YELLOW
from typing import Any
from src.config import Config


class Rank(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        title: Text = Text("Pac-Man", area.center, FONT_TITLE, gap=(0, -200),
                           color=YELLOW)
        hint: Text = Text("press SPACE to play", pos=title.rect.midbottom,
                          align="center")
        self.elements: list[Any] = [title, hint]
        x, y = add_gap(hint.rect.midbottom, GAP_DEFAULT)
        highscore = Config().parse_highscore("highscore.json")
        for index, data in enumerate(highscore, 1):
            name, score = data
            text = Text(f"{index}.{name} - {score}pts", (x, y))
            x, y = text.rect.midbottom
            self.elements.append(text)
        bu: Button = Button("Back to menu", (x, y),
                            "midbottom", GAP_BIG, self.back_to_menu)
        self.buttons: list[Button] = [bu]
        self.elements.append(bu)

    def back_to_menu(self) -> None:
        ...

    def play(self) -> None:
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
