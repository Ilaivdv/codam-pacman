from abc import abstractmethod, ABC
from src.obj import GameObject
from typing import Literal
import pygame as pg


class Entity(GameObject, pg.sprite.Sprite, ABC):
    def __init__(self,
                 collides_with: Literal["player", "enemy", "interactable"]
                 ) -> None:
        super().__init__()

        self.collides_with: str = collides_with
        # self.image: pg.Surface

    @abstractmethod
    def on_collide(self) -> None:
        ...
