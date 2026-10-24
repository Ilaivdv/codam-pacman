from ..ui_constant import GAP_DEFAULT, FONT_RANK_S, FONT_DEFAULT
from src.utils.colors import LIGHT_GRAY, PURPLE
from .. import Text, Button, Overlay, add_gap
from src.utils import GameObject
from src.game import game
from typing import Any
import pygame as pg


class Instruction(GameObject):
    def __init__(self) -> None:
        assert game is not None
        area = game.display.get_rect()
        self.bg: Overlay = Overlay(area.center, size=(1300, 1200))
        with open('assets/instruction.md', 'r', encoding='utf-8') as f:
            content = f.readlines()
        all_text = content
        x, y = add_gap(self.bg.rect.topleft, (50, 10))
        self.elements: list[Any] = []
        for line in all_text:
            if len(line) == 0:
                continue
            elif len(line) > 0 and len(line) < 10:
                title = Text(line, (x, y), font=FONT_DEFAULT, color=PURPLE,
                             align="midleft")
            else:
                title = Text(line, (x, y), font=FONT_RANK_S,
                             color=LIGHT_GRAY,
                             align="midleft")
            _, y = add_gap(title.rect.center, GAP_DEFAULT)
            self.elements.append(title)
        self.bu: Button = Button("Close", add_gap(self.bg.rect.midbottom,
                                                  (0, -140)),
                                 "midtop", (0, 60), self.back_to_menu)
        self.elements.append(self.bu)

    def back_to_menu(self) -> None:
        assert game is not None
        from ..screens.menu import Menu
        game.remove_from_tree(self)
        game.add_to_tree(Menu())

    def __str__(self) -> str:
        return (self.__class__.__name__)

    def process(self) -> None:
        assert game is not None
        self.bg.draw(game.display)
        for i in self.elements:
            i.draw(game.display)
        for event in pg.event.get():
            self.bu.handle_event(event)
