from core.attributes import Attributes
from core.vector2 import Vector2

class Action:

    def execute(self, simulation, delta: float):
        pass

class MoveAction(Action):

    def __init__(self, entity_id, direction: Vector2):
        self.entity_id = entity_id
        self.direction = direction.normalize()
    
    def execute(self, simulation, delta: float):
        entity = simulation.get_entity(self.entity_id)
        move_speed = entity.get_attribute(Attributes.move_speed)
        entity.position.x += self.direction.x * move_speed * delta
        entity.position.y += self.direction.y * move_speed * delta
