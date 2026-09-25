from core.vector2 import Vector2
from core.entity import Component
import pygame


class LineComponent(Component):

    def __init__(self, renderer, color, pos_from: Vector2, pos_to: Vector2):
        super()
        self.renderer = renderer
        self.color = color
        self.pos_from = pos_from
        self.pos_to = pos_to
        self.renderer.sprites.add(self)

    def on_destroyed(self):
        self.renderer.sprites.remove(self)

    def render(self, delta):
        pygame.draw.line(
            self.renderer.screen,
            self.color,
            self.renderer.get_render_pos(self.pos_from).to_tuple(),
            self.renderer.get_render_pos(self.pos_to).to_tuple(),
            10
        )
