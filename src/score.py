from src.config import Config
from typing import Any
import os
import json
from .error import HighscoreError


class Score:
    """ Game's score handler, saves scores to user's local highscore.json. """

    def __init__(self) -> None:
        """ Initializes Score class. """

        self._rank: dict[str, int | Any] = Config.parse_highscore()
        self._current: int = 0
        self._username: str = "UnknownUser"

    @property
    def current(self) -> int:
        """ Returns protected `_current` variable. """
        return self._current

    @property
    def rank(self) -> dict[str, int | Any]:
        """ Returns protected `_rank` variable. """
        return self._rank

    def set_current(self, score: int) -> None:
        """ Sets protected `_current` variable. """
        self._current = score

    def add_score(self, score: int) -> None:
        """ Adds to protected `_current` variable. """
        self._current += score

    def set_username(self, name: str) -> None:
        """ Sets protected `_username` variable. """
        self._username = name

    def update_rank(self) -> None:
        """ Updates protected `_rank` variable. """
        self._rank[self._username] = self.current

    def init_current(self) -> None:
        """ Initializes current user. """
        self.set_current(0)
        self.set_username("Unknown User")

    def update_file(self) -> None:
        """ Updates user's local highscore.json with new score. """

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
