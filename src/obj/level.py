from mazegenerator import MazeGenerator  # type: ignore
from src.obj import GameObject


class Level(GameObject):
    mazegen: MazeGenerator = MazeGenerator()

    def process(self) -> None:
        ...
