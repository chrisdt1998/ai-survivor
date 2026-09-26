from core.vector2 import Vector2
from core.attributes import Attributes
from game.gui.gui_panel import GUIPanel
from game.gui.gui_text import GUIText
from game.gui.gui_element import GUIElement

class Healthbar(GUIElement):
    
    def __init__(self, position, simulation, entity):
        super().__init__(
            position,
            direction="unset",
            size=Vector2(150, 30)
        )

        self.entity = entity
        self.max_health = entity.get_attribute(Attributes.max_health)
        self.current_health = entity.get_attribute(Attributes.health)

        self.bar_size = Vector2(100, 30)
        self.text = self.add_child(GUIText(str(self.current_health), position=Vector2(100, 0)))
        self.background = self.add_child(GUIPanel(color=(100, 100, 100), size=self.bar_size))
        self.foreground = self.add_child(GUIPanel(color=(255, 255, 255), size=self.bar_size))

        simulation.listen("attribute_changed", self.handle_attribute_changed)

    def handle_attribute_changed(self, event):
        target = event["entity"]
        if target == self.entity:
            max_health = target.get_attribute(Attributes.max_health)
            current_health = target.get_attribute(Attributes.health)
            self.text.set_text(str(current_health))
            self.foreground.size = Vector2(
                self.bar_size.x * (self.current_health / max_health),
                self.bar_size.y
            )