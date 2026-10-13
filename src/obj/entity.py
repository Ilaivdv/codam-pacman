from abc import abstractmethod, ABC
from src.obj import GameObject
from typing import Literal
from collections.abc import Container
import pygame as pg


class Entity(GameObject, pg.sprite.Sprite, ABC):
    def __init__(self, collides_with: set[
        Literal["player", "enemy", "interactable"]]) -> None:
        super().__init__()

        self.collides_with: Container[str] = collides_with
        # self.image: pg.Surface

    # @abstractmethod()

    @abstractmethod
    def on_collide(self) -> None:
        ...
