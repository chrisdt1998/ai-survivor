import pygame

BASE_TEXTURES_PATH = "game/assets/textures/"

class Sprites:

    def __init__(self, pixel_scale):
        self.pixel_scale = pixel_scale
        self._sprites: dict[str, pygame.Surface] = {}

    def load(self, sprite_path):
        if sprite_path not in self._sprites:
            surface = pygame.image.load(BASE_TEXTURES_PATH + sprite_path).convert_alpha()
            surface = self._scale_surface(surface)
            self._sprites[sprite_path] = surface
        return self._sprites[sprite_path]

    def _scale_surface(self, surface: pygame.Surface):
        width = surface.get_width() * self.pixel_scale
        height = surface.get_height() * self.pixel_scale
        scaled_sprite = pygame.transform.scale(surface, (width, height))
        return scaled_sprite
