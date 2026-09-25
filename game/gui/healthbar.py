from core.attributes import Attributes
import pygame

class Healthbar:
    
    def __init__(self, position, simulation, entity):
        self.font = pygame.font.SysFont("Arial", 30)

        self.position = position
        self.entity = entity
        self.height = 30
        self.width = 100
        self.health_width = self.width
        self.current_health = entity.get_attribute(Attributes.health)

        simulation.listen("attribute_changed", self.handle_attribute_changed)

    def render(self, screen: pygame.Surface, delta):
        screen.fill(
            (100, 100, 100),
            (self.position.x, self.position.y, self.width, self.height),
        )
        screen.fill(
            (255, 255, 255),
            (self.position.x, self.position.y, self.health_width, self.height),
        )

        font_image = self.font.render(str(self.current_health), True , "white")
        screen.blit(font_image, (self.position.x + self.width + 5, self.position.y))

    def handle_attribute_changed(self, event):
        target = event["entity"]
        if target == self.entity:
            max_health = target.get_attribute(Attributes.max_health)
            self.current_health = target.get_attribute(Attributes.health)
            self.health_width = self.width * (self.current_health / max_health)