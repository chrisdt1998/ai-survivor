from core.entity import Component

class PowerupComponent(Component):
    
    def __init__(self, attribute_bonuses):
        super().__init__()
        self.attribute_bonuses = attribute_bonuses
