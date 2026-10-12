from mazegenerator import MazeGenerator  # type: ignore[import-untyped]
from src.obj import GameObject
from src.utils import Tileset
from src.game import game  # noqa: F401
import pygame as pg


class Level(GameObject):
    def __init__(self) -> None:
        assert game is not None

        self.mazegen: MazeGenerator = MazeGenerator((21,21))
        self.tileset: Tileset = Tileset(image=pg.image.load(
            "assets/tileset.png").convert())

        self.mazegen.generate()
        self.maze: list[list[int]] = self.mazegen.maze

        self.screen: pg.Surface = pg.Surface(
                (len(self.maze[0]) * self.tileset.tile_size[0],
                 len(self.maze) * self.tileset.tile_size[1]))
        self.scale: int = 5
        self.pos: tuple[int, int] = (
                game.display.get_rect().centerx -
                self.screen.get_rect().centerx * self.scale,
                game.display.get_rect().centery -
                (self.screen.get_rect().centery +
                 self.tileset.tile_size[1] // 2) * self.scale)

    def process(self) -> None:
        assert game is not None

        # Draw the maze
        for y in range(0, len(self.maze)):
            for x, i in enumerate(self.maze[y]):
                self.screen.blit(self.tileset.tiles[i],
                                 (x * self.tileset.tile_size[0],
                                  y * self.tileset.tile_size[1]))

        game.display.blit(pg.transform.scale_by(self.screen, self.scale),
                          self.pos)
