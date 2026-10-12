from src.obj.entity import Entity
import pygame as pg


class Player(Entity):
    def process(self) -> None:
        super().process()

    def on_collide(self) -> None:
        ...
