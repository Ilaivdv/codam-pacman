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
    
    def _get_shortest(self) -> Direction:

        def get_heuristic(pos: tuple[int, int]) -> int:
            return abs(pos[0] - int(self.player_pos.x)) + abs(
                    pos[1] - int(self.player_pos.y))

        visited_cells: list[list[bool]] = [[False for _ in range(self.maze[1])]
                                           for _ in range(self.maze)]
        open_cells: list[tuple[float, int, int]] = []
        x, y = self.current_maze_position
        heapq.heappush(open_cells, (0, x, y))

        while len(open_cells) > 0:
            cell = heapq.heappop(open_cells)
            # starting at path[2] to convert x, y position to row, col
            i: int = cell[2]
            j: int = cell[1]
            visited_cells[i][j] = True

            directions = self._get_neighbors((j, i))
            for dir in directions:
                new_j, new_i = self._get_maze_cell(dir)
                
                # TODO Check if at destination
                if not visited_cells[i][j]:
                    new_f: int = get_heuristic((new_j, new_i))

                    if cell[0] > new_f:
                        heapq.heappush(open_cells, (new_f, j, i))

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
