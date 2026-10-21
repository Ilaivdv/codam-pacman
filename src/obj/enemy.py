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
    
    def _get_shortest_path(self) -> list[Direction]:

        res: list[Direction] = []

        def get_heuristic(pos: tuple[int, int]) -> int:
            return abs(pos[0] - int(self.player_pos.x)) + abs(
                    pos[1] - int(self.player_pos.y))

        def retrace_path(path: dict[tuple[int, int], tuple[int, int] | None],
                         current: tuple[int, int]) -> list[Direction]:
            res.insert(0, current)
            if path[current] is None:
                return res
            return retrace_path(path, path[current])

        pos: tuple[int, int] = self.current_maze_position
        # [0] = hueristic, [1], [2] = position in x, y
        open_cells: list[tuple[int, int, int]] = []
        closed_cells: list[tuple[int, int, int]] = []

        # key = cell, value = parent of cell
        path: dict[tuple[int, int], tuple[int, int] | None] = {
                self.current_maze_position: None
                }

        heapq.heappush(open_cells, (get_heuristic(pos), *pos))
        while len(open_cells):
            curr = heapq.heappop(open_cells)
            # print(self.player_pos, curr)
            if pg.Vector2(curr[1:]) == self.player_pos:
                print(f"player found at {curr[1:]}")
                return retrace_path(path, curr[1:])
            heapq.heappush(closed_cells, curr)
            for dir in self._get_neighbors(curr[1:]):
                x, y = self._get_maze_cell(dir, curr[1:])
                h = get_heuristic((x, y))
                if (h, x, y) not in closed_cells:
                    if (h, x, y) not in open_cells:
                        heapq.heappush(open_cells, (h, x, y))
                    path[(x, y)] = curr[1:]
        
        # game.remove_from_tree(self)
        print(path.keys())
        return [Direction.NONE]

        # visited_cells: list[list[bool]] = [[False for _ in range(self.maze[1])]
        #                                    for _ in range(self.maze)]
        # open_cells: list[tuple[float, int, int]] = []
        # x, y = self.current_maze_position
        # heapq.heappush(open_cells, (0, x, y))
        #
        # while len(open_cells) > 0:
        #     cell = heapq.heappop(open_cells)
        #     # starting at path[2] to convert x, y position to row, col
        #     i: int = cell[2]
        #     j: int = cell[1]
        #     visited_cells[i][j] = True
        #
        #     directions = self._get_neighbors((j, i))
        #     for dir in directions:
        #         new_j, new_i = self._get_maze_cell(dir)
        #
        #         # TODO Check if at destination
        #         if not visited_cells[i][j]:
        #             new_f: int = get_heuristic((new_j, new_i))
        #
        #             if cell[0] > new_f:
        #                 heapq.heappush(open_cells, (new_f, j, i))
        #
        # return Direction.NONE

    class ChasingState(State):
        def __init__(self, parent: Enemy) -> None:
            super().__init__(parent)
            self.parent: Enemy = parent

        def on_enter(self) -> None:
            pass

        def state_process(self) -> None:
            # self.parent.move_to_pos(self.parent._get_shortest(self.parent._get_neighbors()))
            print(self.parent._get_shortest_path())
            ...

    class RunningState(State):
        def __init__(self, parent: Enemy) -> None:
            super().__init__(parent)

        def on_enter(self) -> None:
            pass

        def state_process(self) -> None:
            ...
