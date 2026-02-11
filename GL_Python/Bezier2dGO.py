
from .GraphicObject2d import GraphicObject2d
from .Bezier2d import Bezier2d
from .Point2d import Point2d
from .Transformation2d import Transformation2d

class Bezier2dGO(GraphicObject2d):
    def __init__(self, control_points: list[Point2d], steps: int = 20):
        super().__init__(control_points[0] if control_points else Point2d(0, 0))
        self.control_points = control_points
        self.steps = steps
        self._curve = Bezier2d([(p.x(), p.y()) for p in control_points], steps)

    def draw(self, g=None) -> None:
        self._points = self._curve.compute_points()

    def erase(self, g=None) -> None:
        self._points = []

    def transform(self, trans: Transformation2d) -> None:
        self.control_points = [trans @ p for p in self.control_points]
        self._curve = Bezier2d([(p.x(), p.y()) for p in self.control_points], self.steps)

    def get_points(self) -> list[tuple[float, float]]:
        return getattr(self, "_points", [])
