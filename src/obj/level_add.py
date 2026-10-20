import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui.uielement import Text, add_gap, Image, CheckBox
from src.ui.uiconstant import GAP_LIFE, GAP_SCORE, SIZE_LIFE
from src.utils.colors import DARK_GRAY
from typing import Any


class Level_add(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        path: str = "assets/pacgum.png"
        life: Image = Image(path, SIZE_LIFE, add_gap(area.midtop, GAP_LIFE),
                            "midtop")
        self.elements: list[Any] = [life]
        for _ in range(game._life - 1):
            life = Image(path, SIZE_LIFE, add_gap(life.rect.midright, (20, 0)),
                         "midleft")
            self.elements.append(life)
        score: Text = Text(f"{game._score.current}", add_gap(area.midtop,
                                                             GAP_SCORE),
                           align="midleft")
        self.elements.append(score)
        x, _ = add_gap(area.midtop, GAP_LIFE)
        _, y = area.midbottom
        self.checkb = CheckBox("Cheat Mode", (x, y - 100), "midbottom",
                               gap=None)
        self.elements.append(self.checkb)

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def process(self) -> None:
        assert game is not None
        game.display.fill(DARK_GRAY)
        for element in self.elements:
            element.draw(game.display)
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.checkb.handle_event(event)
