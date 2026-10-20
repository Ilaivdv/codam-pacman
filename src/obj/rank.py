import pygame as pg
from src.game import game
import sys
from src.obj import GameObject
from src.ui.uielement import Button, Text, add_gap
from src.ui import FONT_TITLE, GAP_BIG, GAP_DEFAULT
from src.utils.colors import DARK_GRAY, YELLOW
from typing import Any


class Rank(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        title: Text = Text("Pac-Man", area.center, FONT_TITLE, gap=(0, -200),
                           color=YELLOW)
        hint: Text = Text("press SPACE to play", pos=title.rect.midbottom,
                          align="center")
        self.elements: list[Any] = [title, hint]
        x, y = add_gap(hint.rect.midbottom, GAP_DEFAULT)
        for index, name in enumerate(game._score.rank, 1):
            score: int = game._score.current
            text = Text(f"{index}.{name} - {score}pts", (x, y))
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

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def play(self) -> None:
        assert game is not None
        from src.obj.level import Level
        game.remove_from_tree(self)
        game.add_to_tree(Level())

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
