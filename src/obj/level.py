from mazegenerator import MazeGenerator  # type: ignore
from src.obj import GameObject
from src.utils import Tileset
from src.game import game  # noqa: F401
import pygame as pg


class Level(GameObject):
    def __init__(self) -> None:
        self.mazegen: MazeGenerator = MazeGenerator()
        self.tileset: Tileset = Tileset(image=pg.image.load(
            "assets/tileset.png").convert())

    def process(self) -> None:
        if not game:
            raise ValueError("ERROR: Game is not initialized!")
        game.display.blit(pg.transform.scale_by(self.tileset.tiles[0], 5.0),
                          (0,0))
