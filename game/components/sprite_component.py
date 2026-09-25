from core.vector2 import Vector2
from core.entity import Component
import pygame


class SpriteComponent(Component):

    def __init__(self, renderer, sprite: pygame.Surface, offset=Vector2()):
        super()
        self.renderer = renderer
        self.sprite = sprite
        self.offset = Vector2(
            -sprite.get_width() / 2.0,
            -sprite.get_height() / 2.0,
        )
        self.renderer.sprites.add(self)

    def on_destroyed(self):
        self.renderer.sprites.remove(self)

    def render(self, delta):
        sprite = pygame.transform.rotate(self.sprite, self.entity.rotation)
        position = self.renderer.get_render_pos(self.entity.position).add(self.offset)
        self.renderer.screen.blit(sprite, position.to_tuple())
