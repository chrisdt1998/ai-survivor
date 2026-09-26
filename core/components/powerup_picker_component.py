from core.components.powerup_component import PowerupComponent
from core.entity import Component

class PowerupPickerComponent(Component):
    
    def setup(self):
        self.pickup_range = 3

    def update(self, delta):
        powerups = self.entity.simulation.get_entities_in_range(
            self.entity.position,
            self.pickup_range,
            lambda e: e.entity_type == "powerup"
        )

        for powerup_entity in powerups:
            powerup = powerup_entity.get_component(PowerupComponent)
            for attribute_id in powerup.attribute_bonuses:
                value = powerup.attribute_bonuses[attribute_id]
                self.entity.add_attribute(attribute_id, value)

            self.entity.simulation.emit("powerup_picked", {
                "source": self.entity,
                "powerup": powerup_entity,
            })
            powerup_entity.destroy()
