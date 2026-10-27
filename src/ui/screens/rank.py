from src.ui.ui_constant import FONT_TITLE, GAP_BIG, FONT_RANK, GAP_MID
from src.utils.colors import DARK_GRAY, YELLOW
from src.utils import GameObject
from ..non_clickable import Text
from ..ui_element import add_gap
from ..clickable import Button
from src.game import game
from typing import Any
import pygame as pg


class Rank(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        title: Text = Text("RANK", area.center, FONT_TITLE, gap=(0, -700),
                           color=YELLOW)
        hint: Text = Text("press SPACE to play", pos=title.rect.midbottom,
                          gap=GAP_MID,
                          align="center")
        self.elements: list[Any] = [title, hint]
        x, y = add_gap(hint.rect.midbottom, GAP_MID)
        for index, name in enumerate(game.score.rank, 1):
            score: int = game.score.rank[name]
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
        from .menu import Menu
        game.remove_from_tree(self)
        game.add_to_tree(Menu())

    def play(self) -> None:
        assert game is not None
        if game.is_paused is True:
            game.is_paused = False
        game.remove_from_tree(self)
        from src.level import LevelManager
        game.add_to_tree(LevelManager())
        

    def process(self) -> None:
        assert game is not None
        game.display.fill(DARK_GRAY)
        for element in self.elements:
            element.draw(game.display)

    def handle_event(self, event: pg.event.Event) -> None:
        for bu in self.buttons:
            bu.handle_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.play()
