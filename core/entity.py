from ast import TypeVar
from core.vector2 import Vector2


class Component:

    def __init__(self):
        self.entity: Entity | None = None

    def update(self, delta: float):
        pass


T = TypeVar("T")

class Entity:

    id = -1
    name: str = ""
    entity_type: str = ""
    position = Vector2(0, 0)
    _components: dict[type, Component] = {}
    attributes: dict[str, float] = {}

    def __init__(self, name="", entity_type="", position=Vector2(0, 0)):
        self.position = position
        self.name = name
        self.entity_type = entity_type

    def update(self, delta: float):
        for comp in self._components.values():
            comp.update(delta)

    def add_component(self, component: Component):
        component.entity = self
        self._components[type(component)] = component
    
    def get_component(self, component_type: type[T]) -> T:
        return self._components.get(component_type, None)
    
    def has_component(self, component_type: type):
        return component_type in self._components

    def set_attribute(self, attribute_id: str, value: float):
        self.attributes[attribute_id] = value
    
    def get_attribute(self, attribute_id: str) -> float:
        return self.attributes.get(attribute_id, 0)
