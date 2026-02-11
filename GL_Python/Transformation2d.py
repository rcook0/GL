
from .Matrix import Matrix
import math

class Transformation2d(Matrix):
    def __init__(self):
        super().__init__(3, 3, 0.0)
        self.m[0][0] = 1.0
        self.m[1][1] = 1.0
        self.m[2][2] = 1.0

    def translate(self, x: float, y: float) -> None:
        self.m[0][2] = float(x)
        self.m[1][2] = float(y)

    def rotate(self, angle: float) -> None:
        c = math.cos(angle); s = math.sin(angle)
        self.m[0][0] = c; self.m[1][0] = -s
        self.m[0][1] = s; self.m[1][1] = c
