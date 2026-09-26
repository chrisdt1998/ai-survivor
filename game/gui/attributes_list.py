from game.gui.gui_element import GuiElement
from core.vector2 import Vector2
from game.gui.text import Text
import pygame

class AttributeDescription(GuiElement):

    def __init__(self, attribute_id, value):
        self.name = Text(attribute_id, horizontal_alignment="start")
        self.name.size.x = 100
        self.add_child(self.name)

        self.value = Text(str(value), horizontal_alignment="center")
        self.value.size.x = 50
        self.add_child(self.value)

class AttributesList(GuiElement):

    def __init__(self, position: Vector2, simulation, entity):
        super().__init__(
            position,
            direction="vertical",
            margin=(0, 0, 0, 0),
            spacing=0,
        )

        simulation.listen("attribute_changed", self.on_attribute_changed)

        self.entity_id = entity.id
        self.attributes = {}
        for attribute_id in entity.attributes:
            content = f"{attribute_id} {entity.get_attribute(attribute_id)}"
            text = Text(content, font_size=20)
            self.add_child(text)
            self.attributes[attribute_id] = text

    def on_attribute_changed(self, data):
        entity = data["entity"]
        if entity.id == self.entity_id:
            attribute_id = data["attribute_id"]
            text = f"{attribute_id} {entity.get_attribute(attribute_id)}"
            self.attributes[attribute_id].set_text(text)
