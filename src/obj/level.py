from src.obj.consumables import Consumable
from mazegenerator import MazeGenerator  # type: ignore[import-untyped]
from src.utils.colors import BLACK
from src.obj.player import Player
from src.obj.entity import Entity
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
        self.scale: int = self._get_display_maze_scale()

        self.pos: tuple[int, int] = (
                game.display.get_rect().centerx -
                self.screen.get_rect().centerx * self.scale,
                game.display.get_rect().centery -
                self.screen.get_rect().centery * self.scale)

        self.sprite_groups: dict[str, pg.sprite.Group[Entity]] = {
                "player": pg.sprite.Group(),
                "consumable": pg.sprite.Group(),
                "enemy": pg.sprite.Group(),
                }
        self.player: Player = Player(self.sprite_groups,
                                     game.assets.player,
                                     self.maze, (0, 0), 1)
        self.sprite_groups["player"].add(self.player)
        self.pacgum: Consumable = Consumable(self.sprite_groups,
                                             game.assets.pacgum,
                                             self.maze, (16, 0), 1)
        self.sprite_groups["consumable"].add(self.pacgum)

    def _get_display_maze_scale(self) -> int:
        assert game is not None
        screen_size: tuple[int, int] = self.screen.get_rect().size
        scale: int = 1

        while screen_size[0] * (scale + 1) < game.resolution[0] and \
                screen_size[1] * (scale + 1) < game.resolution[1]:
            scale += 1
        return scale

    def _to_global_pos(self, pos: tuple[int, int],
                       rect_size: tuple[int, int]) -> tuple[int, int]:
        offset_x, offset_y = self.tileset.tile_size
        return ((pos[0] * offset_x) + (offset_x - rect_size[0]) // 2,
                (pos[1] * offset_y) + (offset_y - rect_size[1]) // 2)

    def process(self) -> None:
        assert game is not None

        game.display.fill(BLACK)

        # Draw the maze
        for y in range(0, len(self.maze)):
            for x, i in enumerate(self.maze[y]):
                self.screen.blit(self.tileset.tiles[i],
                                 (x * self.tileset.tile_size[0],
                                  y * self.tileset.tile_size[1]))

        for group in self.sprite_groups.values():
            group.draw(self.screen)

        game.display.blit(pg.transform.scale_by(self.screen, self.scale),
                          self.pos)
