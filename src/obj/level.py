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
                "enemy": pg.sprite.Group(),
                "interactable": pg.sprite.Group(),
                }
        self.player: Player = Player(game.assets.player, (0, 0),
                                     self.maze, speed=1,
                                     **{k: self.sprite_groups[k] for k in [
                                         "enemy", "interactable"]})
        self.sprite_groups["player"].add(self.player)

    def _get_display_maze_scale(self) -> int:
        assert game is not None
        screen_size: tuple[int, int] = self.screen.get_rect().size
        scale: int = 1

        while screen_size[0] * (scale + 1) < game.resolution[0] and \
                screen_size[1] * (scale + 1) < game.resolution[1]:
            scale += 1
        return scale

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
