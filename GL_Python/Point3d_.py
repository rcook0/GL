# graphics_package/point3d.py
from graphics_package.matrix import Matrix
from graphics_package.vector4d import Vector4d

class Point3d(Matrix):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(4, 1, 0.0)
        self.m[0][0] = x
        self.m[1][0] = y
        self.m[2][0] = z
        self.m[3][0] = 1.0  # homogeneous coord

    @classmethod
    def from_vector(cls, v: Vector4d):
        return cls(v.x(), v.y(), v.z())

    def x(self): return self.m[0][0]
    def y(self): return self.m[1][0]
    def z(self): return self.m[2][0]

    def set_x(self, val): self.m[0][0] = val
    def set_y(self, val): self.m[1][0] = val
    def set_z(self, val): self.m[2][0] = val

    def __str__(self):
        return f"({self.x():.3f}, {self.y():.3f}, {self.z():.3f})"
