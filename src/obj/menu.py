import pygame as pg
from src.game import Game
import sys
from src.obj import GameObject
from src.ui import Button, Image
from src.ui.color import LIGHT
from typing import Any


class Menu(GameObject):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def process(self) -> None:
        pg.init()
        self.game.display.fill(LIGHT)
        area = self.game.display.get_rect()
        path = "assets/pacman-outfit-0.jpg"
        start_im = Image(path, None, area.midtop, "midtop")
        elements: list[Any] = [start_im]
        labels = ["Play", "Rank", "Quit"]
        Gap = 50
        y = area.centery
        for label in labels:
            bu = Button(label, (140, 50), (area.centerx, y), "midtop")
            elements.append(bu)
            y = bu.rect.bottom + Gap

        for element in elements:
            element.draw(self.game.display)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            pg.display.update()
