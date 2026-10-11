from mazegenerator import MazeGenerator  # type: ignore[import-untyped]
from src.obj import GameObject
from src.utils import Tileset
from src.game import game  # noqa: F401
import pygame as pg


class Level(GameObject):
    def __init__(self) -> None:
        self.mazegen: MazeGenerator = MazeGenerator()
        self.tileset: Tileset = Tileset(image=pg.image.load(
            "assets/tileset.png").convert())

        self.mazegen.generate()
        self.maze: list[list[int]] = self.mazegen.maze
        self.scale: int = 4

    def process(self) -> None:
        if not game:
            raise ValueError("ERROR: Game is not initialized!")
        for y in range(0, len(self.maze)):
            for x, i in enumerate(self.maze[y]):
                game.display.blit(pg.transform.scale_by(
                    self.tileset.tiles[i], self.scale),
                                  (x * self.tileset.tile_size[0] * self.scale,
                                   y * self.tileset.tile_size[1] * self.scale))
