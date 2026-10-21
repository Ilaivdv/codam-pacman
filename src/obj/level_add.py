import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui.uielement import Text, add_gap, Image, CheckBox
from src.ui.uiconstant import GAP_LIFE, GAP_SCORE, SIZE_LIFE, SIZE_PAUSE
from typing import Any
from src.obj.level import Level


class Level_add(GameObject):
    def __init__(self, level: Level) -> None:
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
        pause: Image = Image("assets/pause.png", SIZE_PAUSE,
                             (score.rect.x, y - 100),
                             align="midbottom", on_click=self.pause)
        self.elements.append(self.checkb)
        self.elements.append(pause)
        self.reactions: list[Any] = [self.checkb, pause]
        self.level = level

    def pause(self) -> None:
        assert game is not None
        from src.obj.pause import Pause
        game.remove_from_tree(self)
        game.remove_from_tree(self.level)
        game.add_to_tree(Pause())

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def process(self) -> None:
        assert game is not None
        for element in self.elements:
            element.draw(game.display)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            for reaction in self.reactions:
                reaction.handle_event(event)
