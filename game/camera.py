from core.entity import Entity
from core.vector2 import Vector2

class Camera:

    position = Vector2()
    offset = Vector2()
    target: Entity = None

    def __init__(self, screen, pixel_size):
        self.set_screen(screen, pixel_size)

    def set_screen(self, screen, pixel_size):
        self.offset = Vector2(
            screen.get_rect().centerx,
            screen.get_rect().centery,
        ).div(pixel_size)

    def update(self, delta):
        if self.target:
            target_pos = self.target.position.minus(self.offset)
            self.position = self.position.lerp(target_pos, delta * 5)
