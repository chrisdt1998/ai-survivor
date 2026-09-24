from core.vector2 import Vector2
from core.components.component import Component

class Entity:

    id = -1
    name: str = ""
    position = Vector2(0, 0)
    components: list[Component] = []
    attributes: dict[str, float] = {}

    def __init__(self, name="", position=Vector2(0, 0)):
        self.position = position
        self.name = name

    def update(self, delta: float):
        for comp in self.components:
            comp.update(delta)

    def add_component(self, component: Component):
        component.entity = self
        self.components.append(component)

    def set_attribute(self, attribute_id: str, value: float):
        self.attributes[attribute_id] = value
    
    def get_attribute(self, attribute_id: str) -> float:
        return self.attributes.get(attribute_id, 0)
