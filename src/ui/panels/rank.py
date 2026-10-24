import pygame as pg
from src.game import game
import sys
from src.utils import GameObject
from src.ui import Button, Text, add_gap
from src.ui.ui_constant import FONT_TITLE, GAP_BIG, FONT_RANK, GAP_MID
from src.utils.colors import DARK_GRAY, YELLOW
from typing import Any


class Rank(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        title: Text = Text("Pac-Man", area.center, FONT_TITLE, gap=(0, -500),
                           color=YELLOW)
        hint: Text = Text("press SPACE to play", pos=title.rect.midbottom,
                          gap=GAP_MID,
                          align="center")
        self.elements: list[Any] = [title, hint]
        x, y = add_gap(hint.rect.midbottom, GAP_MID)
        for index, name in enumerate(game._score.rank, 1):
            score: int = game._score.current
            text = Text(f"{index}. {name} - {score} pts", (x, y),
                        font=FONT_RANK)
            x, y = text.rect.midbottom
            self.elements.append(text)
        bu: Button = Button("Back to menu", (x, y),
                            "midbottom", GAP_BIG, self.back_to_menu)
        self.buttons: list[Button] = [bu]
        self.elements.append(bu)

    def back_to_menu(self) -> None:
        assert game is not None
        from src.obj.menu import Menu
        game.remove_from_tree(self)
        game.add_to_tree(Menu())

    def play(self) -> None:
        assert game is not None
        if game.is_paused is True:
            game.is_paused = False
        else:
            from src.obj.level import Level
            from src.obj.level_add import Level_add
            level: Level = Level()
            game.add_to_tree(Level_add())
            game.add_to_tree(level)
        game.remove_from_tree(self)

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
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.play()
