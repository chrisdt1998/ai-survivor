from core.entity import Component
import pygame


class SpriteComponent(Component):

    def __init__(self, renderer, sprite):
        super()
        self.renderer = renderer
        self.sprite = sprite
        self.renderer.sprites.add(self)

    def on_destroyed(self):
        self.renderer.sprites.remove(self)

    def render(self, delta):
        if self.sprite:
            sprite = pygame.transform.rotate(self.sprite, self.entity.rotation)
            self.renderer.screen.blit(sprite, self.renderer.get_render_pos(self.entity.position))
        else:
            pygame.draw.circle(self.screen, "red", self.renderer.get_render_pos(self.entity.position), 40)
