import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui import Button, Text
from src.utils.colors import DARK_GRAY, YELLOW
from typing import Any
from src.config import Config

TEXT_GAP = 50
FONT_TITLE = pg.font.SysFont("Arial", 80)


class Rank(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        bx, by = area.bottomright
        bu: Button = Button("Back to menu", (bx - 100, by - 100),
                            "bottomright", self.back_to_menu)
        y: int = area.centery
        _, font_height = FONT_TITLE.size("Pac-Man")
        title: Text = Text("Pac-Man",
                           (area.centerx, y - font_height - TEXT_GAP),
                           FONT_TITLE, color=YELLOW)
        hint: Text = Text("press SPACE to play",
                          (area.centerx, y - font_height))
        self.buttons: list[Button] = [bu]
        self.elements: list[Any] = [bu, title, hint]
        highscore = Config().parse_highscore("highscore.json")
        for index, data in enumerate(highscore, 1):
            name, score = data
            text = Text(f"{index}.{name} - {score}pts", (area.centerx, y))
            self.elements.append(text)
            y += bu.rect.height + TEXT_GAP

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
