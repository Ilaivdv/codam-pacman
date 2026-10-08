from pydantic import BaseModel, PrivateAttr, Field, ConfigDict
import pygame as pg


class GameSettings(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    _display: pg.Surface = PrivateAttr(pg.display.set_mode())
    _resolution: tuple[int, int] = PrivateAttr(Field(
        gt=(0, 0),
        default=pg.display.get_desktop_sizes()[0]))

    @property
    def display(self) -> pg.Surface:
        return self._display

    @property
    def resolution(self) -> tuple[int, int]:
        return self._resolution


settings: GameSettings | None = None
