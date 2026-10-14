from src.obj.entity import Entity
from src.game import game
import pygame as pg


class Player(Entity):
    def __init__(self, image: pg.Surface, pos: pg.Vector2,
                 **collides_with: pg.sprite.Group[Entity]) -> None:
        super().__init__(image, pos)
        assert game is not None

        self.collides_with: dict[str, pg.sprite.Group[Entity]] = collides_with
        self.current_speed: int = self.speed
        self.is_flipped: bool = False
        game.add_to_tree(self)

    def process(self) -> None:
        key_just_pressed = pg.key.get_just_pressed()
        self.current_speed = not self.current_speed

        # if key_pressed[pg.K_w] or key_pressed[pg.K_UP]:
        #     self.rect.y -= self.current_speed
        # if key_pressed[pg.K_a] or key_pressed[pg.K_LEFT]:
        #     self.rect.x -= self.current_speed
        # if key_pressed[pg.K_s] or key_pressed[pg.K_DOWN]:
        #     self.rect.y += self.current_speed
        # if key_pressed[pg.K_d] or key_pressed[pg.K_RIGHT]:
        #     self.rect.x += self.current_speed


    def on_collide(self, group_name: str) -> None:
        ...
