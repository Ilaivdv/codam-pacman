from src.settings import settings, GameSettings  # noqa: F401
from src.config import Config
from src.game import Game
import pygame as pg


def main() -> None:
    try:
        pg.init()
        global settings
        settings = GameSettings.model_validate(Config.parse("config.json"))
        Game()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
