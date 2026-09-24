from game.camera import Camera
from core.entity import Entity
from core.simulation import Simulation
import pygame

class Renderer:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.camera = Camera()

    def render(self, simulation: Simulation):
        self.screen.fill((0, 0, 0))

        for entity in simulation.entities:
            self.render_entity(entity)

        pygame.display.flip()

    def render_entity(self, entity: Entity):
        render_pos = entity.position.minus(self.camera.position)
        pygame.draw.circle(self.screen, "red", render_pos.to_tuple(), 40)


