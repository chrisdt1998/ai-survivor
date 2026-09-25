from core.vector2 import Vector2
from game.gui.healthbar import Healthbar

class GUI:
    
    def __init__(self, simulation, renderer):
        self.simulation = simulation
        self.renderer = renderer

        self.player_health = Healthbar(Vector2(5, 5))
        self.base_health = Healthbar(Vector2(205, 5))
    
    def render(self, delta):
        self.player_health.render(self.renderer.screen, delta)
        self.base_health.render(self.renderer.screen, delta)
