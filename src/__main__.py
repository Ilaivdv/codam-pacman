from src.game import Game, GameSettings, game, settings  # noqa: F401
from src.config import Config
import pygame as pg


def main() -> None:
    try:
        pg.init()
        global settings
        settings = GameSettings.model_validate(Config.parse("config.json"))
    except Exception as e:
        print(e)
    else:
        global game
        game = Game()


if __name__ == "__main__":
    main()
