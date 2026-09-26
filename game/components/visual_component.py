from core.vector2 import Vector2
from core.entity import Component
import pygame


class VisualComponent(Component):

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer
        self.renderer._visuals.add(self)

    def on_destroyed(self):
        self.renderer._visuals.remove(self)

    def to_screen_pos(self, pos: Vector2):
        return pos.minus(self.renderer.camera.position).mult(self.renderer.pixel_size)

    def render(self, screen: pygame.Surface):
        pass