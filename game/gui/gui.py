from game.gui.attributes_list import AttributesList
from core.vector2 import Vector2

from game.gui.gui_element import GUIElement
from game.gui.powerup_panel import PowerupPanel
from game.gui.game_over import GameOver
from game.gui.healthbar import Healthbar

class GUI:
    
    def __init__(self, simulation, renderer):
        self.simulation = simulation
        self.renderer = renderer

        self.root = GUIElement(direction="unset")

        player_health = Healthbar(Vector2(5, 5), simulation, simulation.get_entity_by_name("player"))
        self.root.add_child(player_health)

        base_health = Healthbar(Vector2(5, 45), simulation, simulation.get_entity_by_name("homestead"))
        self.root.add_child(base_health)

        attributes_list = AttributesList(Vector2(10, 100), simulation, simulation.get_entity_by_name("player"))
        self.root.add_child(attributes_list)

    
        # self.game_over = GameOver(simulation)

        # self.powerups_container = GUIElement(direction="horizontal")
        # self.root.add_child(self.powerups_container)
        # for i in range(3):
        #     powerup_panel = PowerupPanel(Vector2(10, 10), renderer.sprites.load("gui/powerup_panel.png"))
        #     self.powerups_container.add_child(powerup_panel)

    def render(self, delta):
        self.root._render(self.renderer.screen, delta)
