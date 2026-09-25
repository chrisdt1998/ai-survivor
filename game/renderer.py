from game.gui.gui import GUI
from core.level import Level
from core.vector2 import Vector2
from core.entity import Entity
from core.simulation import Simulation
from core.components.auto_destroy_component import AutoDestroyComponent

from game.camera import Camera
from game.components.sprite_component import SpriteComponent
from game.components.line_component import LineComponent
import pygame


def loadSprite(path) -> pygame.Surface:
    return pygame.image.load("game/assets/textures/" + path).convert_alpha()


class Renderer:
    
    def __init__(self, simulation: Simulation):
        self.screen = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE)
        self.simulation = simulation
        self.sprites = set()
        self.gui = GUI(simulation, self)

        self.entities_sprites = {
            "player": loadSprite("manBlue_gun.png"),
            "enemy": loadSprite("zombie1_hold.png"),
            "homestead": loadSprite("tiles/tile_156.png"),
        }

        self.tiles_sprites = {
            "dirt_0": loadSprite("tiles/tile_05.png"),
            "dirt_1": loadSprite("tiles/tile_04.png"),
        }
        self.pixel_size = self.tiles_sprites["dirt_0"].get_width()
        self.camera = Camera(self.screen, self.pixel_size)

        self.simulation.listen("entity_attacked", self.handle_entity_attack)
        self.simulation.listen("entity_added", self.handle_entity_added)

    def render(self, delta: float):
        self.screen.fill((0, 0, 0))

        self.camera.target = self.simulation.get_entity_by_name("player")
        self.camera.update(delta)
        self.render_level(self.simulation.level)

        for sprite in self.sprites:
            sprite.render(delta)

        self.gui.render(delta)

        pygame.display.flip()

    def render_level(self, level: Level):
        for tile_pos in level.tiles:
            tile = level.tiles[tile_pos]
            sprite = self.tiles_sprites[tile.tile_type]
            self.screen.blit(sprite, self.get_render_pos(Vector2(tile_pos[0], tile_pos[1])))
    
    def get_render_pos(self, pos: Vector2):
        return pos.minus(self.camera.position).mult(self.pixel_size).to_tuple()

    def handle_entity_added(self, entity: Entity):
        if entity.entity_type in self.entities_sprites:
            sprite = self.entities_sprites[entity.entity_type]
            sprite_component = SpriteComponent(self, sprite)
            entity.add_component(sprite_component)

    def handle_entity_attack(self, event):
        if event["source"].name == "player":
            bullet = Entity(Vector2())
            line_component = LineComponent(
                self,
                event["source"].position,
                event["target"].position,
            )
            bullet.add_component(line_component)
            bullet.add_component(AutoDestroyComponent(.05))
            self.simulation.add_entity(bullet)
