import math
from core.components.attack_component import AttackComponent
import random
from core.entity import Alliance, Entity
from core.attributes import Attributes
from core.vector2 import Vector2
from core.components.enemy_component import EnemyComponent
from core.components.physics_component import PhysicsComponent

class Spawner:

    def __init__(self, simulation):
        self.simulation = simulation

        self.spawn_timer = 0
        self.spawn_delay = 10.0
        self.min_spawn_delay = 0.1
    
    def update(self, delta):
        if self.spawn_timer > 0:
            self.spawn_timer -= delta
            return
        
        self.spawn_enemy()
        self.spawn_timer = self.spawn_delay

        self.spawn_delay -= 0.01
        if self.spawn_delay < self.min_spawn_delay:
            self.spawn_delay = self.min_spawn_delay
    
    def spawn_enemy(self):
        enemy = Entity(name="enemy", entity_type="enemy", position=self.get_random_position())
        enemy.alliance = Alliance.opponent
        enemy.set_attribute(Attributes.health, 10)
        enemy.set_attribute(Attributes.move_speed, 1.0)
        enemy.set_attribute(Attributes.damage, 5)
        enemy.set_attribute(Attributes.attack_range, 2.0)
        enemy.set_attribute(Attributes.attack_speed, 0.5)
        enemy.add_component(PhysicsComponent())
        enemy_component = EnemyComponent()
        enemy.add_component(enemy_component)
        enemy.add_component(AttackComponent())
        self.simulation.add_entity(enemy)
    
    def get_random_position(self):
        if random.random() > 0.5:
            x = self.simulation.map_min.x if random.random() > 0.5 else self.simulation.map_max.x
            y = random.randrange(self.simulation.map_min.y, self.simulation.map_max.y)
        else:
            x = random.randrange(self.simulation.map_min.x, self.simulation.map_max.y)
            y = self.simulation.map_min.y if random.random() > 0.5 else self.simulation.map_max.y
        return Vector2(x, y)
