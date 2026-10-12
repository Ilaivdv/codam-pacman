from pydantic import BaseModel, Field
from src.obj import GameObject
from src.config import Config
import pygame as pg


def start_game(config_file: str) -> None:
    global settings, game

    if game is not None and game.running:
        return
    try:
        pg.init()
        settings = GameSettings.model_validate(Config.parse(config_file))
    except Exception as e:
        print(e)
    else:
        game = Game()
        from src.obj.lose import Lose
        game.add_to_tree(Lose())
        game.start_process()


class Game:
    def __init__(self) -> None:
        self._process_tree: list[GameObject] = []
        self._display: pg.Surface = pg.display.set_mode()
        self._resolution: tuple[int, int] = pg.display.get_desktop_sizes()[0]
        self._clock: pg.time.Clock = pg.time.Clock()
        self._running: bool = False

    def start_process(self) -> None:
        self._running = True
        while self._running:
            for p in self._process_tree:
                p.process()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._running = False

            pg.display.update()
            self._clock.tick(60)

        pg.quit()

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

    @property
    def resolution(self) -> tuple[int, int]:
        return self._resolution

    @property
    def running(self) -> bool:
        return self._running


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
