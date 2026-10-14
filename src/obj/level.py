from mazegenerator import MazeGenerator  # type: ignore[import-untyped]
from src.utils.colors import BLACK
from src.obj.player import Player
from src.obj.enemy import Enemy
from src.obj import GameObject
from src.utils import Tileset
from src.game import game  # noqa: F401
import pygame as pg


class Level(GameObject):
    def __init__(self) -> None:
        assert game is not None

        self.mazegen: MazeGenerator = MazeGenerator()
        self.tileset: Tileset = Tileset(image=game.assets.tileset)

        self.mazegen.generate()
        self.maze: list[list[int]] = self.mazegen.maze

        self.screen: pg.Surface = pg.Surface(
                (len(self.maze[0]) * self.tileset.tile_size[0],
                 len(self.maze) * self.tileset.tile_size[1]))
        self.scale: int = 6
        self.pos: tuple[int, int] = (
                game.display.get_rect().centerx -
                self.screen.get_rect().centerx * self.scale,
                game.display.get_rect().centery -
                (self.screen.get_rect().centery +
                 self.tileset.tile_size[1] // 2) * self.scale)

        self.sprite_groups: dict[str, pg.sprite.Group[Player | Enemy]] = {
                "player": pg.sprite.Group(),
                "enemy": pg.sprite.Group(),
                "interactable": pg.sprite.Group(),
                }
        # self.enemy: Enemy = Enemy(**{k: self.sprite_groups[k] for k in [
        #     "player"]})

    def process(self) -> None:
        assert game is not None

        game.display.fill(BLACK)

        # Draw the maze
        for y in range(0, len(self.maze)):
            for x, i in enumerate(self.maze[y]):
                self.screen.blit(self.tileset.tiles[i],
                                 (x * self.tileset.tile_size[0],
                                  y * self.tileset.tile_size[1]))

        game.display.blit(pg.transform.scale_by(self.screen, self.scale),
                          self.pos)
