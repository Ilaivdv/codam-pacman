from src.obj.entity import Entity
from src.game import game
import pygame as pg


class Consumable(Entity):
    def __init__(self,
                 sprite_groups: dict[str, pg.sprite.Group[Entity]],
                 maze: list[list[int]],
                 pos: tuple[int, int],
                 speed: int = 1
                 ) -> None:
        assert game is not None

        sprite: pg.Surface = game.assets.pacgum
        super().__init__(sprite_groups, sprite, maze, pos, speed)

        self.sprite_groups["consumable"].add(self)
        self.collides_with: dict[str, pg.sprite.Group[Entity]] = {
                k: self.sprite_groups[k] for k in ["player"]}

        game.add_to_tree(self)

    def process(self) -> None:
        super().process()

    def on_collide(self, group_name: str) -> None:
        assert game is not None
        self.remove(self.sprite_groups["consumable"])
        print("collided")
        game.remove_from_tree(self)
