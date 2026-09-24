from math import sqrt

class Vector2:

    x: float = 0
    y: float = 1

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def length(self) -> float:
        return sqrt((self.x * self.x) + (self.y * self.y))
    
    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector2(self.x / length, self.y / length)
        else:
            return Vector2()
    
    def mult(self, value: float):
        return Vector2(self.x * value, self.y * value)

    def add(self, vector: Vector2):
        return Vector2(self.x + vector.x, self.y + vector.x)

    def minus(self, vector: Vector2):
        return Vector2(self.x - vector.x, self.y - vector.x)

    def to_tuple(self):
        return (self.x, self.y)
