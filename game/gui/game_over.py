from core.vector2 import Vector2
from core.attributes import Attributes
import pygame

class GameOver:
    
    def __init__(self, simulation):
        self.font = pygame.font.SysFont("Arial", 12)

    def render(self, screen: pygame.Surface, delta):
        screen.fill(
            (0, 0, 0, 250),
        )

        font_image = self.font.render("Game Over", True, "white", (0, 0, 0, 0))
        screen.blit(font_image, (50, 50))
