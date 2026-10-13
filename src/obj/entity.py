from abc import abstractmethod, ABC
from src.obj import GameObject
import pygame as pg


class Entity(GameObject, pg.sprite.Sprite, ABC):
    def __init__(self, image: pg.Surface,
                 **collides_with: pg.sprite.Group[Entity]) -> None:
        super().__init__()

        self.collides_with: dict[str, pg.sprite.Group[Entity]] = collides_with

    @abstractmethod
    def process(self) -> None:
        for name, group in self.collides_with.items():
            if pg.sprite.spritecollide(self, group, False):
                self.on_collide(name)

    @abstractmethod
    def on_collide(self, group_name: str) -> None:
        ...
