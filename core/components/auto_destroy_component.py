from core.entity import Component

class AutoDestroyComponent(Component):

    def __init__(self, duration):
        super()
        self.timer = duration

    def update(self, delta):
        self.timer -= delta
        if self.timer <= 0:
            self.entity.destroy()
