from pydantic import BaseModel, PrivateAttr, Field, ConfigDict, model_validator
import pygame as pg


class GameSettings(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _display: pg.Surface = PrivateAttr(pg.display.set_mode())
    _resolution: tuple[int, int] = PrivateAttr(Field(
        gt=(0, 0),
        default=pg.display.get_desktop_sizes()[0]))
    # _highscore_filename: str = PrivateAttr()
    # _level: list[dict[str, int]] = PrivateAttr()
    # _lives: int = PrivateAttr(Field(gt=0))
    # _pacgum: int = PrivateAttr(Field(gt=0))
    # _points_per_pacgum: int = PrivateAttr(Field(gt=0))
    # _points_per_super_pacgum: int = PrivateAttr(Field(gt=0))
    # _points_per_ghost: int = PrivateAttr(Field(gt=0))
    # _seed: int = PrivateAttr()
    # _level_max_time: int = PrivateAttr(Field(gt=0))

    # @staticmethod
    # def validate_config(config: dict[str, Any]) -> GameSettings:
    #     return GameSettings.model_validate(config)

    @property
    def display(self) -> pg.Surface:
        return self._display

    @property
    def resolution(self) -> tuple[int, int]:
        return self._resolution
    #
    # @model_validator(mode="after")
    # def post(self) -> None:
    #     print(self.model_dump())


settings: GameSettings | None = None
