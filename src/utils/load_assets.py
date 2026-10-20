import pygame as pg
import os


ASSET_LIST: dict[str, str] = {
        "tileset": "assets/tileset.png",
        "player": "assets/player.png",
        "pacgum": "assets/pacgum.png",
        "enemy0": "assets/enemy_00.png",
        "enemy1": "assets/enemy_01.png",
        "enemy2": "assets/enemy_02.png",
        "enemy3": "assets/enemy_03.png",
        }


class Assets:
    def __init__(self) -> None:
        self._tileset: pg.Surface = pg.image.load(
                ASSET_LIST["tileset"])
        self._player: pg.Surface = pg.image.load(
                ASSET_LIST["player"])
        self._pacgum: pg.Surface = pg.image.load(
                ASSET_LIST["pacgum"])
        self._enemy0: pg.Surface = pg.image.load(
                ASSET_LIST["enemy0"])
        self._enemy1: pg.Surface = pg.image.load(
                ASSET_LIST["enemy1"])
        self._enemy2: pg.Surface = pg.image.load(
                ASSET_LIST["enemy2"])
        self._enemy3: pg.Surface = pg.image.load(
                ASSET_LIST["enemy3"])

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

    @property
    def pacgum(self) -> pg.Surface:
        return self._pacgum.convert_alpha()

    @property
    def enemy0(self) -> pg.Surface:
        return self._enemy0.convert_alpha()

    @property
    def enemy1(self) -> pg.Surface:
        return self._enemy1.convert_alpha()

    @property
    def enemy2(self) -> pg.Surface:
        return self._enemy2.convert_alpha()

    @property
    def enemy3(self) -> pg.Surface:
        return self._enemy3.convert_alpha()
