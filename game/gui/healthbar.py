import pygame

class Healthbar:
    
    def __init__(self, position):
        self.position = position
        self.width = 100
        self.height = 30
        print((self.position.x, self.position.y, self.position.x + self.width, self.position.y + self.height))

    def render(self, screen: pygame.Surface, delta):
        print(self.height)
        screen.fill(
            (100, 100, 100),
            (self.position.x, self.position.y, self.position.x + self.width, self.position.y + self.height),
        )
