from ..ui_constant import SIZE_LIFE, SIZE_PAUSE, FONT_RANK
from src.utils.colors import LIGHT_GRAY, PINK, RED
from src.game import game, settings
from ..ui_element import add_gap
from src.utils import GameObject
from ..non_clickable import Text
from ..clickable import Image
from typing import Any
import pygame as pg


class LevelOverlay(GameObject):
    def __init__(self) -> None:
        assert game is not None
        assert settings is not None
        self.area: pg.Rect = game.display.get_rect()
        path: str = "assets/pacgum.png"
        life: Image = Image(path, SIZE_LIFE,
                            add_gap(self.area.topleft, (20, 20)),
                            "topleft")
        pause: Image = Image("assets/pause.png", SIZE_PAUSE,
                             add_gap(self.area.bottomright, (-20, -100)),
                             align="bottomright", on_click=self.pause,
                             hover=True)
        level: Text = Text("LEVEL #TODO",
                           add_gap(self.area.bottomleft, (20, -140)),
                           font=FONT_RANK, color=LIGHT_GRAY,
                           align="bottomleft")
        self.elements: list[Any] = [pause, level]
        self.lives: list[Image] = [life]
        if game.player_lives > 1:
            for _ in range(game.player_lives - 1):
                life = Image(path, SIZE_LIFE, add_gap(life.rect.midright,
                                                      (20, 0)),
                             "midleft")
                self.lives.append(life)
        self.reactions: list[Any] = [pause]
        self.elapsed: int = 0
        self.level_max_time: int = settings.level_max_time
        self.start: int = pg.time.get_ticks()
        self.time_left: int = self.level_max_time
        self.minute = str(int(self.time_left / 60)).zfill(2)
        self.second = str(int(self.time_left % 60)).zfill(2)
        self.win_score: int = settings.points_per_pacgum * settings.pacgum

    def pause(self) -> None:
        assert game is not None
        game.is_paused = not game.is_paused
        if game.is_paused is True:
            from .pause import Pause
            game.add_to_tree(Pause(), False)
        else:
            game._process_tree.pop()

    def win(self) -> None:
        assert game is not None
        from .win import Win
        game.remove_from_tree(self)
        game._process_tree.pop()
        game.add_to_tree(Win(), False)

    def lose(self) -> None:
        assert game is not None
        from .lose import Lose
        game.process_tree.clear()
        game.current_level = 0
        game.add_to_tree(Lose(), False)

    def process(self) -> None:
        assert game is not None
        self.elapsed += pg.time.get_ticks() - self.start
        print(self.elapsed)
        if game.player_lives <= 0 or self.time_left <= 0:
            game.is_paused = True
            self.lose()
            return
        elif (game.is_paused is False
              and self.time_left >= 0 and self.elapsed >= 1000):
            self.elapsed = 0
            self.time_left -= 1
            # print(self.time_left)
            self.minute = str(int(self.time_left / 60)).zfill(2)
            self.second = str(int(self.time_left % 60)).zfill(2)
            time_remain = Text(f"{self.minute}:{self.second}",
                               self.area.midtop, FONT_RANK,
                               align="center", color=PINK)
            time_remain.draw(game.display)
        elif game.is_paused and self.time_left >= 0:
            time_remain = Text(f"{self.minute}:{self.second}",
                               self.area.midtop, FONT_RANK,
                               align="center", color=PINK)
            time_remain.draw(game.display)
        if self.time_left < 30:
            time_remain = Text(f"{self.minute}:{self.second}",
                               self.area.midtop, FONT_RANK,
                               align="center", color=RED)
            time_remain.draw(game.display)
        
        self.score: Text = Text(f"{game.score.current}",
                                add_gap(self.area.topleft, (20, 30)),
                                font=FONT_RANK, align="topleft")
        self.score.draw(game.display)

        if len(self.lives) > game.player_lives:
            diff = len(self.lives) - game.player_lives
            for _ in range(diff):
                self.lives.pop()
        for element in self.elements:
            element.draw(game.display)
        for life in self.lives:
            life.draw(game.display)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.pause()
        for reaction in self.reactions:
            reaction.handle_event(event)
