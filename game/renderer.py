from core.level import Level
from core.vector2 import Vector2
from core.entity import Entity
from core.simulation import Simulation
from game.camera import Camera
import pygame


def loadSprite(path) -> pygame.Surface:
    return pygame.image.load("game/assets/textures/" + path).convert_alpha()


class Renderer:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.camera = Camera(self.screen)
        
        self.entities_sprites = {
            "player": loadSprite("manBlue_gun.png"),
        }

        self.tiles_sprites = {
            "dirt_0": loadSprite("tiles/tile_05.png"),
            "dirt_1": loadSprite("tiles/tile_04.png"),
        }
        self.tile_size = self.tiles_sprites["dirt_0"].get_width()

    def render(self, delta: float, simulation: Simulation):
        self.screen.fill((0, 0, 0))

        self.camera.target = simulation.get_entity_by_name("player")
        self.camera.update(delta)
        self.render_level(simulation.level)

        for entity in simulation.entities:
            self.render_entity(entity)

        pygame.display.flip()

    def render_entity(self, entity: Entity):
        if entity.entity_type in self.entities_sprites:
            sprite = self.entities_sprites[entity.entity_type]
            self.screen.blit(sprite, self.get_render_pos(entity.position))
        else:
            pygame.draw.circle(self.screen, "red", self.get_render_pos(entity.position), 40)

    def render_level(self, level: Level):
        for tile_pos in level.tiles:
            tile = level.tiles[tile_pos]
            sprite = self.tiles_sprites[tile.tile_type]
            screen_pos = Vector2(tile_pos[0], tile_pos[1]).mult(self.tile_size)
            self.screen.blit(sprite, self.get_render_pos(screen_pos))
    
    def get_render_pos(self, pos: Vector2):
        return pos.minus(self.camera.position).to_tuple()

