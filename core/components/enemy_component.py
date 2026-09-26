from core.entity import Alliance
from core.attributes import Attributes
from core.components.physics_component import PhysicsComponent
from core.entity import Entity, Component

class EnemyComponent(Component):

    def setup(self):
        self.physics = self.entity.get_component(PhysicsComponent)
        self.target: Entity = None
        self.attack_timer = 0
        self.chase_range = 5

    def update(self, delta):
        close_target = self.entity.simulation.get_closest(
            self.entity.position,
            self.chase_range,
            lambda e: e.alliance == Alliance.ally
        )

        self.target = close_target if close_target else self.entity.simulation.homestead
        if not self.target:
            return

        direction = self.entity.position.direction_to(self.target.position)
        self.entity.rotation = direction.angle()

        distance = self.entity.position.distance_to(self.target.position)
        if distance < self.entity.get_attribute(Attributes.attack_range) * 0.75:
            self.attack(delta)
        else:
            self.chase(direction)
    
    def chase(self, direction):
        move_speed = self.entity.get_attribute(Attributes.move_speed)
        self.physics.velocity = direction.mult(move_speed)

    def attack(self, delta):
        if self.attack_timer > 0:
            self.attack_timer -= delta
            return

        attack_speed = self.entity.get_attribute(Attributes.attack_speed)
        self.attack_timer = 1.0 / (attack_speed if attack_speed > 0 else 0.01)

        damage = self.entity.get_attribute(Attributes.damage)
        self.target.add_attribute(Attributes.health, -damage)
        self.entity.simulation.emit("entity_attacked", {
            "source": self.entity,
            "target": self.target,
            "damage": damage,
        })
