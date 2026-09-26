from core.attributes import Attributes
from core.entity import Component

class HealthRegenComponent(Component):

    def __init__(self, delay=1.0):
        super().__init__()
        self.delay = delay
        self.timer = delay

    def update(self, delta):
        self.timer -= delta
        if self.timer <= 0:
            self.timer = self.delay
            health_regen = self.entity.get_attribute(Attributes.health_regen)
            self.entity.add_attribute(Attributes.health, health_regen)
