import math
from math import sqrt

def rad_to_deg(value):
    pass

def clamp(value, min_value, max_value):
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value

class Vector2:

    x: float = 0
    y: float = 1

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __hash__(self):
        return f"({self.x}, {self.y})".__hash__()
    
    def __eq__(self, other):
        return other is Vector2 and self.x == other.x and self.y == other.y

    def length(self) -> float:
        return sqrt((self.x * self.x) + (self.y * self.y))

    def length_squared(self) -> float:
        return (self.x * self.x) + (self.y * self.y)
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector2(self.x / length, self.y / length)
        else:
            return Vector2()
    
    def lerp(self, target, t):
        return Vector2(
            (1.0 - t) * self.x + t * target.x,
            (1.0 - t) * self.y + t * target.y,
        )

    def mult(self, value: float):
        return Vector2(self.x * value, self.y * value)

    def div(self, value: float):
        return Vector2(self.x / value, self.y / value)

    def add(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)

    def minus(self, vector):
        return Vector2(self.x - vector.x, self.y - vector.y)

    def direction_to(self, target):
        return target.minus(self).normalize()

    def distance_to(self, vector):
        return vector.minus(self).length()
    
    def distance_squared_to(self, vector):
        return vector.minus(self).length_squared()
    
    def angle(self):
        return math.atan(self.y / self.x)

    def clamp(self, min_vector, max_vector):
        return Vector2(
            clamp(self.x, min_vector.x, max_vector.x),
            clamp(self.y, min_vector.y, max_vector.y),
        )

    def to_tuple(self):
        return (self.x, self.y)
    
