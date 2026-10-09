from mazegenerator import MazeGenerator  # type: ignore
from src.obj import GameObject
from src.game import game
import pygame as pg


class Level(GameObject):
    def __init__(self) -> None:
        self.mazegen: MazeGenerator = MazeGenerator()
        self.tileset: pg.Surface = pg.transform.scale_by(
                pg.image.load("assets/tileset.png"), 6.0)

    def process(self) -> None:
        global game
        if not game:
            raise ValueError("ERROR: Game is not initialized!")
        game.display.blit(self.tileset)
