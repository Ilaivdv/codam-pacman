from src.obj.entity import Entity, Direction
from src.utils import SpriteSheet
from src.game import game
import pygame as pg


class Enemy(Entity):
    def __init__(self,
                 sprite_groups: dict[str, pg.sprite.Group[Entity]],
                 tile_size: tuple[int, int],
                 maze: list[list[int]],
                 pos: tuple[int, int],
                 speed: int = 1,
                 variant: int = 0
                 ) -> None:
        assert game is not None

        image: pg.Surface
        match variant:
            case 0:
                image = game.assets.enemy0
            case 1:
                image = game.assets.enemy1
            case 2:
                image = game.assets.enemy2
            case 3:
                image = game.assets.enemy3
            case _:
                image = game.assets.enemy0

        self.sprite: SpriteSheet = SpriteSheet(image=image)
        super().__init__(sprite_groups, tile_size,
                         self.sprite.frames[0], maze,
                         pos, speed)

        self.sprite_groups["enemy"].add(self)
        self.collides_with: dict[str, pg.sprite.Group[Entity]] = {
                k: self.sprite_groups[k] for k in ["player"]}

        game.add_to_tree(self)

    def process(self) -> None:
        super().process()

    def on_collide(self, group_name: str) -> None:
        assert game is not None
        self.remove(self.sprite_groups["consumable"])
        print("enemy collision")
