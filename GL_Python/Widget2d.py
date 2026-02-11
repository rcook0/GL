
import math
from .GraphicObject2d import GraphicObject2d
from .Point2d import Point2d

class Widget2d(GraphicObject2d):
    def __init__(self, position: Point2d, dimension, visible: bool, owner):
        super().__init__(position)
        self.position = position
        if isinstance(dimension, tuple):
            self.width, self.height = dimension
        else:
            self.width = getattr(dimension, 'width', 20)
            self.height = getattr(dimension, 'height', 20)
        self.visible = visible
        self.owner = owner
        self._selected = False

    def select(self): self._selected = True
    def deselect(self): self._selected = False
    def isSelected(self) -> bool: return self._selected

    def hasPoint(self, x: int, y: int) -> bool:
        halfw, halfh = self.width / 2, self.height / 2
        dx = abs(x - self.position.x())
        dy = abs(y - self.position.y())
        return dx <= halfw and dy <= halfh

    @staticmethod
    def angleOfRotation(centre: Point2d, selPoint: Point2d) -> float:
        dx = selPoint.x() - centre.x()
        dy = selPoint.y() - centre.y()
        return math.atan2(dy, dx)
