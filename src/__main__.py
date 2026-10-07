import pygame as pg
from .game import Game


def main() -> None:
    try:
        pg.init()
        Game()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
