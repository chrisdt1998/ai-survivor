from core.entity import Entity
from core.components.physics_component import PhysicsComponent
from core.attributes import Attributes
from core.vector2 import Vector2

class Action:

    def apply(self, simulation, delta: float):
        pass

class MoveAction(Action):

    def __init__(self, entity: Entity, direction: Vector2):
        self.entity = entity
        self.direction = direction.normalize()
    
    def apply(self, simulation, delta: float):
        move_speed = self.entity.get_attribute(Attributes.move_speed)
        physics_component = self.entity.get_component(PhysicsComponent)
        physics_component.velocity = self.direction.mult(move_speed)

class AttackAction(Action):

    def __init__(self, entity: Entity, shoot_direction: Vector2):
        self.entity = entity
        self.shoot_direction = shoot_direction.normalize()
    
    def apply(self, simulation, delta: float):
        pass