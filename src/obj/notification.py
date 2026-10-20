import pygame as pg
from src.game import game, settings
from src.obj import GameObject
from src.ui import GAP_DEFAULT
from src.ui.uielement import Noti, add_gap
import textwrap


class Notification(GameObject):
    def __init__(self) -> None:
        assert game is not None
        assert settings is not None
        self.hold = 2000
        self.fade = 2000
        self.start = pg.time.get_ticks()
        area = game.display.get_rect()
        all_text: str = ""
        messages = settings.notification
        for i in messages:
            all_text += "\n".join(textwrap.wrap(i, width=50))
            all_text += "\n"
        self.noti: Noti = Noti(all_text,
                               add_gap(area.topright, GAP_DEFAULT),
                               "midright")

    def init(self) -> None:
        assert game is not None
        game.remove_from_tree(self)

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def process(self) -> None:
        assert game is not None
        progress: int = pg.time.get_ticks() - self.start
        if self.hold + self.fade <= progress:
            self.init()
            pg.display.update()
            return
        if progress <= self.hold:
            alpha: float | int = 1
        else:
            alpha = 1 - (progress - self.hold) / self.fade
        self.noti.surface.set_alpha(int(alpha * 255))
        self.noti.draw(game.display)
        pg.display.update()
