from src.config import Config
from typing import Any
import os
import json
from .error import HighscoreError


class Score:
    def __init__(self) -> None:
        self._rank: dict[str, int | Any] = Config.parse_highscore()
        self._current: int = 0
        self._username: str = "UnknownUser"

    @property
    def current(self) -> int:
        return self._current

    @property
    def rank(self) -> dict[str, int | Any]:
        return self._rank

    def set_current(self, score: int) -> None:
        self._current = score

    def add_score(self, score: int) -> None:
        self._current += score

    def set_username(self, name: str) -> None:
        self._username = name

    def update_rank(self) -> None:
        self._rank[self._username] = self._current

    def init_current(self) -> None:
        self.set_current(0)
        self.set_username("Unknown User")

    def update_file(self) -> None:
        file_path: str = os.path.expanduser("~/.local/share/highscore.json")
        if not self.rank or len(self.rank) == 1:
            with open(file_path, "w") as f:
                json.dump(self.rank, f)
            return
        else:
            try:
                top_10: dict[str, int] = dict(sorted(self.rank.items(),
                                              key=lambda x: x[1],
                                              reverse=True)[:10])
                with open(file_path, "w") as f:
                    json.dump(top_10, f)
            except HighscoreError as e:
                print(e)
