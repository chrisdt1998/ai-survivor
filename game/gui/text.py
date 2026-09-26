from game.gui.gui_element import GuiElement
from core.vector2 import Vector2
import pygame

class Text(GuiElement):

    fonts = {}

    @staticmethod
    def get_font(font_size):
        if font_size not in Text.fonts:
            Text.fonts[font_size] = pygame.font.SysFont("Arial", font_size)
        return Text.fonts[font_size]

    def __init__(self,
        text="",
        position: Vector2 = Vector2(),
        color=(255,255,255),
        font_size=30,
        horizontal_alignment="start",
    ):
        super().__init__(position, horizontal_sizing="fill")

        self.color = color
        self.font_size = font_size
        self.horizontal_alignment = horizontal_alignment

        self._font_image = None
        self.set_text(text)

    def set_text(self, text):
        self._text = text
        if text:
            font = Text.get_font(self.font_size)
            self._font_image = font.render(self._text, True , self.color)
        else:
            self._font_image = None

    def render(self, screen, delta):
        if self._font_image:
            position = self.screen_position
            if self.horizontal_alignment == "center":
                position.x = position.x + (self.size.x / 2) - (self._font_image.get_width() / 2)
            screen.blit(self._font_image, position.to_tuple())
