from game.gui.game_over import GameOver
from core.vector2 import Vector2
from game.gui.healthbar import Healthbar

class GUI:
    
    def __init__(self, simulation, renderer):
        self.simulation = simulation
        self.renderer = renderer

        self.player_health = Healthbar(Vector2(5, 5), simulation, simulation.get_entity_by_name("player"))
        self.base_health = Healthbar(Vector2(5, 45), simulation, simulation.get_entity_by_name("homestead"))
        self.game_over = GameOver(simulation)

    def render(self, delta):
        self.player_health.render(self.renderer.screen, delta)
        self.base_health.render(self.renderer.screen, delta)
        # self.game_over.render(self.renderer.screen, delta)
