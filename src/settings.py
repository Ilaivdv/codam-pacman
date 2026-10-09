from pydantic import (BaseModel, PrivateAttr, Field,
                      ConfigDict, model_validator)
from typing import Self
import pygame as pg
from src.config import Config


class GameSettings(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    display: pg.Surface = pg.display.set_mode()
    resolution: tuple[int, int] = Field(
            gt=(0, 0),
            default=pg.display.get_desktop_sizes()[0])

    _highscore_filename: str = PrivateAttr()
    _level: list[dict[str, int]] = PrivateAttr()
    _lives: int = PrivateAttr(Field(gt=0))
    _pacgum: int = PrivateAttr(Field(gt=0))
    _points_per_pacgum: int = PrivateAttr(Field(gt=0))
    _points_per_super_pacgum: int = PrivateAttr(Field(gt=0))
    _points_per_ghost: int = PrivateAttr(Field(gt=0))
    _seed: int = PrivateAttr()
    _level_max_time: int = PrivateAttr(Field(gt=0))

    @model_validator(mode="after")
    def validate_config(self) -> Self:
        config = {f"_{k}": v for k, v in Config.parse("config.json").items()}
        model_dump = self.model_dump()
        for k, v in config.items():
            model_dump[k] = v

        return self


settings: GameSettings | None = None
