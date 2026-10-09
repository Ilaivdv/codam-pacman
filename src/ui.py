import pygame as pg
from .obj import GameObject
from pydantic import ConfigDict, Field
import sys
from enum import Enum
from pathlib import Path

pg.init()
screen = pg.display.set_mode((500, 500))
screen_rect = screen.get_rect
pg.display.set_caption("Pacman")
mouse = pg.mouse.get_pos()
pg.font.init()
font = pg.font.SysFont("arial", 40)


class Color(Enum):
    WHITE = (255, 255, 255)
    LIGHT = (170, 170, 170)
    DARK = (100, 100, 100)
    BG = (60, 25, 60)


class UIElement(GameObject):
    x: int
    y: int

    def process(self) -> None:
        ...


class Text(UIElement):
    text: str
    color: tuple[int, int, int] = Field(default=Color.WHITE.value)
    font_size: int = Field(default=40)

    def draw(self, screen: pg.Surface,
             font: pg.font.Font, center: bool) -> None:
        surface = font.render(self.text, True, self.color)
        if center:
            rect = surface.get_rect(center=(self.x, self.y))
            screen.blit(surface, rect)
        else:
            screen.blit(surface, (self.x, self.y))


class Button(UIElement):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    width: int
    height: int
    text: str | None

    @property
    def rect(self) -> pg.Rect:
        return pg.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: pg.Surface, mouse: tuple[int, int]) -> None:
        """Draw the text on the button, change color when mouse on the button

        Args:
            screen (_type_): screen
            mouse (_type_): tuple
        """
        bu = self.rect
        if bu.collidepoint(mouse):
            color = Color.LIGHT.value
        else:
            color = Color.DARK.value
        pg.draw.rect(screen, color, bu)
        if self.text:
            text_surface = font.render(self.text, True, Color.WHITE.value)
            text_rect = text_surface.get_rect(center=bu.center)
            screen.blit(text_surface, text_rect)


class Image(UIElement):
    path: str

    def draw(self, screen: pg.Surface) -> None:
        img = pg.image.load(self.path).convert_alpha()
        img_small = pg.transform.scale(img, (500, 1000))
        screen.blit(img_small, (0, 0))


class UI(GameObject):

    @staticmethod
    def process() -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            screen.fill(Color.DARK.value)
            bu = Text(x=250, y=250, text="Game Started!")
            bu.draw(screen, font, center=True)
            pg.display.update()

    def start_menu(self) -> None:
        while True:
            mouse = pg.mouse.get_pos()
            screen.fill(Color.LIGHT.value)
            path = str(Path.cwd().parent) + "/pacman-outfit-0.jpg"
            start_im = Image(x=200, y=200, path=path)

            play_bu = Button(x=300, y=300, width=140, height=50, text="Play")
            quit_bu = Button(x=300, y=380, width=140, height=50, text="Quit")

            start_im.draw(screen)
            play_bu.draw(screen, mouse)
            quit_bu.draw(screen, mouse)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if play_bu.rect.collidepoint(mouse):
                        self.process()
                    if quit_bu.rect.collidepoint(mouse):
                        pg.quit()
                        sys.exit()
            pg.display.update()


UI().start_menu()
