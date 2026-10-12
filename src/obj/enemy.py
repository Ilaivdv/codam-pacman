from src.obj.entity import Entity
import pygame as pg


class Enemy(Entity):
    def process(self) -> None:
        ...

    def on_collide(self) -> None:
        ...
