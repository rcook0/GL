
from .GraphicObject2d import GraphicObject2d
from .Point2d import Point2d
from .Transformation2d import Transformation2d

class Line2d(GraphicObject2d):
    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        super().__init__(Point2d(x1, y1))
        self.p1 = Point2d(x1, y1)
        self.p2 = Point2d(x2, y2)

    def getDestinationPoint(self) -> Point2d:
        return self.p2

    def transform(self, trans: Transformation2d) -> None:
        self.p1 = trans @ self.p1
        self.p2 = trans @ self.p2

    def rasterize(self) -> list[tuple[int, int]]:
        x1, y1 = int(round(self.p1.x())), int(round(self.p1.y()))
        x2, y2 = int(round(self.p2.x())), int(round(self.p2.y()))
        points = []

        dx = abs(x2 - x1)
        dy = -abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx + dy

        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x1 += sx
            if e2 <= dx:
                err += dx
                y1 += sy

        return points
