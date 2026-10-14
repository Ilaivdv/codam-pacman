from abc import abstractmethod, ABC
from src.obj import GameObject
import pygame as pg


class Entity(GameObject, pg.sprite.Sprite, ABC):
    def __init__(self, image: pg.Surface, pos: pg.Vector2,
                 speed: int = 1.0,
                 **collides_with: pg.sprite.Group[Entity]) -> None:
        super().__init__()

        self.image: pg.Surface = image
        self.rect: pg.Rect = self.image.get_rect()
        self.rect.topleft = pos
        self.collides_with: dict[str, pg.sprite.Group[Entity]] = collides_with
        self.speed: int = speed

    @abstractmethod
    def process(self) -> None:
        for name, group in self.collides_with.items():
            if pg.sprite.spritecollide(self, group, False):
                self.on_collide(name)

    @abstractmethod
    def on_collide(self, group_name: str) -> None:
        ...
