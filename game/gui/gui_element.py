from core.vector2 import Vector2
from core.object import Object

class GuiElement(Object):

    def __init__(
        self,
        position: Vector2=Vector2(),
        size: Vector2=Vector2(),
        direction = "vertical",
        alignment = "start",
        items_alignment = "start",
        horizontal_sizing = "default",
        vertical_sizing = "default",
        spacing = 10,
        margin = (0, 0, 0, 0), # Top, Right, Bottom, Left
    ):
        super().__init__()

        self.position = position
        self.size = size
        self.horizontal_sizing = horizontal_sizing
        self.vertical_sizing = vertical_sizing
        self.scale = Vector2()
        self.parent = None

        self.direction = direction
        self.alignment = alignment
        self.items_alignment = items_alignment
        self.spacing = spacing
        self.margin = margin

        self.children = []
        self._parent_screen_pos = Vector2()
    
    @property
    def screen_position(self):
        return self._parent_screen_pos

    def add_child(self, child):
        if child.parent:
            raise KeyError("gui element already has a prent")
        child.parent = self

        self._update_child(child)
        self.children.append(child)

    def remove_child(self, child):
        for i in range(len(self.children)):
            if self.children[i] == child:
                child.parent = None
                self.children.pop(i)
                return

    def render(self, screen, delta):
        pass

    def _render(self, screen, delta):
        self.render(screen, delta)
        for child in self.children:
            child._parent_screen_pos = self.screen_position.add(child.position)
            child._render(screen, delta)

    def _update_child(self, element):
        if self.direction == "unset":
            return

        margin = Vector2(self.margin[3], self.margin[0])
        if self.children:
            element.position = self._get_relative_pos(element, self.children[-1]).add(margin)
        else:
            element.position = Vector2(margin.x, margin.y)

        if element.horizontal_sizing == "fill":
            element.size.x = self.size.x - self.margin[1] - self.margin[3]
        
        if element.vertical_sizing == "fill":
            element.size.y = self.size.y - self.margin[0] - self.margin[2]

    def _get_relative_pos(self, element, previous):
        if self.direction == "vertical":
            x = previous.position.x
            y = previous.position.y + previous.size.y + self.spacing
            return Vector2(x, y)

        elif self.direction == "horizontal":
            x = previous.position.x + previous.size.x + self.spacing
            y = previous.position.y
            return Vector2(x, y)
