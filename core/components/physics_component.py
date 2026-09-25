from core.vector2 import Vector2
from core.entity import Component

class Circle:

    def __init__(self, radius):
        self.radius = radius

class Rectangle:

    def __init__(self, width, height):
        self.width = width
        self.height = height

class PhysicsComponent(Component):

    def __init__(self):
        self.velocity: Vector2 = Vector2()
        self.acceleration: float = 5.0
        self.decceleration: float = 5.0

        self.hitbox = Circle(1.0)

    def update(self, delta):
        self.entity.position = self.entity.position.add(self.velocity.mult(delta))
        self.velocity = self.velocity.lerp(Vector2(), delta * self.decceleration)
