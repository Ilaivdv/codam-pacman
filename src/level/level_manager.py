from src.game import game, settings  # noqa: F401
from src.utils import GameObject
from .level import Level


class LevelManager(GameObject):
    def __init__(self) -> None:
        assert settings is not None
        self._current_level: int = 0
        self._level: Level | None = self.start_next()

    def start_next(self) -> Level:
        assert game is not None and settings is not None
        if self._current_level > 0:
            self.remove_current()

        level = Level(seed=settings.seed + self._current_level)
        game.add_to_tree(level)
        self._current_level += 1
        if self._current_level > settings.level:
            self._current_level = 1
        return level

    def remove_current(self) -> None:
        if self._level is None:
            return
        assert game is not None
        game.remove_from_tree(self._level)
        del self._level
        self._level = None

    def process(self) -> None:
        ...

    @property
    def current_level(self) -> int:
        return self.current_level
