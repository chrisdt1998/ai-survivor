from core.attributes import Attributes
from core.components.physics_component import PhysicsComponent
from core.entity import Entity
from core.vector2 import Vector2
from core.entity import Component

class EnemyComponent(Component):
    
    homestead: Entity
    target: Entity

    def update(self, delta):
        _target = self.target if self.target else self.homestead
        direction = self.entity.position.direction_to(_target.position)
        
        move_speed = self.entity.get_attribute(Attributes.move_speed)
        physics = self.entity.get_component(PhysicsComponent)
        physics.velocity = direction.mult(move_speed)
