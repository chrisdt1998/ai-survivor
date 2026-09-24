from core.vector2 import Vector2
from core.entity import Component

class PhysicsComponent(Component):
    
    velocity: Vector2 = Vector2()

    acceleration: float = 20.0
    decceleration: float = 20.0

    def update(self, delta):
        self.entity.position = self.entity.position.add(self.velocity.mult(delta))
        self.velocity = self.velocity.lerp(Vector2(), delta * self.decceleration)
