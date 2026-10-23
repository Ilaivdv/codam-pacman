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

        image: pg.Surface = game.assets.enemy
        color: tuple[int, int, int] = random.choice([
            RED,
            PINK,
            CYAN,
            BLUE,
            PURPLE
            ])

        image.fill(color, special_flags=pg.BLEND_MULT)
        self.sprite: SpriteSheet = SpriteSheet(image=image,
                                               frame_duration=80)
        super().__init__(sprite_groups, tile_size, self.sprite.frames[0],
                         maze, pos, speed)
        self.sprite.animations = {
                "idle": [0],
                "moving": [0, 1, 2, 3],
                "idle_vulnerable": [4],
                "moving_vulnerable": [4, 5, 6, 7],
                "dead": [8, 9, 10, 11, 12]
                }
        self.flipped: bool = False

        self.sprite_groups["enemy"].add(self)
        self.collides_with: dict[str, pg.sprite.Group[Entity]] = {
                k: self.sprite_groups[k] for k in ["player"]}
        self.current_state: State = self.ChasingState(self)

        self._slow_down_count: int = 0
        self._slow_down: int = 4
        self.player_pos: pg.Vector2 = player_pos
        self.current_path: list[Direction] = []
        self._path_update_time: int = 1000
        self._path_last_update: int = game.clock.get_time()

        self.current_state.on_enter()
        game.add_to_tree(self)

    def process(self) -> None:
        assert game is not None

        if self.speed == 0:
            self.speed = 1
        self._slow_down_count += 1
        if self._slow_down_count >= self._slow_down:
            self._slow_down_count = 0
            self.speed = 0
        super().process()
        self.current_state.state_process()

        curr_anim: str = "moving"
        match self.move_direction:
            case Direction.NONE:
                curr_anim = "idle"
            case Direction.UP:
                self.rotation = 90
            case Direction.RIGHT:
                self.flipped = False
                self.rotation = 0
            case Direction.DOWN:
                self.rotation = -90
            case Direction.LEFT:
                self.flipped = True
                self.rotation = 0
        self.image = self.sprite.process_animation(curr_anim,
                                                   game.clock.get_time())
        self.image = pg.transform.rotate(self.image, self.rotation)
        self.image = pg.transform.flip(self.image, self.flipped, False)

    def on_collide(self, group_name: str) -> None:
        assert game is not None
        self.remove(self.sprite_groups["consumable"])

    def _get_path(self, reverse: bool = False) -> list[Direction]:

        res: list[Direction] = []

        def get_heuristic(pos: tuple[int, int]) -> int:
            return abs(pos[0] - int(self.player_pos.x)) + abs(
                    pos[1] - int(self.player_pos.y))

        def retrace_path(path: dict[tuple[int, int],
                                    tuple[Direction, int, int] | None],
                         current: tuple[Direction, int, int] | None
                         ) -> list[Direction]:
            assert current is not None
            res.append(current[0])
            if path[current[1:]] is None:
                return res
            return retrace_path(path, path[current[1:]])

        pos: tuple[int, int] = self.current_maze_position

        if reverse:
            for dir in self.get_neighbors():
                if get_heuristic(self._get_maze_cell(dir)
                                 ) > get_heuristic(pos):
                    return [dir]

        # [0] = hueristic, [1], [2] = position in x, y
        open_cells: list[tuple[int, int, int]] = []
        closed_cells: list[tuple[int, int, int]] = []

        # key = cell, value = parent of cell with direction to key
        path: dict[tuple[int, int], tuple[Direction, int, int] | None] = {
                self.current_maze_position: None}

        heapq.heappush(open_cells, (get_heuristic(pos), *pos))
        while len(open_cells):
            curr = heapq.heappop(open_cells)
            heapq.heappush(closed_cells, curr)
            for dir in self.get_neighbors(curr[1:]):
                x, y = self._get_maze_cell(dir, curr[1:])
                h = get_heuristic((x, y))
                if (h, x, y) not in closed_cells:
                    if (h, x, y) not in open_cells:
                        heapq.heappush(open_cells, (h, x, y))
                    path[(x, y)] = (dir, *curr[1:])
                    if pg.Vector2((x, y)) == self.player_pos:
                        return retrace_path(path, (dir, *curr[1:]))

        return [Direction.NONE]

    class ChasingState(State):
        def __init__(self, parent: Enemy) -> None:
            super().__init__(parent)
            self.parent: Enemy = parent

        def on_enter(self) -> None:
            self.parent.current_path = self.parent._get_path()

        def state_process(self) -> None:
            assert game is not None
            self.parent._path_last_update += game.clock.get_time()

            # if len(self.parent.current_path) < 3:
            #     self.parent.current_path = self.parent._get_shortest_path()
            # if self.parent.current_path and \
            #         self.parent.current_path[0] == Direction.NONE and \
            #         self.parent.target_reached():
            #     self.parent.current_path.append(
            #             random.choice(self.parent.get_neighbors()))

            if self.parent._path_last_update >= self.parent._path_update_time \
                    or len(self.parent.current_path) < 1:
                self.parent._path_last_update = 0
                if len(self.parent.current_path) < 4:
                    self.parent.current_path = self.parent._get_path()

            if self.parent.target_reached() and self.parent.current_path:
                self.parent.move_to_pos(self.parent.current_path.pop())

    class RunningState(State):
        def __init__(self, parent: Enemy) -> None:
            super().__init__(parent)
            self.parent: Enemy = parent

        def on_enter(self) -> None:
            self.parent.current_path = self.parent._get_path(True)

        def state_process(self) -> None:
            self.parent.current_path = self.parent._get_path(True)

            if self.parent.target_reached() and self.parent.current_path:
                self.parent.move_to_pos(self.parent.current_path.pop())
