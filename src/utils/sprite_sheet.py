from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Self
import pygame as pg


class SpriteSheet(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    image: pg.Surface = Field()
    frame_size: tuple[int, int] = Field(gt=(0, 0), default=(16, 16))
    frames: list[pg.Surface] = Field(default=list())

    @model_validator(mode="after")
    def _load_frames(self) -> Self:
        w, h = self.image.get_rect().size

        for x in range(0, w, self.frame_size[0]):
            for y in range(0, h, self.frame_size[1]):
                new_tile = pg.Surface(self.frame_size).convert()
                new_tile.blit(self.image, (0, 0), (x, y, *self.frame_size))
                new_tile = pg.transform.flip(new_tile, True, True)
                self.frames.append(new_tile)

        return self
