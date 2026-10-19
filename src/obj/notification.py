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
        self.duration = 4000
        self.active = True
        self.start = pg.time.get_ticks()
        area = game.display.get_rect()
        all_text: str = ""
        self.notis: list[Noti] = []
        if not settings.notification:
            messages = ["NOTICE: Missing {key} in config.json,"
                        "using a default value: points_per_super_pacgum",
                        "NOTICE: Missing {key} in config.json, "
                        "using a default value."]
        else:
            messages = settings.notification
        for i in messages:
            all_text += "\n".join(textwrap.wrap(i, width=50))
            all_text += "\n"
        bu = Noti(all_text,
                  add_gap(area.topright, GAP_DEFAULT),
                  "midright")
        self.notis.append(bu)

    def init(self) -> None:
        self.active = False
        self.notis.clear()

    def process(self) -> None:
        assert game is not None
        if not self.active:
            return
        now = pg.time.get_ticks()
        if self.start + self.duration < now:
            self.init()
            pg.display.update()
            return
        for bu in self.notis:
            bu.draw(game.display)
