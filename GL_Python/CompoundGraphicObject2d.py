from typing import List
from .Point2d import Point2d
from .Transformation2d import Transformation2d
from .GraphicObject2d import GraphicObject2d
from .GraphicObjectIdentifier import GraphicObjectIdentifier
from .ForeignObjectException import ForeignObjectException

class CompoundGraphicObject2d(GraphicObject2d):
    classCGO2d = "CompoundGraphicObject2d"
    classGO2d = "GraphicObject2d"

    def __init__(self, localOrigin: Point2d | None = None):
        super().__init__()
        self.localOrigin = localOrigin or Point2d(0, 0)
        self.parts: List[GraphicObject2d] = []
        self.numberOfParts = 0

    def getGraphicObject(self, o: object) -> GraphicObjectIdentifier:
        if isinstance(o, GraphicObject2d):
            return GraphicObjectIdentifier(self.classGO2d, o)
        elif isinstance(o, CompoundGraphicObject2d):
            return GraphicObjectIdentifier(self.classCGO2d, o)
        else:
            raise ForeignObjectException(f"Unsupported object: {type(o)}", o)

    def clear(self) -> None:
        self.numberOfParts = 0
        self.parts.clear()

    def add(self, obj: GraphicObject2d) -> None:
        self.numberOfParts += 1
        self.parts.append(obj)

    def draw(self, g=None) -> None:
        for o in self.parts:
            try:
                id_ = self.getGraphicObject(o)
                go2d = id_.getObject()
                go2d.draw(g)
            except ForeignObjectException:
                continue

    def erase(self, g=None) -> None:
        for o in self.parts:
            try:
                id_ = self.getGraphicObject(o)
                go2d = id_.getObject()
                go2d.erase(g)
            except ForeignObjectException:
                continue

    def transform(self, trans: Transformation2d) -> None:
        for o in self.parts:
            try:
                id_ = self.getGraphicObject(o)
                go2d = id_.getObject()
                go2d.transform(trans)
            except ForeignObjectException:
                continue
        self.localOrigin.transform(trans)
