from core.components.health_regen_component import HealthRegenComponent
from collections import defaultdict
from math import inf
import random

from core.vector2 import Vector2
from core.level import Level
from core.entity import Entity, Alliance
from core.attributes import Attributes
from core.actions.action import Action
from core.spawner import Spawner
from core.entities_data import ENTITIES

from core.components.attack_component import AttackComponent
from core.components.physics_component import PhysicsComponent
from core.components.powerup_picker_component import PowerupPickerComponent
from core.components.powerup_component import PowerupComponent
from core.components.enemy_component import EnemyComponent

FIXED_DT = 1.0 / 30

class Simulation:

    event_handlers = defaultdict(list)
    event_queue = []

    def __init__(self):
        self.entities: dict[int, Entity] = {}
        self.entity_next_id: int = 0
        
        self.entities_to_remove: list[int] = []
        self.entities_to_add: list[Entity] = []
    
        self.map_min = Vector2(-10, -10)
        self.map_max = Vector2(10, 10)
        self.level = Level(self.map_min, self.map_max)

        self.game_duration = 0
        
        self.enemies_spawner = Spawner(self, self.create_enemy)
        self.enemies_spawner.spawn_delay = 5.0
        self.enemies_spawner.spawn_delay_decrement = 0.25

        self.powerup_spawner = Spawner(self, self.create_powerup)
        self.powerup_spawner.spawn_border_size = 5
        self.powerup_spawner.spawn_delay = 5.0

        self.homestead = Entity(name="homestead", entity_type="homestead", position=Vector2(0, 0))
        self.homestead.alliance = Alliance.ally
        self.homestead.set_data(ENTITIES["homestead"])
        self.homestead.add_component(PhysicsComponent())
        self.homestead.add_component(HealthRegenComponent())
        self.add_entity(self.homestead)

        player = Entity(name="player", entity_type="player", position=Vector2(3, 0))
        player.alliance = Alliance.ally
        player.set_data(ENTITIES["player"])
        player.add_component(PhysicsComponent())
        player.add_component(AttackComponent())
        player.add_component(PowerupPickerComponent())
        player.add_component(HealthRegenComponent())
        self.add_entity(player)

    def listen(self, event_type, callback):
        self.event_handlers[event_type].append(callback)

    def emit(self, event_type, data):
        self.event_queue.append((event_type, data))
        # print(f"[Event] {event_type}")
    
    def drain_events(self):
        for (event_type, data) in self.event_queue:
            callbacks = self.event_handlers[event_type]
            for cb in callbacks:
                cb(data)
        self.event_queue.clear()

    def update(self, delta: float, actions: list[Action] = []):
        self.game_duration += delta

        for action in actions:
            action.apply(self, delta)
        
        self.enemies_spawner.update(delta)
        self.powerup_spawner.update(delta)
        self.level.update(delta)

        for entity in self.entities.values():
            entity.update(delta)
        
        for entity_id in self.entities_to_remove:
            self.entities.pop(entity_id)
        self.entities_to_remove.clear()

    def add_entity(self, entity: Entity):
        if entity.id != -1:
            # print("Entity already added")
            return
            
        self.entity_next_id += 1
        entity.id = self.entity_next_id
        entity.simulation = self
        self.entities[entity.id] = entity
        entity.setup()
        self.emit("entity_added", entity)

    def _destroy_entity(self, entity: Entity):
        # Defer entity removal to avoid issues during
        # entities loop update
        entity.on_destroyed()
        self.entities_to_remove.append(entity.id)
        self.emit("entity_destroyed", entity)
    
    def get_entity(self, entity_id: int) -> Entity:
        return self.entities[entity_id]
    
    def get_entity_by_name(self, entity_name: str) -> Entity:
        for entity in self.entities.values():
            if entity.name == entity_name:
                return entity
        return None

    def get_closest(self, position: Vector2, range: float = inf, filter = lambda: True) -> Entity | None:
        closest_dist = inf
        closest_entity = None

        for entity in self.entities.values():
            if not filter(entity):
                continue

            dist = entity.position.distance_squared_to(position)
            if dist < range and dist < closest_dist:
                closest_dist = dist
                closest_entity = entity

        return closest_entity

    def get_entities_in_range(self, position: Vector2, range: float = inf, filter=lambda x: True) -> list[Entity]:
        entities = []

        for entity in self.entities.values():
            if not filter(entity):
                continue

            dist = entity.position.distance_squared_to(position)
            if dist < range:
                entities.append(entity)
    
        return entities

    def create_enemy(self):
        enemy = Entity(name="enemy", entity_type="enemy")
        enemy.alliance = Alliance.opponent
        enemy.set_data(ENTITIES["enemy"])

        default_attributes = ENTITIES["enemy"]["attributes"]

        for attribute_id in ENTITIES["enemy"]["scaling"]:
            scaling_fn = ENTITIES["enemy"]["scaling"][attribute_id]
            value = round(scaling_fn(default_attributes[attribute_id], self.game_duration))
            enemy.set_attribute(attribute_id, value)
            print(f"[Enemy] {attribute_id} {value}")

            if attribute_id == Attributes.max_health:
                enemy.set_attribute(Attributes.health, value)

        enemy.add_component(PhysicsComponent())
        enemy.add_component(EnemyComponent())
        return enemy

    def create_powerup(self):
        entity = Entity(name="powerup", entity_type="powerup")

        bonus = random.choice(ENTITIES["powerup"]["bonuses"])
        powerup = PowerupComponent({ bonus[0]: bonus[1] })
        entity.add_component(powerup)
        
        return entity