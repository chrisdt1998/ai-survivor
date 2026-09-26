from game.components.visual_component import VisualComponent
from core.vector2 import Vector2
import pygame


class LineComponent(VisualComponent):

    def __init__(self, renderer, color, pos_from: Vector2, pos_to: Vector2, width: int = 10):
        super().__init__(renderer)
        self.color = color
        self.pos_from = pos_from
        self.pos_to = pos_to
        self.width = width

    def render(self, screen: pygame.Surface):        
        pygame.draw.line(
            screen,
            self.color,
            self.to_screen_pos(self.pos_from).to_tuple(),
            self.to_screen_pos(self.pos_to).to_tuple(),
            round(self.width)
        )
