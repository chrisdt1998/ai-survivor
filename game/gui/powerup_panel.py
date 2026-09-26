from game.gui.gui_element import GUIElement
from core.vector2 import Vector2
from game.gui.gui_text import GUIText
import pygame

class PowerupPanel(GUIElement):

    def __init__(self, position: Vector2, sprite):
        super().__init__(
            position,
            size=Vector2(sprite.get_width(), sprite.get_height()),
            direction="vertical",
            margin=(50, 0, 0, 0),
        )
        self.sprite = sprite

        self.title = GUIText("Bigger Gun", horizontal_alignment="center")
        self.add_child(self.title)
        
        self.description = GUIText("+5 damage", horizontal_alignment="center")
        self.add_child(self.description)

    def render(self, screen: pygame.Surface, delta):
        screen.blit(self.sprite, self.screen_position.to_tuple())
        # self.title.render(screen)

    def on_click(self):
        pass
