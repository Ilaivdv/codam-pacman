from .ui_constant import GAP_DEFAULT
from src.game import game, settings
from src.utils import GameObject
from .non_clickable import Noti
from .ui_element import add_gap
import pygame as pg
import textwrap


class Notification(GameObject):
    def __init__(self) -> None:
        assert game is not None
        assert settings is not None
        self.hold: int = 2000
        self.fade: int = 2000
        area = game.display.get_rect()
        all_text: str = ""
        messages = settings.notification
        for i in messages:
            all_text += "\n".join(textwrap.wrap(i, width=50))
            all_text += "\n"
        self.noti: Noti = Noti(all_text,
                               add_gap(area.topright, GAP_DEFAULT),
                               "midright")
        self.alpha: int = 255
        self.elapsed: int = 0

    def process(self) -> None:
        assert game is not None
        self.elapsed += pg.time.get_ticks()
        if self.elapsed >= self.hold:
            self.alpha -= 2
            self.noti.surface.set_alpha(self.alpha)
        if self.alpha <= 0:
            assert game is not None
            game.remove_from_tree(self)
        self.noti.draw(game.display)
