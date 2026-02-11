# graphics_package/vector4d.py
import math
from graphics_package.matrix import Matrix
from graphics_package.point3d import Point3d

class Vector4d(Matrix):
    def __init__(self, x=0.0, y=0.0, z=0.0, h=None):
        super().__init__(4, 1, 0.0)
        self.m[0][0] = x
        self.m[1][0] = y
        self.m[2][0] = z
        self.m[3][0] = 1.0 if h is None else h

    @classmethod
    def from_point(cls, p: Point3d):
        return cls(p.x(), p.y(), p.z(), 1.0)

    @classmethod
    def from_points(cls, a: Point3d, b: Point3d):
        return cls(b.x() - a.x(), b.y() - a.y(), b.z() - a.z(), 0.0)

    def x(self): return self.m[0][0]
    def y(self): return self.m[1][0]
    def z(self): return self.m[2][0]
    def h(self): return self.m[3][0]

    def add(self, v: "Vector4d"):
        self.m[0][0] += v.x()
        self.m[1][0] += v.y()
        self.m[2][0] += v.z()
        self.m[3][0] += v.h()

    def divide(self, n: float):
        for i in range(4):
            self.m[i][0] /= n

    def multiply(self, n: float):
        for i in range(4):
            self.m[i][0] *= n

    def length(self) -> float:
        return math.sqrt(self.x()**2 + self.y()**2 + self.z()**2 + self.h()**2)

    def homogenize(self):
        w = self.m[3][0]
        if w != 1.0 and w != 0.0:
            self.m[0][0] /= w
            self.m[1][0] /= w
            self.m[2][0] /= w
            self.m[3][0] = 1.0

    @staticmethod
    def sum(v1: "Vector4d", v2: "Vector4d") -> "Vector4d":
        return Vector4d(v1.x() + v2.x(), v1.y() + v2.y(), v1.z() + v2.z(), v1.h() + v2.h())

    @staticmethod
    def quotient(v1: "Vector4d", v2: "Vector4d") -> "Vector4d":
        return Vector4d(v1.x() / v2.x(), v1.y() / v2.y(), v1.z() / v2.z(), v1.h() / v2.h())

    @staticmethod
    def dot_product(u: "Vector4d", v: "Vector4d") -> "Vector4d":
        return Vector4d(u.x() * v.x(), u.y() * v.y(), u.z() * v.z())

    @staticmethod
    def product(u: "Vector4d", v: "Vector4d") -> "Vector4d":
        multI = (u.y() * v.z()) - (u.z() * v.y())
        multJ = (u.z() * v.x()) - (u.x() * v.z())
        multK = (u.x() * v.y()) - (u.y() * v.x())
        return Vector4d(multI, multJ, multK)

    def to_point3d(self) -> Point3d:
        return Point3d(self.x(), self.y(), self.z())
