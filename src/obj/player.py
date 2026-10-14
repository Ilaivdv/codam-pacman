from src.obj.entity import Entity
# import pygame as pg


class Player(Entity):
    def process(self) -> None:
        ...

    def on_collide(self, group_name: str) -> None:
        ...
