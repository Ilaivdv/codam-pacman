from abc import abstractmethod, ABC
from src.utils import GameObject
from enum import IntEnum
import pygame as pg


class Direction(IntEnum):
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8


class Entity(GameObject, pg.sprite.Sprite, ABC):
    def __init__(self,
                 sprite_groups: dict[str, pg.sprite.Group[Entity]],
                 tile_size: tuple[int, int],
                 image: pg.Surface,
                 maze: list[list[int]],
                 pos: tuple[int, int],
                 speed: int = 1
                 ) -> None:
        super().__init__()

        self.maze: list[list[int]] = maze
        self.tile_size: tuple[int, int] = tile_size
        self.sprite_groups: dict[str, pg.sprite.Group[Entity]] = sprite_groups
        self.collides_with: dict[str, pg.sprite.Group[Entity]] = {}
        self.image: pg.Surface = image
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.topleft = self._to_global_pos(pos)

        self.current_maze_position: tuple[int, int] = pos
        self.spawn_position: tuple[int, int] = pos
        self.target_position: pg.Vector2 = pg.Vector2(
                self._to_global_pos(pos))
        self.move_direction: Direction = Direction.NONE
        self.speed: int = speed

        self.stop_at_target: bool = True

    def _to_global_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        offset_x, offset_y = self.tile_size
        return ((pos[0] * offset_x) + (offset_x - self.rect.width) // 2,
                (pos[1] * offset_y) + (offset_y - self.rect.height) // 2)

    def get_neighbors(self,
                      pos: tuple[int, int] | None = None) -> list[Direction]:
        if not pos:
            pos = self.current_maze_position

        res: list[Direction] = []
        x, y = pos
        for i in Direction:
            if i == Direction.NONE:
                continue
            if not self.maze[y][x] & i:
                res.append(i)
        return res

    def _get_maze_cell(self, direction: Direction,
                       from_pos: tuple[int, int] | None = None
                       ) -> tuple[int, int]:
        if from_pos is None:
            from_pos = self.current_maze_position
        if not self._validate_direction(direction, from_pos):
            return from_pos

        res: tuple[int, int]
        match direction:
            case Direction.UP:
                res = (from_pos[0],
                       from_pos[1] - 1)
            case Direction.RIGHT:
                res = (from_pos[0] + 1,
                       from_pos[1])
            case Direction.DOWN:
                res = (from_pos[0],
                       from_pos[1] + 1)
            case Direction.LEFT:
                res = (from_pos[0] - 1,
                       from_pos[1])
            case Direction.NONE:
                res = from_pos
        return res

    def target_reached(self) -> bool:
        if pg.Vector2(self.rect.topleft) == self.target_position:
            self.current_maze_position = (int(self.target_position.x //
                                              self.tile_size[0]),
                                          int(self.target_position.y //
                                              self.tile_size[1]))
            return True
        else:
            return False

    def _validate_direction(self, direction: Direction,
                            from_pos: tuple[int, int] | None = None
                            ) -> bool:
        if from_pos is None:
            from_pos = self.current_maze_position
        if self.maze[from_pos[1]][
                from_pos[0]] & direction:
            return False
        else:
            return True

    def move_to_pos(self, direction: Direction) -> bool:
        if not self.target_reached() or \
                not self._validate_direction(direction):
            return False

        self.move_direction = direction
        match direction:
            case Direction.NONE:
                pass
            case Direction.UP:
                self.target_position.y -= self.tile_size[1]
            case Direction.RIGHT:
                self.target_position.x += self.tile_size[0]
            case Direction.DOWN:
                self.target_position.y += self.tile_size[1]
            case Direction.LEFT:
                self.target_position.x -= self.tile_size[0]
        return True

    @abstractmethod
    def process(self) -> None:
        for name, group in self.collides_with.items():
            if pg.sprite.spritecollide(
                    self, group, False, pg.sprite.collide_rect_ratio(0.5)):
                self.on_collide(name)

        if self.target_reached() and self.stop_at_target:
            self.move_direction = Direction.NONE
        match self.move_direction:
            case Direction.NONE:
                pass
            case Direction.UP:
                self.rect.y -= self.speed
            case Direction.RIGHT:
                self.rect.x += self.speed
            case Direction.DOWN:
                self.rect.y += self.speed
            case Direction.LEFT:
                self.rect.x -= self.speed

    @abstractmethod
    def on_collide(self, group_name: str) -> None:
        ...

    def __str__(self) -> str:
        """ Returns the name of parent class. """
        return self.__class__.__name__
