from src.obj.entity import Entity, Direction
from src.game import game
import pygame as pg


class Player(Entity):
    def __init__(self,
                 image: pg.Surface,
                 pos: tuple[int, int],
                 maze: list[list[int]],
                 speed: int = 1,
                 **collides_with: pg.sprite.Group[Entity]) -> None:
        super().__init__(image, pos, maze)
        self.stop_at_target: bool = False
        assert game is not None

        self.collides_with: dict[str, pg.sprite.Group[Entity]] = collides_with
        self.current_speed: int = self.speed
        self.is_flipped: bool = False
        self.input_buffer: Direction = Direction.NONE

        game.add_to_tree(self)

    def process(self) -> None:
        super().process()
        key_pressed = pg.key.get_just_pressed()

        if key_pressed[pg.K_w] or key_pressed[pg.K_UP]:
            self.move_to_pos(Direction.UP)
            self.input_buffer = Direction.UP
        if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
            self.move_to_pos(Direction.LEFT)
            self.input_buffer = Direction.LEFT
        if key_pressed[pg.K_s] or key_pressed[pg.K_DOWN]:
            self.move_to_pos(Direction.DOWN)
            self.input_buffer = Direction.DOWN
        if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
            self.move_to_pos(Direction.RIGHT)
            self.input_buffer = Direction.RIGHT

        if self.target_reached() and not self.stop_at_target:
            if self._validate_direction(self.input_buffer):
                self.move_to_pos(self.input_buffer)
            elif not self.move_to_pos(self.move_direction):
                self.move_direction = Direction.NONE

    def on_collide(self, group_name: str) -> None:
        ...
