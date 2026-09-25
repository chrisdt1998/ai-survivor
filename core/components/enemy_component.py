from core.attributes import Attributes
from core.components.physics_component import PhysicsComponent
from core.entity import Entity, Component

class EnemyComponent(Component):
    
    target: Entity = None
    physics: PhysicsComponent = None

    def setup(self):
        self.physics = self.entity.get_component(PhysicsComponent)

    def update(self, delta):
        _target = self.target if self.target else self.entity.simulation.homestead
        if not _target:
            return

        direction = self.entity.position.direction_to(_target.position)
        
        move_speed = self.entity.get_attribute(Attributes.move_speed)
        self.physics.velocity = direction.mult(move_speed)
