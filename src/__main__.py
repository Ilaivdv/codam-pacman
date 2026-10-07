from .config import Config
from .game import Game
import pygame as pg


def main() -> None:
    try:
        pg.init()
        Game(context=Config.parse("config.json"))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
