
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

    def add(self, object: Object):
        if self._free_ids:
            object.id = self._free_ids.pop()
            self._objects[object.id] = object
        else:
            object.id = len(self._objects)
            self._objects.append(object)

    def remove(self, object: Object):
        self._free_ids.append(object.id)
        self._objects[object.id] = None
