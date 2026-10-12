from abc import abstractmethod, ABC
from src.obj import GameObject
import pygame as pg


class Entity(GameObject, pg.sprite.Sprite, ABC):
    def __init__(self) -> None:
        super(pg.sprite.Sprite()).__init__()

        self.image: pg.Surface

    @abstractmethod
    def process(self) -> None:
        if pg.sprite.spritecollide(self):
            ...

    @abstractmethod
    def on_collide(self) -> None:
        ...
