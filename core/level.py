from random import random
from core.vector2 import Vector2

class Tile:
    tile_type: str

    def __init__(self, tile_type: str):
        self.tile_type = tile_type

class Level:
    
    tiles: dict = {}

    def __init__(self):
        map_size = 10

        dirt_0 = Tile("dirt_0")
        dirt_1 = Tile("dirt_1")

        for x in range(-map_size, map_size + 1):
            for y in range(-map_size, map_size + 1):
                tile = dirt_0 if random() > 0.25 else dirt_1 
                self.set_tile(tile, x, y)

    def set_tile(self, tile: Tile, x, y):
        self.tiles[(x, y)] = tile

    def get_tile(self, x, y) -> Tile | None:
        return self.tiles.get((x, y), None)