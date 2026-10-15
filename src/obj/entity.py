from abc import abstractmethod, ABC
from src.obj import GameObject
from enum import IntEnum
import pygame as pg


class error(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Direction(IntEnum):
    NONE = 0
    UP = 1
    RIGHT = 2
    DOWN = 4
    LEFT = 8


class Entity(GameObject, pg.sprite.Sprite, ABC):
    def __init__(self,
                 image: pg.Surface,
                 pos: tuple[int, int],
                 maze: list[list[int]],
                 speed: int = 1,
                 **collides_with: pg.sprite.Group[Entity]) -> None:
        super().__init__()

        self.collides_with: dict[str, pg.sprite.Group[Entity]] = collides_with
        self.image: pg.Surface = image
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.topleft = pos

        self.maze: list[list[int]] = maze
        self.current_maze_position: tuple[int, int] = pos
        self.target_position: pg.Vector2 = pg.Vector2(pos)
        self.move_direction: Direction = Direction.NONE
        self.speed: int = speed

    def target_reached(self) -> bool:
        if pg.Vector2(self.rect.topleft) == self.target_position:
            self.current_maze_position = (int(self.target_position.x //
                                              self.rect.width),
                                          int(self.target_position.y //
                                              self.rect.height))
            return True
        else:
            return False

    def move_to_pos(self, direction: Direction) -> None:
        if not self.target_reached() or self.maze[
                self.current_maze_position[1]][
                        self.current_maze_position[0]] & direction:
            return
        self.move_direction = direction
        match direction:
            case Direction.NONE:
                pass
            case Direction.UP:
                self.target_position.y -= self.rect.height
            case Direction.RIGHT:
                self.target_position.x += self.rect.width
            case Direction.DOWN:
                self.target_position.y += self.rect.height
            case Direction.LEFT:
                self.target_position.x -= self.rect.width

    @abstractmethod
    def process(self) -> None:
        for name, group in self.collides_with.items():
            if pg.sprite.spritecollide(self, group, False):
                self.on_collide(name)

        if self.target_reached():
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
