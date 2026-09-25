from core.vector2 import Vector2
from core.entity import Component

class PhysicsComponent(Component):

    def __init__(self):
        self.velocity: Vector2 = Vector2()
        self.acceleration: float = 5.0
        self.decceleration: float = 5.0

    def update(self, delta):
        self.entity.position = self.entity.position.add(self.velocity.mult(delta))
        self.velocity = self.velocity.lerp(Vector2(), delta * self.decceleration)
