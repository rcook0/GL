
from .Matrix import Matrix

class Point2d(Matrix):
    def __init__(self, in_x: float, in_y: float):
        super().__init__(3, 1, 1.0)
        self.m[0][0] = float(in_x)
        self.m[1][0] = float(in_y)

    def x(self) -> float:
        return float(self.m[0][0])

    def y(self) -> float:
        return float(self.m[1][0])
