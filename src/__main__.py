from src.settings import settings, GameSettings  # noqa: F401
from src.game import Game
import pygame as pg


def main() -> None:
    try:
        pg.init()
        global settings
        settings = GameSettings()

        Game()
    except KeyError as e:
        print(e)


if __name__ == "__main__":
    main()
