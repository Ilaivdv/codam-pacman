import pygame as pg
import os


ASSET_LIST: dict[str, str] = {
        "tileset": "assets/tileset.png",
        "player": "assets/player.png",
        }


class Assets:
    def __init__(self) -> None:
        self._tileset: pg.Surface = pg.image.load(
                ASSET_LIST["tileset"])
        self._player: pg.Surface = pg.image.load(
                ASSET_LIST["player"])

    @classmethod
    def validate_assets(cls) -> Assets:
        for name, path in ASSET_LIST.items():
            if not os.path.exists(path):
                raise FileNotFoundError(f"Invalid asset path for '{name}'")
            elif not os.access(path, os.R_OK):
                raise FileNotFoundError(("No permission to read "
                                         f"asset path for '{name}'"))
            elif not path.endswith(".png"):
                raise ValueError(
                        f"Asset path for '{name}' is not a png")
        return Assets()

    @property
    def tileset(self) -> pg.Surface:
        return self._tileset.convert_alpha()

    @property
    def player(self) -> pg.Surface:
        return self._player.convert_alpha()
