import pygame as pg


def main() -> None:
    try:
        pg.init()
    except KeyError as e:
        print(e)


if __name__ == "__main__":
    main()
