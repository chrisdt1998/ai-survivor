from collections import defaultdict
from core.level import Level
from core.components.physics_component import PhysicsComponent
from core.vector2 import Vector2
from core.attributes import Attributes
from core.actions.action import Action
from core.entity import Entity

class Simulation:

    entities: list[Entity] = []
    level = None

    event_handlers = defaultdict(list)
    event_queue = []

    def __init__(self):
        self.level = Level()

        player = Entity(name="player", entity_type="player", position=Vector2(10, 10))
        player.set_attribute(Attributes.health, 30)
        player.set_attribute(Attributes.move_speed, 300)
        player.add_component(PhysicsComponent())
        self.add_entity(player)

    def listen(self, event_type, callback):
        self.event_handlers[event_type].append(callback)

    def emit(self, event_type, data):
        self.event_queue.append((event_type, data))
    
    def drain_events(self):
        for (event_type, data) in self.event_queue:
            callbacks = self.event_handlers[event_type]
            for cb in callbacks:
                cb(data)
        self.event_queue.clear()

    def update(self, delta: float, actions: list[Action] = []):
        for action in actions:
            action.apply(self, delta)
        
        for entity in self.entities:
            entity.update(delta)

    def add_entity(self, entity: Entity):
        entity.id = len(self.entities)
        self.entities.append(entity)
        self.emit("entity_added", entity)

    def remove_entity(self, entity: Entity):
        self.entities.pop(entity.id)
        self.emit("entity_destroyed", entity)
    
    def get_entity(self, entity_id: int) -> Entity:
        return self.entities[entity_id]
    
    def get_entity_by_name(self, entity_name: str) -> Entity:
        for entity in self.entities:
            if entity.name == entity_name:
                return entity
        return None
