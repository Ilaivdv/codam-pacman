from src.obj.consumables import Consumable
from mazegenerator import MazeGenerator  # type: ignore[import-untyped]
from src.utils.colors import BLACK
from src.obj.player import Player
from src.obj.entity import Entity
from src.utils import SpriteSheet
from src.obj.enemy import Enemy
from src.obj import GameObject
from random import randint
from src.game import game  # noqa: F401
import pygame as pg


class Level(GameObject):
    def __init__(self) -> None:
        assert game is not None

        self.mazegen: MazeGenerator = MazeGenerator()
        self.tileset: SpriteSheet = SpriteSheet(image=game.assets.tileset)

        self.mazegen.generate()
        self.maze: list[list[int]] = self.mazegen.maze

        self.screen: pg.Surface = pg.Surface(
                (len(self.maze[0]) * self.tileset.frame_size[0],
                 len(self.maze) * self.tileset.frame_size[1]))
        self.scale: int = self._get_display_maze_scale()
        self.pos: tuple[int, int] = (
                game.display.get_rect().centerx -
                self.screen.get_rect().centerx * self.scale,
                game.display.get_rect().centery -
                self.screen.get_rect().centery * self.scale)

        self.sprite_groups: dict[str, pg.sprite.Group[Entity]] = {
                "consumable": pg.sprite.Group(),
                "enemy": pg.sprite.Group(),
                "player": pg.sprite.Group(),
                }
        self.player_spawn_pos: tuple[int, int] = self._get_maze_center()
        self.player: Player = Player(self.sprite_groups,
                                     self.tileset.frame_size,
                                     self.maze,
                                     self.player_spawn_pos, 1)
        self.pacgums: list[Consumable] = []
        self._spawn_pacgums(30, 4)
        self._super_pacgum_duration: int = 5000
        self._super_pacgum_elapsed: int = 0
        self.enemy0: Enemy = Enemy(self.sprite_groups,
                                   self.tileset.frame_size,
                                   self.maze, (5, 0),
                                   pg.Vector2(self.player_spawn_pos), 1)

    def _get_display_maze_scale(self) -> int:
        assert game is not None
        screen_size: tuple[int, int] = self.screen.get_rect().size
        scale: int = 1

        while screen_size[0] * (scale + 1) < game.resolution[0] and \
                screen_size[1] * (scale + 1) < game.resolution[1]:
            scale += 1
        return scale

    def _get_maze_center(self) -> tuple[int, int]:
        pos: tuple[int, int] = (
                (len(self.maze[0]) - 1) // 2, (len(self.maze) - 1) // 2)
        while self.maze[pos[1]][pos[0]] == 15:
            pos = (pos[0] + 1, pos[1])
        return pos

    def _spawn_pacgums(self, pacgum_amount: int,
                       super_pacgum_amount: int) -> None:
        if pacgum_amount + super_pacgum_amount >= \
                len(self.maze[0]) * len(self.maze):
            # TODO Add warning log here
            print("Too many pacgums! Falling back to defaults")
            max_capacity: int = len(self.maze[0]) * len(self.maze)
            pacgum_amount = max_capacity // 4
            super_pacgum_amount = 4

        is_available: list[list[bool]] = [
                [True if self.maze[y][x] != 15 else False
                 for x in range(len(self.maze[0]))]
                for y in range(len(self.maze))]
        is_available[self.player_spawn_pos[1]][
                self.player_spawn_pos[0]] = False

        spawn_pos: tuple[int, int] = (
                randint(0, len(self.maze[0]) - 1),
                randint(0, len(self.maze) - 1))
        for _ in range(pacgum_amount):
            while not is_available[spawn_pos[1]][spawn_pos[0]]:
                spawn_pos = (randint(0, len(self.maze[0]) - 1),
                             randint(0, len(self.maze) - 1))
            self.pacgums.append(Consumable(self.sprite_groups,
                                           self.tileset.frame_size,
                                           self.maze, spawn_pos, 1))
            is_available[spawn_pos[1]][spawn_pos[0]] = False
        for _ in range(super_pacgum_amount):
            while not is_available[spawn_pos[1]][spawn_pos[0]]:
                spawn_pos = (randint(0, len(self.maze[0]) - 1),
                             randint(0, len(self.maze) - 1))
            self.pacgums.append(Consumable(self.sprite_groups,
                                           self.tileset.frame_size,
                                           self.maze, spawn_pos, 1,
                                           True))
            is_available[spawn_pos[1]][spawn_pos[0]] = False

    def process(self) -> None:
        assert game is not None

        game.display.fill(BLACK)
        self.enemy0.player_pos = pg.Vector2(self.player.current_maze_position)

        # Draw the maze
        for y in range(0, len(self.maze)):
            for x, i in enumerate(self.maze[y]):
                self.screen.blit(self.tileset.frames[i],
                                 (x * self.tileset.frame_size[0],
                                  y * self.tileset.frame_size[1]))

        for group in self.sprite_groups.values():
            group.draw(self.screen)

        game.display.blit(pg.transform.scale_by(self.screen, self.scale),
                          self.pos)

        if game.player_is_super and \
                self._super_pacgum_elapsed <= self._super_pacgum_duration:
            self._super_pacgum_elapsed += game.clock.get_time()
        elif game.player_is_super:
            self._super_pacgum_elapsed = 0
            game.player_is_super = False
