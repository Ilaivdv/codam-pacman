from src.utils.colors import RED, PINK, CYAN, BLUE, PURPLE
from src.obj.entity import Entity, Direction
from src.utils import SpriteSheet, State
from src.game import game
import pygame as pg
import random
import heapq


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
        self._get_neighbors()

        game.add_to_tree(self)

    def process(self) -> None:
        super().process()
        self.current_state.state_process()

    def on_collide(self, group_name: str) -> None:
        assert game is not None
        self.remove(self.sprite_groups["consumable"])

    def _get_neighbors(self) -> list[Direction]:
        res: list[Direction] = []
        x, y = self.current_maze_position
        for i in Direction:
            if i == Direction.NONE:
                continue
            if not self.maze[y][x] & i:
                res.append(i)
        return res
    
    def _get_shortest(self) -> Direction:
        x, y = self.current_maze_position
        heuristic = abs(x - self.player_pos.x) + abs(y - self.player_pos.y) 
        visited_cells = [[False for _ in range(self.maze[1])]
                         for _ in range(self.maze)]
        open_list = []
        heapq.heappush(open_list, (0.0, x, y))

        while len(open_list) > 0:
            ...

        return Direction.NONE

    class ChasingState(State):
        def __init__(self, parent: Enemy) -> None:
            super().__init__(parent)
            self.parent: Enemy = parent

        def on_enter(self) -> None:
            pass

        def state_process(self) -> None:
            # self.parent.move_to_pos(self.parent._get_shortest(self.parent._get_neighbors()))
            ...

    class RunningState(State):
        def __init__(self, parent: Enemy) -> None:
            super().__init__(parent)

        def on_enter(self) -> None:
            pass

        def state_process(self) -> None:
            ...
