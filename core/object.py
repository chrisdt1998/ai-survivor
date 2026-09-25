
class Object:

    def __init__(self):
        self.id = -1

class ObjectList:
    
    def __init__(self):
        self._objects = []
        self._free_ids = []
    
    def values(self):
        for object in self._objects:
            if object:
                yield object

    def add(self, sprite: Object):
        if self._free_ids:
            sprite.id = self._free_ids.pop()
            self._objects[sprite.id] = sprite
        else:
            sprite.id = len(self._objects)
            self._objects.append(sprite)

    def remove(self, object: Object):
        pass
