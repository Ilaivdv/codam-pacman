from pydantic import BaseModel, ConfigDict
from src.obj import GameObject
import pygame as pg


class Process(GameObject):
    def __init__(self) -> None:
        self.tree: list[GameObject] = []
        self.clock: pg.time.Clock = pg.time.Clock()

        self._start_process_loop()

    def _start_process_loop(self) -> None:
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    running = False

            self.process()
            for p in self.tree:
                p.process()

            self.clock.tick(60)

    def process(self) -> None:
        ...


class Game(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    process: Process = Process()

    def add_to_tree(self, obj: GameObject) -> None:
        self.process.tree.append(obj)

    def remove_from_tree(self, obj: GameObject) -> None:
        self.process.tree.remove(obj)
