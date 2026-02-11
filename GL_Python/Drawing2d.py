# graphics_package/Drawing2d.py
from .CompoundGraphicObject2d import CompoundGraphicObject2d
from .GraphicObject2d import GraphicObject2d
from .Transformation2d import Transformation2d

class Drawing2d(CompoundGraphicObject2d):
    """
    Top-level container for 2D graphics data.
    Extends CompoundGraphicObject2d.
    """

    def __init__(self):
        super().__init__()

    def add(self, o: GraphicObject2d) -> None:
        super().add(o)

    def transform(self, trans: Transformation2d) -> None:
        super().transform(trans)

    def draw(self, g=None) -> None:
        super().draw(g)

    def erase(self, g=None) -> None:
        super().erase(g)

    def clear(self) -> None:
        self.parts.clear()
