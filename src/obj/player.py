from src.obj.entity import Entity, Direction
from src.utils import SpriteSheet
from src.game import game
import pygame as pg


class Player(Entity):
    def __init__(self,
                 sprite_groups: dict[str, pg.sprite.Group[Entity]],
                 tile_size: tuple[int, int],
                 maze: list[list[int]],
                 pos: tuple[int, int],
                 speed: int = 1
                 ) -> None:
        assert game is not None

        self.sprite: SpriteSheet = SpriteSheet(image=game.assets.player)
        super().__init__(sprite_groups, tile_size, self.sprite.frames[0],
                         maze, pos, speed)
        self.sprite_groups["player"].add(self)
        self.collides_with: dict[str, pg.sprite.Group[Entity]] = {
                k: self.sprite_groups[k] for k in ["enemy"]}

        self.stop_at_target: bool = False
        self.current_speed: int = self.speed
        self.input_buffer: Direction = Direction.NONE
        self.sprite.animations = {
                "idle": [3],
                "moving": [0, 1, 3, 2, 1],
                "dead": [4, 5, 6, 7, 8, 9, 10, 11, 11, 12, 13, 14, 15]
                }
        self.rotation: int = 0
        self.flipped: bool = False

        self.is_dead: bool = False

        game.add_to_tree(self)

    def process(self) -> None:
        super().process()
        assert game is not None

        if self.is_dead:
            self.image = self.sprite.process_animation("dead",
                                                       game.clock.get_time())
            self.move_direction = Direction.NONE
            if self.sprite.animation_finished:
                game.remove_from_tree(self)
                self.remove(self.sprite_groups["player"])
            return

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

        curr_anim: str = "moving"
        match self.move_direction:
            case Direction.NONE:
                curr_anim = "idle"
            case Direction.UP:
                self.rotation = 90
            case Direction.RIGHT:
                self.flipped = False
                self.rotation = 0
            case Direction.DOWN:
                self.rotation = -90
            case Direction.LEFT:
                self.flipped = True
                self.rotation = 0
        self.image = self.sprite.process_animation(curr_anim,
                                                   game.clock.get_time())
        self.image = pg.transform.rotate(self.image, self.rotation)
        self.image = pg.transform.flip(self.image, self.flipped, False)

    def on_collide(self, group_name: str) -> None:
        assert game is not None
        self.is_dead = True
