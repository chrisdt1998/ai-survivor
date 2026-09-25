from core.components.enemy_component import EnemyComponent
from core.components.physics_component import PhysicsComponent
from core.attributes import Attributes
from core.entity import Alliance
from core.entity import Entity
from random import random
from core.vector2 import Vector2

class Tile:
    tile_type: str

    def __init__(self, tile_type: str):
        self.tile_type = tile_type

class Level:

    def __init__(self, map_min: Vector2, map_max: Vector2):
        self.tiles: dict = {}
        
        dirt_0 = Tile("dirt_0")
        dirt_1 = Tile("dirt_1")

        for x in range(map_min.x, map_max.x):
            for y in range(map_min.y, map_max.y):
                tile = dirt_0 if random() > 0.25 else dirt_1 
                self.set_tile(tile, x, y)

    def update(self, delta):
        pass

    def set_tile(self, tile: Tile, x, y):
        self.tiles[(x, y)] = tile

    def get_tile(self, x, y) -> Tile | None:
        return self.tiles.get((x, y), None)