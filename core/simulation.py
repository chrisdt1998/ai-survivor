from core.vector2 import Vector2
from core.attributes import Attributes
from core.actions.action import Action
from core.entity import Entity

class Simulation:

    entities: list[Entity] = []
    level = None

    def __init__(self):
        player = Entity(name="player", position=Vector2(10, 10))
        player.set_attribute(Attributes.health, 30)
        player.set_attribute(Attributes.move_speed, 300)
        self.add_entity(player)

    def update(self, delta: float, actions: list[Action] = []):
        for action in actions:
            action.execute(self, delta)
        
        for entity in self.entities:
            entity.update(delta)

    def add_entity(self, entity: Entity):
        entity.id = len(self.entities)
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        self.entities.pop(entity.id)
    
    def get_entity(self, entity_id: int) -> Entity:
        return self.entities[entity_id]
    
    def get_entity_by_name(self, entity_name: str) -> Entity:
        for entity in self.entities:
            if entity.name == entity_name:
                return entity
        return None
