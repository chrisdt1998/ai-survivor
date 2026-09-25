from math import inf
from collections import defaultdict

from core.vector2 import Vector2
from core.level import Level
from core.entity import Entity, Alliance
from core.attributes import Attributes
from core.actions.action import Action
from core.components.attack_component import AttackComponent
from core.components.physics_component import PhysicsComponent
from core.spawner import Spawner

class Simulation:

    event_handlers = defaultdict(list)
    event_queue = []

    def __init__(self):
        self.entities: dict[int, Entity] = {}
        self.entity_next_id: int = 0
        
        self.entities_to_remove: list[Entity] = []
        self.entities_to_add: list[Entity] = []
    
        self.map_min = Vector2(-10, -10)
        self.map_max = Vector2(10, 10)
        self.level = Level(self.map_min, self.map_max)

        self.spawner = Spawner(self)

        self.homestead = Entity(name="homestead", entity_type="homestead", position=Vector2(0, 0))
        self.homestead.alliance = Alliance.ally
        self.homestead.set_attribute(Attributes.health, 50)
        self.homestead.set_attribute(Attributes.move_speed, 0)
        self.homestead.add_component(PhysicsComponent())
        self.add_entity(self.homestead)

        player = Entity(name="player", entity_type="player", position=Vector2(3, 0))
        player.alliance = Alliance.ally
        player.set_attribute(Attributes.health, 30)
        player.set_attribute(Attributes.move_speed, 5.0)
        player.set_attribute(Attributes.damage, 5.0)
        player.set_attribute(Attributes.attack_speed, 0.5)
        player.set_attribute(Attributes.attack_range, 10.0)
        player.add_component(PhysicsComponent())
        player.add_component(AttackComponent())
        self.add_entity(player)

    def listen(self, event_type, callback):
        self.event_handlers[event_type].append(callback)

    def emit(self, event_type, data):
        self.event_queue.append((event_type, data))
        print(f"[Event] {event_type}")
    
    def drain_events(self):
        for (event_type, data) in self.event_queue:
            callbacks = self.event_handlers[event_type]
            for cb in callbacks:
                cb(data)
        self.event_queue.clear()

    def update(self, delta: float, actions: list[Action] = []):
        for action in actions:
            action.apply(self, delta)
        
        self.spawner.update(delta)
        self.level.update(delta)

        for entity in self.entities.values():
            entity.update(delta)
        
        for entity_id in self.entities_to_remove:
            self.entities.pop(entity_id)
        self.entities_to_remove.clear()

    def add_entity(self, entity: Entity):
        if entity.id != -1:
            print("Entity already added")
            return
            
        self.entity_next_id += 1
        entity.id = self.entity_next_id
        entity.simulation = self
        self.entities[entity.id] = entity
        entity.setup()
        self.emit("entity_added", entity)

    def destroy_entity(self, entity: Entity):
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

    def get_entities_in_range(self, position: Vector2, range: float = inf, filter = lambda: True) -> list[Entity]:
        entities = []

        for entity in self.entities.values():
            if not filter(entity):
                continue

            dist = entity.position.distance_squared_to(position)
            if dist < range:
                entities.append(entity)
    
        return entities

