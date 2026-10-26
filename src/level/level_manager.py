from src.game import game, settings  # noqa: F401
from src.utils import GameObject
from .level import Level


class LevelManager(GameObject):
    def __init__(self) -> None:
        assert settings is not None
        self._level: Level | None = None
        self.start_next()

    def start_next(self) -> None:
        assert game is not None and settings is not None
        if game.current_level > 0:
            self.remove_current()

        self._level = Level(seed=settings.seed + game.current_level)
        game.add_to_tree(self._level)
        game.current_level += 1
        if game.current_level > settings.level:
            game.current_level = 1

    def remove_current(self) -> None:
        if self._level is None:
            return
        assert game is not None
        self._level.exit()
        del self._level
        self._level = None

    def process(self) -> None:
        assert game is not None
        if game.is_paused:
            return

        if game.cheat_options["Skip level"]:
            self._level = self.start_next()
            game.cheat_options["Skip level"] = False

    @property
    def current_level(self) -> int:
        return self.current_level
