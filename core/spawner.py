from core.components.attack_component import AttackComponent
from core.entity import Alliance, Entity
from core.attributes import Attributes
from core.vector2 import Vector2
from core.components.enemy_component import EnemyComponent
from core.components.physics_component import PhysicsComponent
from core.entities_data import ENTITIES

import random

class Spawner:

    def __init__(self, simulation, create_entity):
        self.simulation = simulation
        self.create_entity = create_entity

        self.spawn_timer = 0
        self.spawn_delay = 10.0
        self.spawn_delay_decrement = 0.0
        self.min_spawn_delay = 0.1
        self.spawn_border_size = 1
    
    def update(self, delta):
        if self.spawn_timer > 0:
            self.spawn_timer -= delta
            return
        
        entity = self.create_entity()
        entity.position = self.get_random_position()
        self.simulation.add_entity(entity)
        self.spawn_timer = self.spawn_delay

        self.spawn_delay -= self.spawn_delay_decrement
        if self.spawn_delay < self.min_spawn_delay:
            self.spawn_delay = self.min_spawn_delay

    def get_random_position(self):
        min_x = self.simulation.map_min.x
        min_y = self.simulation.map_min.y
        max_x = self.simulation.map_max.x
        max_y = self.simulation.map_max.y

        if random.random() > 0.5:
            if random.random() > 0.5:
                x = random.randrange(min_x, min_x + self.spawn_border_size)
            else:
                x = random.randrange(max_x - self.spawn_border_size, max_x)
            y = random.randrange(min_y, max_y)
        else:
            x = random.randrange(min_x, max_x)
            if random.random() > 0.5:
                y = random.randrange(min_y, min_y + self.spawn_border_size)
            else:
                y = random.randrange(max_y - self.spawn_border_size, max_y)
        
        return Vector2(x, y)
