import pygame as pg
from src.game import game, settings
import sys
from src.obj import GameObject
from src.ui.uielement import Text, add_gap, Image
from src.ui.uiconstant import (GAP_LIFE, GAP_SCORE, SIZE_LIFE,
                               SIZE_PAUSE, FONT_RANK)
from src.utils.colors import LIGHT_GRAY, PINK, RED
from typing import Any


class Level_add(GameObject):
    def __init__(self) -> None:
        assert game is not None
        self.area = game.display.get_rect()
        path: str = "assets/pacgum.png"
        life: Image = Image(path, SIZE_LIFE,
                            add_gap(self.area.midtop, GAP_LIFE),
                            "midtop")
        self.elapsed: float = 0
        score: Text = Text(f"{game._score.current}", add_gap(self.area.midtop,
                                                             GAP_SCORE),
                           font=FONT_RANK, align="midleft")
        _, y = self.area.midbottom
        pause: Image = Image("assets/pause.png", SIZE_PAUSE,
                             (score.rect.x, y - 100),
                             align="midbottom", on_click=self.pause)
        level: Text = Text("Lv 1", (life.rect.x, pause.rect.y - 30),
                           font=FONT_RANK, color=LIGHT_GRAY,
                           align="midleft")
        self.elements: list[Any] = [life, score, pause, level]
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

    # def win(self) -> None:
    #     from src.obj.win import Win
    #     game.add_to_tree(Win())
    # def lose(self) -> None:
    #     from src.obj.lose import Lose
    #     game.add_to_tree(Lose())

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def process(self) -> None:
        assert game is not None
        assert settings is not None
        self.elapsed += pg.time.get_ticks()
        time_left: int = settings.level_max_time - int(self.elapsed / 100000)
        if time_left >= 0:
            minute: str = str(int(time_left / 60)).zfill(2)
            second: str = str(int(time_left % 60)).zfill(2)
            if time_left < 30:
                time_remain = Text(f"{minute}:{second}",
                                   self.area.midtop, FONT_RANK,
                                   align="center", color=RED)
            else:
                time_remain = Text(f"{minute}:{second}",
                                   self.area.midtop, FONT_RANK,
                                   align="center", color=PINK)
            time_remain.draw(game.display)
        else:
            time_remain = Text("00:00",
                               self.area.midtop, FONT_RANK,
                               align="center", color=RED)
            time_remain.draw(game.display)
            # if pacgum all eaten and life left win
            # else if life left, -1 life
            # else lose
            self.pause()
        for element in self.elements:
            element.draw(game.display)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.pause()
            for reaction in self.reactions:
                reaction.handle_event(event)
