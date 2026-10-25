from .entity import Entity
from src.game import game
import pygame as pg


class Consumable(Entity):
    def __init__(self,
                 sprite_groups: dict[str, pg.sprite.Group[Entity]],
                 tile_size: tuple[int, int],
                 maze: list[list[int]],
                 pos: tuple[int, int],
                 speed: int = 1,
                 is_super: bool = False
                 ) -> None:
        assert game is not None
        self.is_super: bool = is_super

        sprite: pg.Surface = game.assets.super_pacgum if self.is_super \
            else game.assets.pacgum
        super().__init__(sprite_groups, tile_size, sprite, maze, pos, speed)

        self.sprite_groups["consumable"].add(self)
        self.collides_with: dict[str, pg.sprite.Group[Entity]] = {
                k: self.sprite_groups[k] for k in ["player"]}

        game.add_to_tree(self)

    def process(self) -> None:
        assert game is not None

        super().process()

    def on_collide(self, group_name: str) -> None:
        assert game is not None
        self.remove(self.sprite_groups["consumable"])
        if self.is_super:
            game.player_is_super = True
            game.super_elapsed_time = 0

        game.remove_from_tree(self)
