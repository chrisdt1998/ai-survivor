from core.vector2 import Vector2
from game.gui.gui_element import GUIElement
import pygame

class GUIPanel(GUIElement):

    def __init__(
        self,
        color=(255, 255, 255),
        size=Vector2(30, 30),
        *args,
        **kwards
    ):
        super().__init__(
            size=size,
            margin=(50, 0, 0, 0),
            *args, **kwards,
        )
        self.color = color

    def render(self, screen: pygame.Surface, delta):
        screen.fill(
            self.color,
            (self.screen_position.x, self.screen_position.y, self.size.x, self.size.y),
        )
