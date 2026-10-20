from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Self
import pygame as pg


class SpriteSheet(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    image: pg.Surface = Field()
    frame_size: tuple[int, int] = Field(gt=(0, 0), default=(16, 16))
    frames: list[pg.Surface] = Field(default=list())

    animations: dict[str, list[int]] = Field(default_factory=dict)
    animation_finished: bool = False
    current_animation: str = Field(default="")
    current_frame: int = Field(default=0)
    last_frame_update: int = Field(gt=0, default=0)
    frame_duration: int = Field(gt=0, default=80)

    @model_validator(mode="after")
    def _load_frames(self) -> Self:
        w, h = self.image.get_rect().size

        for y in range(0, h, self.frame_size[0]):
            for x in range(0, w, self.frame_size[1]):
                new_frame = pg.Surface(self.frame_size)
                new_frame.blit(self.image, (0, 0), (x, y, *self.frame_size))
                new_frame.set_colorkey((0, 0, 0))
                self.frames.append(new_frame)

        return self

    def process_animation(self, animation: str,
                          current_time: int) -> pg.Surface:
        self.last_frame_update += current_time
        if animation != self.current_animation:
            self.animation_finished = False
            self.current_animation = animation
            self.current_frame = 0

        if self.last_frame_update >= self.frame_duration:
            self.animation_finished = False
            self.last_frame_update = 0
            self.current_frame += 1
            if self.current_frame >= len(
                    self.animations[self.current_animation]):
                self.current_frame = 0

        if self.current_frame + 1 >= len(
                self.animations[self.current_animation]):
            self.animation_finished = True


        return self.frames[self.animations[self.current_animation][
            self.current_frame]]
