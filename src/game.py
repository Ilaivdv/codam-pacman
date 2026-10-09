from pydantic import BaseModel, Field
from src.obj import GameObject
import pygame as pg


class Game:
    def __init__(self) -> None:
        self._process_tree: list[GameObject] = []
        self._display: pg.Surface = pg.display.set_mode()
        self._resolution: tuple[int, int] = pg.display.get_desktop_sizes()[0]
        self._clock: pg.time.Clock = pg.time.Clock()

        self._start_process()

    def _start_process(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False

            for p in self._process_tree:
                p.process()

            self._clock.tick(60)

    def add_to_tree(self, obj: GameObject) -> None:
        self._process_tree.append(obj)

    def remove_from_tree(self, obj: GameObject) -> None:
        self._process_tree.remove(obj)

    @property
    def process_tree(self) -> list[GameObject]:
        return self._process_tree

    @property
    def display(self) -> pg.Surface:
        return self._display


class GameSettings(BaseModel):
    highscore_filename: str = Field(frozen=True)
    level: list[dict[str, int]] = Field(frozen=True)
    lives: int = Field(gt=0, frozen=True)
    pacgum: int = Field(gt=0, frozen=True)
    points_per_pacgum: int = Field(gt=0, frozen=True)
    points_per_super_pacgum: int = Field(gt=0, frozen=True)
    points_per_ghost: int = Field(gt=0, frozen=True)
    seed: int = Field(frozen=True)
    level_max_time: int = Field(gt=0, frozen=True)


settings: GameSettings | None = None
game: Game | None = None
