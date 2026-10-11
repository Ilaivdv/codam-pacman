from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Self
import pygame as pg


class Tileset(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    image: pg.Surface = Field()
    tile_size: tuple[int, int] = Field(gt=(0, 0), default=(16, 16))
    margin: int = Field(ge=0, default=0)
    tiles: list[pg.Surface] = Field(default=list())

    @model_validator(mode="after")
    def load_tiles(self) -> Self:
        w, h = self.image.get_rect().size

        for x in range(0, w, self.tile_size[0]):
            for y in range(0, h, self.tile_size[1]):
                new_tile = pg.Surface(self.tile_size).convert()
                new_tile.blit(self.image, (0, 0), (x, y, *self.tile_size))
                new_tile = pg.transform.flip(new_tile, True, True)
                self.tiles.append(new_tile)

        return self


class Tilemap:
    ...
