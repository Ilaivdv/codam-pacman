import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui.uielement import Text, add_gap, Image
from src.ui.uiconstant import GAP_LIFE, GAP_SCORE, SIZE_LIFE, SIZE_PAUSE
from typing import Any


class Level_add(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        path: str = "assets/pacgum.png"
        life: Image = Image(path, SIZE_LIFE, add_gap(area.midtop, GAP_LIFE),
                            "midtop")
        score: Text = Text(f"{game._score.current}", add_gap(area.midtop,
                                                             GAP_SCORE),
                           align="midleft")
        _, y = area.midbottom
        pause: Image = Image("assets/pause.png", SIZE_PAUSE,
                             (score.rect.x, y - 100),
                             align="midbottom", on_click=self.pause)
        self.elements: list[Any] = [life, score, pause]
        for _ in range(game._life - 1):
            life = Image(path, SIZE_LIFE, add_gap(life.rect.midright, (20, 0)),
                         "midleft")
            self.elements.append(life)
        self.reactions: list[Any] = [pause]

    def pause(self) -> None:
        assert game is not None
        from src.obj.pause import Pause
        game.add_to_tree(Pause(), False)
        game.is_paused = True

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
