from game.gui.gui_element import GUIElement
from core.vector2 import Vector2
import pygame

class GUISprite(GUIElement):

    def __init__(self, sprite=None, *args, **kwards):
        super().__init__(
            size=Vector2(sprite.get_width(), sprite.get_height()),
            margin=(50, 0, 0, 0),
            *args, **kwards,
        )
        self.sprite = sprite

    def render(self, screen: pygame.Surface, delta):
        screen.blit(self.sprite, self.screen_position.to_tuple())
