from core.vector2 import Vector2
from core.object import Object

class GuiElement(Object):

    def __init__(self, position: Vector2):
        super()
        self.position = position
    
    def render(self, screen, delta):
        pass