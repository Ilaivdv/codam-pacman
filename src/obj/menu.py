from src.obj import GameObject
from src.ui import Button, Image
from src.ui.color import LIGHT
from src.game import game
from typing import Any
import pygame as pg
import sys


class Menu(GameObject):
    def process(self) -> None:
        assert game is not None

        game.display.fill(LIGHT)
        area = game.display.get_rect()
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
            element.draw(game.display)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            pg.display.update()
