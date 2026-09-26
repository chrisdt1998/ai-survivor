from game.sprites import Sprites
from game.components.visual_component import VisualComponent
from core.object import ObjectList
from game.tween import Tween
from game.player_controller import PlayerController
from game.gui.gui import GUI
from core.level import Level
from core.vector2 import Vector2
from core.entity import Entity
from core.simulation import Simulation
from core.components.auto_destroy_component import AutoDestroyComponent

from game.camera import Camera
from game.components.sprite_component import SpriteComponent
from game.components.line_component import LineComponent
from game.entities_data import ENTITIES

import pygame

def loadSprite(path) -> pygame.Surface:
    return pygame.image.load("game/assets/textures/" + path).convert_alpha()


class Renderer:
    
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720), flags=pygame.RESIZABLE)

        self.pixel_scale = 10
        self.pixel_size = 16.0 * self.pixel_scale
        self.sprites = Sprites(self.pixel_scale)
        self.camera = Camera(self.screen, self.pixel_size)

        self._visuals: set[VisualComponent] = set()
        self._tweens = ObjectList()
    
    def set_simulation(self, simulation):
        self._visuals.clear()

        self.simulation = simulation
        self.simulation.listen("entity_attacked", self.handle_entity_attack)
        self.simulation.listen("entity_added", self.handle_entity_added)

        self.player = self.simulation.get_entity_by_name("player")
        self.player_controller = PlayerController()

        self.gui = GUI(simulation, self)

    def render(self, delta: float):
        self.screen.fill((0, 0, 0))

        for tween in self._tweens.values():
            tween.update(delta)

        self.camera.target = self.simulation.get_entity_by_name("player")
        self.camera.update(delta)
        self.render_level(self.simulation.level)

        for visual in self._visuals:
            visual.render(self.screen)

        self.gui.render(delta)

        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        delta_time = 0

        while running:
            actions = self.player_controller.get_actions(self.player)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.WINDOWRESIZED:
                    self.camera.set_screen(self.screen, self.pixel_size)

            self.simulation.update(delta_time, actions)
            self.simulation.drain_events()
            self.render(delta_time)

            delta_time = clock.tick(60) / 1000

        pygame.quit()

    def render_level(self, level: Level):
        tile_sprites = {
            "dirt_1": self.sprites.load("grass_1.png"),
            "dirt_0": self.sprites.load("grass_0.png"),
            "dirt_2": self.sprites.load("grass_2.png"),
        }

        for tile_pos in level.tiles:
            tile = level.tiles[tile_pos]
            sprite = tile_sprites[tile.tile_type]
            self.screen.blit(sprite, self.get_render_pos(Vector2(tile_pos[0], tile_pos[1])).to_tuple())
    
    def get_render_pos(self, pos: Vector2):
        return pos.minus(self.camera.position).mult(self.pixel_size)

    def create_tween(self) -> Tween:
        tween = Tween(self)
        self._tweens.add(tween)
        return tween

    def handle_entity_added(self, entity: Entity):
        if entity.entity_type not in ENTITIES:
            return

        entity_data = ENTITIES[entity.entity_type]
        sprite = self.sprites.load(entity_data["sprite"])
        sprite_component = SpriteComponent(self, sprite)
        entity.add_component(sprite_component)

    def handle_entity_attack(self, event):
        if event["source"].entity_type == "player":
            bullet = Entity(Vector2())
            line_component = LineComponent(
                self,
                (255, 218, 115),
                event["source"].position,
                event["target"].position,
            )
            bullet.add_component(line_component)
            bullet.add_component(AutoDestroyComponent(.2))
            self.simulation.add_entity(bullet)

            tween = self.create_tween()
            tween.tween_property(line_component, "width", 20, .02)
            tween.tween_property(line_component, "width", 0, .05)
        
        elif event["source"].entity_type == "enemy":
            sprite = event["source"].get_component(SpriteComponent)
            tween = self.create_tween()
            tween.tween_property(sprite, "local_offset.x", -0.3, .5)
            tween.tween_property(sprite, "local_offset.x", 0.2, .1)
            tween.tween_property(sprite, "local_offset.x", 0, .5)

            bullet = Entity(Vector2())
            line_component = LineComponent(
                self,
                (200, 0, 0),
                event["source"].position,
                event["target"].position,
            )
            bullet.add_component(line_component)
            bullet.add_component(AutoDestroyComponent(.05))
            self.simulation.add_entity(bullet)

            tween = self.create_tween()
            tween.tween_property(
                line_component,
                "width",
                0,
                .2
            )
