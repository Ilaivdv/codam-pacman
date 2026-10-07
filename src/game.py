from pydantic import BaseModel, Field, ConfigDict
from typing import Any
from obj import GameObject
import pygame as pg


class Process(GameObject):
    def __init__(self) -> None:
        self.tree: list[GameObject] = []
        self.clock: pg.time.Clock = pg.time.Clock()
        self._start_process_loop()

    def _start_process_loop(self) -> None:
        ...
        # while True:
        #     # for event in pg.event.get():
        #     #     if event.type == pg.QUIT:
        #     #         pg.quit()
        #
        #     self.process()
        #     for p in self.tree:
        #         p.process()
        #
        #     self.clock.tick(60)

    def process(self) -> None:
        ...


class Context(BaseModel):
    highscore_filename: str
    level: list[dict[str, int]]
    lives: int = Field(gt=0)
    pacgum: int = Field(gt=0)
    points_per_pacgum: int = Field(gt=0)
    points_per_super_pacgum: int = Field(gt=0)
    points_per_ghost: int = Field(gt=0)
    seed: int
    level_max_time: int = Field(gt=0)


class Game(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    process: Process = Process()
    context: Context

    @staticmethod
    def validate_config(config: dict[str, Any]) -> Context:
        return Context.model_validate(config)

    def add_to_tree(self, obj: GameObject) -> None:
        self.process.tree.append(obj)

    def remove_from_tree(self, obj: GameObject) -> None:
        self.process.tree.remove(obj)
