from typing import Any


class Error(Exception):
    def __init__(self, *args: Any, msg: str):
        super().__init__(*args)
        self.msg = msg


class ConfigError(Error):
    def __init__(self, *args: Any, msg: str):
        if msg is None:
            print("An error occured with conguration.")
        super().__init__(*args, msg=msg)


class GameError(Error):
    def __init__(self, *args: Any, msg: str):
        if msg is None:
            print("An error occured with game.")
        super().__init__(*args, msg=msg)


class UiError(Error):
    def __init__(self, *args: Any, msg: str):
        if msg is None:
            print("An error occured with UI.")
        super().__init__(*args, msg=msg)


class HighscoreError(Error):
    def __init__(self, *args: Any, msg: str):
        if msg is None:
            print("An error occured with UI.")
        super().__init__(*args, msg=msg)
