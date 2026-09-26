from core.entity import Alliance
from core.attributes import Attributes
from core.entity import Component

class AttackComponent(Component):
    
    def setup(self):
        self.attack_timer = 0

    def update(self, delta):
        if self.attack_timer > 0:
            self.attack_timer -= delta

        target = self.entity.simulation.get_closest(
            self.entity.position,
            self.entity.get_attribute(Attributes.attack_range),
            lambda e: e.alliance != Alliance.neutral and e.alliance != self.entity.alliance
        )

        if not target:
            return

        direction = self.entity.position.direction_to(target.position)
        self.entity.rotation = direction.angle()

        if self.attack_timer > 0:
            return

        attack_speed = self.entity.get_attribute(Attributes.attack_speed)
        self.attack_timer = 1.0 / (attack_speed if attack_speed > 0 else 0.01)

        damage = self.entity.get_attribute(Attributes.damage)
        target.add_attribute(Attributes.health, -damage)
        self.entity.simulation.emit("entity_attacked", {
            "source": self.entity,
            "target": target,
            "damage": damage,
        })

