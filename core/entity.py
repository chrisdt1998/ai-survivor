from core.attributes import Attributes
from typing import TYPE_CHECKING
from ast import TypeVar

from core.vector2 import Vector2

if TYPE_CHECKING:
    from core.simulation import Simulation


class Component:

    def __init__(self):
        self.entity: Entity | None = None

    def setup(self):
        pass

    def on_destroyed(self):
        pass

    def update(self, delta: float):
        pass


class Alliance:
    neutral = 0
    ally = 1
    opponent = 2


T = TypeVar("T")

class Entity:

    def __init__(self, name="", entity_type="", position=Vector2(0, 0)):
        self.id: int = -1
        self.is_destroyed = False
        self.simulation: Simulation = None

        self.position: Vector2 = position
        self.name: str = name
        self.entity_type: str = entity_type
        self.alliance = Alliance.neutral
        self.tags = set()
        self.attributes: dict[str, float] = {}
        self.components: dict[type, Component] = {}
        self.rotation: float = 0

    def set_data(self, data):
        if "attributes" in data:
            for attribute_id in data["attributes"]:
                self.set_attribute(attribute_id, data["attributes"][attribute_id])
            
            max_health = self.get_attribute(Attributes.max_health)
            self.set_attribute(Attributes.health, max_health)

    def setup(self):
        for comp in self.components.values():
            comp.setup()

    def update(self, delta: float):
        for comp in self.components.values():
            comp.update(delta)
    
    def on_destroyed(self):
        for comp in self.components.values():
            comp.on_destroyed()

    def has_tag(self, tag) -> bool:
        return tag in self.tags

    def destroy(self):
        if self.is_destroyed:
            return
        self.is_destroyed = True
        self.simulation._destroy_entity(self)

    def add_component(self, component: Component):
        component.entity = self
        self.components[type(component)] = component

        if self.id >= 0:
            component.setup()
    
    def get_component(self, component_type: type[T]) -> T:
        return self.components.get(component_type, None)
    
    def has_component(self, component_type: type):
        return component_type in self.components

    @property
    def health(self):
        return self._health

    @health.setter
    def set_health(self, value):
        self._health = value

    def set_attribute(self, attribute_id: str, value: float):
        old_value = self.attributes.get(attribute_id, 0.0)
        if value == old_value:
            return

        self.attributes[attribute_id] = value

        if self.simulation:
            self.simulation.emit("attribute_changed", {
                "entity": self,
                "attribute_id": attribute_id,
                "old_value": old_value,
                "value": value
            })

        if attribute_id == "health" and value <= 0:
            self.destroy()
    
    def add_attribute(self, attribute_id: str, value: float):
        self.set_attribute(attribute_id, self.attributes[attribute_id] + value)
    
    def get_attribute(self, attribute_id: str) -> float:
        return self.attributes.get(attribute_id, 0)
