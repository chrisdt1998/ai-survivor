from core.vector2 import Vector2
from game.components.visual_component import VisualComponent
import pygame

class SpriteComponent(VisualComponent):

    def __init__(self, renderer, sprite: pygame.Surface, offset=Vector2()):
        super().__init__(renderer)
        self.sprite = sprite
        self.centering_offset = Vector2(
            -self.sprite.get_width() / 2.0,
            -self.sprite.get_height() / 2.0,
        )
        self.local_offset = Vector2()

    def render(self, screen: pygame.Surface):
        sprite = pygame.transform.rotate(self.sprite, self.entity.rotation)
        local_offset = self.local_offset.rotated(self.entity.rotation)
        position = self.to_screen_pos(self.entity.position.add(local_offset)).add(self.centering_offset)
        screen.blit(sprite, position.to_tuple())
