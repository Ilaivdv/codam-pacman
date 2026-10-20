from src.utils.colors import RED, PINK, CYAN, BLUE, PURPLE
from src.utils import SpriteSheet, State
from src.obj.entity import Entity
from src.game import game
import pygame as pg
import random


class Enemy(Entity):
    def __init__(self,
                 sprite_groups: dict[str, pg.sprite.Group[Entity]],
                 tile_size: tuple[int, int],
                 maze: list[list[int]],
                 pos: tuple[int, int],
                 player_pos: pg.Vector2,
                 speed: int = 1,
                 ) -> None:
        assert game is not None

        image: pg.Surface = game.assets.enemy1
        # match variant:
        #     case 0:
        #         image = game.assets.enemy0
        #     case 1:
        #         image = game.assets.enemy1
        #     case 2:
        #         image = game.assets.enemy2
        #     case 3:
        #         image = game.assets.enemy3
        #     case _:
        #         image = game.assets.enemy0

        color: tuple[int, int, int] = random.choice([
            RED,
            PINK,
            CYAN,
            BLUE,
            PURPLE
            ])

        image.fill(color, special_flags=pg.BLEND_MULT)
        self.sprite: SpriteSheet = SpriteSheet(image=image)
        super().__init__(sprite_groups, tile_size, self.sprite.frames[0],
                         maze, pos, speed)
        self.sprite_groups["enemy"].add(self)
        self.collides_with: dict[str, pg.sprite.Group[Entity]] = {
                k: self.sprite_groups[k] for k in ["player"]}
        self.current_state: State = self.ChasingState(self)

        self.player_pos: pg.Vector2 = player_pos

        game.add_to_tree(self)

    def process(self) -> None:
        super().process()
        self.current_state.state_process()

    def on_collide(self, group_name: str) -> None:
        assert game is not None
        self.remove(self.sprite_groups["consumable"])

    class ChasingState(State):
        def on_enter(self) -> None:
            pass

        def state_process(self) -> None:
            ...

    class RunningState(State):
        def on_enter(self) -> None:
            pass

        def state_process(self) -> None:
            ...
