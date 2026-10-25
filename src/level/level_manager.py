from src.game import game, settings  # noqa: F401
from src.utils import GameObject
from .level import Level
# import pygame as pg


class LevelManager(GameObject):
    def __init__(self) -> None:

        self._current_level: int = 0
        self._level: Level

    def start_next_level(self) -> None:
        assert game is not None and settings is not None

        if self._level:
            game.remove_from_tree(self._level)
            del self._level

        self._level = Level(seed=settings.seed + self._current_level)
        game.add_to_tree(self._level)
        self._current_level += 1
        if self._current_level > settings.level:
            self._current_level = 0

    def process(self) -> None:
        ...

    @property
    def current_level(self) -> int:
        return self.current_level
